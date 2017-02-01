from __future__ import division # float division of integers
from collections import deque

import pyaudio
import wave
import struct
import math
import sys
import threading
import numpy as np

from constants import *
from ecc import OnebyteReedSolomonEcc, EmptyEcc

# Mathy things
TWOPI = 2 * math.pi
WINDOW = np.hamming(CHUNK_SIZE)

class Decoder:

  def __init__(self, debug, coder=EmptyEcc()):
    self.win_len = 2 * int(BIT_DURATION * RATE / CHUNK_SIZE / 2)
    self.win_fudge = int(self.win_len / 2)
    self.buffer = [deque() for i in range(len(CHAR_FREQ))]
    self.buf_len = self.win_len + self.win_fudge
    self.byte = []
    self.receivebytes = bytearray()
    self.idlecount = 0
    self.coder = coder
    self.char_window = [deque() for i in range(len(CHAR_FREQ) + 1)]
    self.base_window = deque()
    self.med_len = 5
    self.char_median = [0 for i in range(8)]
    self.base_median = 0

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

  def listen(self):
    # self.do_listen = True
    self.do_quit = False
    self.receivebytes = []

    while (True):
      if self.do_quit == True:
        break
      audiostr = self.stream.read(CHUNK_SIZE)
      # if self.do_listen == False:
      #   continue
      self.audio = list(struct.unpack("%dh" % CHUNK_SIZE, audiostr))
      self.window()
      [char_window[CHAR_FREQ.index(i)].append(self.goertzel(i)) for i in CHAR_FREQ]
      base_window.append(self.goertzel(BASELINE))

    #   powerlist = np.array([self.goertzel(i) for i in CHAR_FREQ])
    #   base = self.goertzel(BASELINE)
      if len(base_window) >= self.med_len:
        self.calc_median(char_window, base_window)
        self.update_state(self.char_median, self.base_median)
        self.signal_to_bits()
        self.process_byte()

    # self.stream.stop_stream()
    # self.stream.close()
    # self.p.terminate()
    return self.receivebytes

  def window(self):
    self.audio = [aud * win for aud, win in zip(self.audio, WINDOW)]

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

  def calc_median(self):
    [self.char_median[self.char_window.index(i)] = np.median(i) for i in self.char_window]
    self.base_median = np.median(self.base_window)
    [i.popleft() for i in self.char_window]
    self.base_window.popleft()

  # Determine the raw input signal of silences, 0s, 1s, 2s, and 3s. Insert into sliding window.
  def update_state(self, powerlist, base):
    # state = -3 # 無音

    # 各周波数のパワーがしきい値を超えているか判定
    pw = powerlist / base
    th = np.array(CHAR_THRESH)
    judge = pw > th
    # pw[judge==False] = 0

     # 最大値を求める
    # if sum(judge) > 0:
    #   state = int(np.argmax(pw) - 2)

    if len(self.buffer[0]) >= self.buf_len:
      [i.popleft() for i in self.buffer]
    for i in range(8):
      self.buffer[i].append(judge[i])

  # Takes the raw noisy samples of -1/0/1 and finds the bitstream from it
  def signal_to_bits(self):
    if len(self.buffer[0]) < self.buf_len:
      return

    buf = [list(i) for i in self.buffer]

    # if self.debug:
    #   self.printbuf(buf)

    costs = [[] for i in range(8)]#
    for i in range(self.win_fudge):
      win = [j[i : self.win_len + i] for j in buf]
      #
      for j in range(len(win)):
        costs[j].append(sum(win[j]))
    #   costs[0].append(sum(x != True for x in win[0]))
    #   costs[1].append(sum(x != True for x in win[1]))
    #   costs[2].append(sum(x != True for x in win[2]))
    #   costs[3].append(sum(x != True for x in win[3]))
    #   costs[4].append(sum(x != True for x in win[4]))
    #   costs[5].append(sum(x != True for x in win[5]))
    #   costs[6].append(sum(x != True for x in win[6]))
    #   costs[7].append(sum(x != True for x in win[7]))
    #   costs[8].append(sum(x != 8 for x in win))
    #   costs[9].append(sum(x != 9 for x in win))
    #   costs[10].append(sum(x != 10 for x in win))
    #   costs[11].append(sum(x != 11 for x in win))
    #   costs[12].append(sum(x != 12 for x in win))
    #   costs[13].append(sum(x != 13 for x in win))
    #   costs[14].append(sum(x != 14 for x in win))
    #   costs[15].append(sum(x != 15 for x in win))
    #   costs[16].append(sum(x != -1 for x in win))
    #   costs[17].append(sum(x != -2 for x in win))
    #   costs[18].append(sum(x != -3 for x in win))
      #
    max_costs = np.array([max(costs[i]) for i in range(8)])#
    max_cost = max(max_costs)
    signal = np.where(max_costs > 2)[0]
    signal = sum([2**i for i in signal])
    max_index = int(np.where(max_costs == max_cost)[0])
    fudge = costs[max_index].index(max_cost)
    for i in range(self.win_len + fudge):
      [j.popleft() for j in self.buffer]

    if signal == 255:   # If we get a charstart signal, reset byte!
      self.byte = []
      self.idlecount = 0
    elif signal == 254: # If we get a charend signal, reset byte!
      self.byte = []
      self.buffer = deque()
      self.quit()
    elif signal == 0:   # If we get no signal, increment idlecount if we are idling
      self.idlecount += 1
    else:   # If we got a signal, put it in the byte!
      self.byte.append(signal)
      self.idlecount = 0

    if self.idlecount > IDLE_LIMIT and self.idle_callback:
      self.idlecount = 0
      self.idle_callback()


    # # If we got a signal, put it in the byte!
    # if signal < 16:#
    #   self.byte.append(signal)
    #
    # # If we get a charstart signal, reset byte!
    # elif signal == 16:#
    #   signal = 's'
    #   self.byte = []
    #
    # # If we get a charend signal, reset byte!
    # elif signal == 17:#
    #   signal = 'e'
    #   self.byte = []
    #   self.buffer = deque()
    #   self.quit()
    #
    # # If we get no signal, increment idlecount if we are idling
    # if signal == 18:#
    #   self.idlecount += 1
    # else:
    #   self.idlecount = 0
    # if self.idlecount > IDLE_LIMIT and self.idle_callback:
    #   self.idlecount = 0
    #   self.idle_callback()
    #
    # if self.debug:
    #   if signal == 18:#
    #     signal = '-'
    #   sys.stdout.write('')
    #   sys.stdout.write('|{}|\n'.format(signal))
    #   sys.stdout.flush()

  # For now, just print out the characters as we go.
  def process_byte(self):
    if len(self.byte) != self.coder.expected_size():
      return
    byte = self.coder.get_decoded_bytes(self.byte)
    if byte is not None:
      self.receivebytes.append(byte)#
    self.byte = []

  def quit(self):
    self.do_quit = True

  # def printbuf(self, buf):
  #   newbuf = ['-' if x is -3 else x for x in buf]#
  #   newbuf = ['s' if x is -1 else x for x in newbuf]#
  #   newbuf = ['e' if x is -2 else x for x in newbuf]#
  #   print(repr(newbuf).replace(', ', ' ').replace('\'', ''))

def main():
  if len(sys.argv) == 2 and sys.argv[1] == 'debug':
    dec = Decoder(1)
  else:
    dec = Decoder(0)

if __name__ == "__main__":
  main()
