from __future__ import division # float division of integers
from collections import deque

import pyaudio
import wave
import struct
import math
import numpy
import sys
import threading
import reedsolo
from ecc import OnebyteReadSolomonEcc

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
    self.coder = OnebyteReadSolomonEcc()
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
      powerC = self.goertzel(CHARSTART)
      base = self.goertzel(BASELINE)
      self.update_state(power0, power1, powerC, base)
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
    newbuf = ['-' if x is -1 else x for x in buf]
    print(repr(newbuf).replace(', ', '').replace('\'', ''))

  # Takes the raw noisy samples of -1/0/1 and finds the bitstream from it
  def signal_to_bits(self):
    if len(self.buffer) < self.buf_len:
      return
    buf = list(self.buffer)
    
    if self.debug:
      self.printbuf(buf)
    
    costs = [[] for i in range(4)]
    for i in range(self.win_fudge):
      win = buf[i : self.win_len + i]
      costs[0].append(sum(x != 0 for x in win))
      costs[1].append(sum(x != 1 for x in win))
      costs[2].append(sum(x != 2 for x in win))
      costs[3].append(sum(x != -1 for x in win))
    min_costs = [min(costs[i]) for i in range(4)]
    min_cost = min(min_costs)
    signal = min_costs.index(min_cost)
    fudge = costs[signal].index(min_cost)
    for i in range(self.win_len + fudge):
      self.buffer.popleft()

    # If we got a signal, put it in the byte!
    if signal < 2:
      self.byte.append(signal)
    # If we get a charstart signal, reset byte!
    elif signal == 2:
      self.byte = []
    
    # If we get no signal, increment idlecount if we are idling
    if signal == 3:
      self.idlecount += 1
    else:
      self.idlecount = 0
    if self.idlecount > IDLE_LIMIT and self.idle_callback:
      self.idlecount = 0
      self.idle_callback()

    if self.debug:
      if signal == 3:
        signal = '-'
      sys.stdout.write('')
      sys.stdout.write('|{}|\n'.format(signal))
      sys.stdout.flush()


  def split(self, li, num):
      l = [li[i:i+8] for i in range(0,24,8)]
      res = []
      for dd in l:
        res.append(self.intint(dd))
      return res

  def intint(self, bb):
    ascii = 0
    for bit in bb:
      ascii = (ascii << 1) | bit
    return ascii

  def decode_chr(self):
    rs = reedsolo.RSCodec(2)
    print("****")
    print(self.byte)
    sl = self.split(self.byte, 8)
    print("****:sl" + str(sl))
    return rs.decode(sl)

  # For now, just print out the characters as we go.
  def process_byte(self):
    if len(self.byte) != (8 * 3):
      return
    char_d = self.coder.decode_from_bytes_string(self.byte)
    print("*+*:" + char_d)
    if self.character_callback:
      self.character_callback(char_d)
    else:
      sys.stdout.write(char_d)
      sys.stdout.flush()
    self.byte = []

  # Determine the raw input signal of silences, 0s, and 1s. Insert into sliding window.
  def update_state(self, power0, power1, powerC, base):
    state = -1
    if power1 / base > ONE_THRESH:
      state = 1
    elif power0 / base > ZERO_THRESH:
      state = 0
    elif powerC / base > CHARSTART_THRESH:
      state = 2
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
