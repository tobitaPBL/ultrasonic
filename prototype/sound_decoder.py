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
    self.char_window = [deque() for i in range(len(CHAR_FREQ))]
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
      [self.char_window[CHAR_FREQ.index(i)].append(self.goertzel(i)) for i in CHAR_FREQ]
      self.base_window.append(self.goertzel(BASELINE))

      if len(self.base_window) >= self.med_len:
        self.calc_median()
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
    for i in range(len(self.char_window)):
        self.char_median[i] = np.median(self.char_window[i])
    self.base_median = np.median(self.base_window)
    [i.popleft() for i in self.char_window]
    self.base_window.popleft()

  # Determine the raw input signal of silences, 0s, 1s, 2s, and 3s. Insert into sliding window.
  def update_state(self, powerlist, base):
    # state = -3 # 無音

    # 各周波数のパワーがしきい値を超えているか判定
    pw = powerlist / base
    # print("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f" % (pw[0], pw[1], pw[2], pw[3], \
    #                                           pw[4], pw[5], pw[6], pw[7]))
    th = np.array(CHAR_THRESH)
    judge = pw > th

    if len(self.buffer[0]) >= self.buf_len:
      [i.popleft() for i in self.buffer]
    for i in range(8):
      self.buffer[i].append(judge[i])

  # Takes the raw noisy samples of -1/0/1 and finds the bitstream from it
  def signal_to_bits(self):
    if len(self.buffer[0]) < self.buf_len:
      return

    buf = [list(i) for i in self.buffer]

    costs = [[] for i in range(8)]#
    for i in range(self.win_fudge):
      win = [j[i : self.win_len + i] for j in buf]
      #
      for j in range(len(win)):
        costs[j].append(sum(win[j]))
    max_costs = np.array([max(costs[i]) for i in range(8)])#
    max_cost = max(max_costs)
    signal = np.where(max_costs > 2)[0]
    signal = sum([2**i for i in signal])
    max_index = int(np.where(max_costs == max_cost)[0][0])
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

  # For now, just print out the characters as we go.
  def process_byte(self):
    if len(self.byte) != self.coder.expected_size():
      return
    # byte = self.coder.get_decoded_bytes(self.byte)
    # if byte is not None:
    self.receivebytes.append(self.byte)#
    self.byte = []

  def quit(self):
    self.do_quit = True

def main():
  if len(sys.argv) == 2 and sys.argv[1] == 'debug':
    dec = Decoder(1)
  else:
    dec = Decoder(0)

if __name__ == "__main__":
  main()
