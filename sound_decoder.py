from __future__ import division # float division of integers
from collections import deque

import pyaudio
import wave
import struct
import math
import numpy
import sys
import threading
import numpy as np

from constants import *

# Mathy things
TWOPI = 2 * math.pi
WINDOW = numpy.hamming(CHUNK_SIZE)

class Decoder:
  
  def __init__(self, debug):
    self.win_len = 2 * int(BIT_DURATION * RATE / CHUNK_SIZE / 2)
    self.win_fudge = int(self.win_len / 2)
    self.buffer = deque()
    self.buf_len = self.win_len + self.win_fudge
    self.byte = []
    self.idlecount = 0

    self.do_quit = False
    self.character_callback = None
    self.idle_callback = None
    self.debug = debug
    self.p = pyaudio.PyAudio()
    self.stream = self.p.open(format = pyaudio.paInt16,
                  channels = 1,
                  rate = RATE,
                  input = True,
                  frames_per_buffer = AUDIOBUF_SIZE)
    
    listen_thread = threading.Thread(target = self.listen)
    listen_thread.start()

  def listen(self):
    self.do_listen = True
    while (True):
      if self.do_quit == True:
        break
      audiostr = self.stream.read(CHUNK_SIZE)
      if self.do_listen == False:
        continue
      self.audio = list(struct.unpack("%dh" % CHUNK_SIZE, audiostr))
      self.window()
      power0 = self.goertzel(ZERO)
      power1 = self.goertzel(ONE)
      #
      power2 = self.goertzel(TWO)
      power3 = self.goertzel(THREE)
      #
      powerC = self.goertzel(CHARSTART)
      base = self.goertzel(BASELINE)
      self.update_state(power0, power1, power2, power3, powerC, base)
      self.signal_to_bits()
      self.process_byte()
    
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()

  def attach_character_callback(self, func):
    self.character_callback = func

  def attach_idle_callback(self, func):
    self.idle_callback = func

  def start_listening(self):
    self.do_listen = True

  def stop_listening(self):
    self.do_listen = False

  def quit(self):
    self.do_quit = True

  def printbuf(self, buf):
    newbuf = ['-' if x is -2 else x for x in buf]
    print(repr(newbuf).replace(', ', '').replace('\'', ''))

  # Takes the raw noisy samples of -1/0/1 and finds the bitstream from it
  def signal_to_bits(self):
    if len(self.buffer) < self.buf_len:
      return

    buf = list(self.buffer)
    
    if self.debug:
      self.printbuf(buf)
    
    costs = [[] for i in range(6)]
    for i in range(self.win_fudge):
      win = buf[i : self.win_len + i]
      costs[0].append(sum(x != 0 for x in win))
      costs[1].append(sum(x != 1 for x in win))
      costs[2].append(sum(x != 2 for x in win))
      costs[3].append(sum(x != 3 for x in win))
      costs[4].append(sum(x != -1 for x in win))
      costs[5].append(sum(x != -2 for x in win))
    min_costs = [min(costs[i]) for i in range(6)]
    min_cost = min(min_costs)
    signal = min_costs.index(min_cost)
    fudge = costs[signal].index(min_cost)
    for i in range(self.win_len + fudge):
      self.buffer.popleft()

    # If we got a signal, put it in the byte!
    if signal < 4:
      self.byte.append(signal)
    # If we get a charstart signal, reset byte!
    elif signal == 4:
      self.byte = []
    
    # If we get no signal, increment idlecount if we are idling
    if signal == 5:
      self.idlecount += 1
    else:
      self.idlecount = 0
    if self.idlecount > IDLE_LIMIT and self.idle_callback:
      self.idlecount = 0
      self.idle_callback()

    if self.debug:
      if signal == 5:
        signal = '-'
      sys.stdout.write('')
      sys.stdout.write('|{}|\n'.format(signal))
      sys.stdout.flush()

  # For now, just print out the characters as we go.
  def process_byte(self):
    if len(self.byte) != 4:
      return
    #ascii = 0
    #for bit in self.byte:
      #ascii = (ascii << 1) | bit
    ascii = int(''.join([format(i, 'b').zfill(2) for i in self.byte]), 2)
    char = chr(ascii)
    if self.character_callback:
      self.character_callback(char)
    else:
      sys.stdout.write(char)
      sys.stdout.flush()
    self.byte = []

  # Determine the raw input signal of silences, 0s, 1s, 2s, and 3s. Insert into sliding window.
  def update_state(self, power0, power1, power2, power3, powerC, base):
    state = -2 # 無音

    # 各周波数のパワーがしきい値を超えているか判定
    pw = np.array([power0, power1, power2, power3, powerC]) / base
    th = np.array([ZERO_THRESH, ONE_THRESH, TWO_THRESH, THREE_THRESH, CHARSTART_THRESH])
    judge = pw > th
    pw[judge==False] = 0

     # 最大値を求める
    if sum(judge) > 0:
      state = -1 if np.argmax(pw) == 4 else np.argmax(pw)

    # 各周波数のパワーがしきい値を超えているかを判定しているが最大値を見ていない
    # if power3 / base > THREE_THRESH:
    #   state = 3
    # elif power2 / base > TWO_THRESH:
    #   state = 2
    # elif power1 / base > ONE_THRESH:
    #   state = 1
    # elif power0 / base > ZERO_THRESH:
    #   state = 0
    # elif powerC / base > CHARSTART_THRESH:
    #   state = -1
    # print int(power0 / base), int(power1 / base), int(powerC / base)

    if len(self.buffer) >= self.buf_len:
      self.buffer.popleft()
    self.buffer.append(state)

  def goertzel(self, frequency):
    prev1 = 0.0
    prev2 = 0.0
    norm_freq = frequency / RATE
    coeff = 2 * math.cos(TWOPI * norm_freq)
    for sample in self.audio:
      s = sample + (coeff * prev1) - prev2
      prev2 = prev1
      prev1 = s
    power = (prev2 * prev2) + (prev1 * prev1) - (coeff * prev1 * prev2)
    return int(power) + 1 # prevents division by zero problems

  def window(self):
    self.audio = [aud * win for aud, win in zip(self.audio, WINDOW)]

def main():
  if len(sys.argv) == 2 and sys.argv[1] == 'debug':
    dec = Decoder(1)
  else:
    dec = Decoder(0)

if __name__ == "__main__":
  main()
