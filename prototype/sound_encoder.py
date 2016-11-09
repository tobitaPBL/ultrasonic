import sys
import argparse
import numpy as np
import pyaudio
from scipy.io import wavfile

from constants import *
from ecc import OnebyteReedSolomonEcc, EmptyEcc


class Encoder:
  def __init__(self, coder=EmptyEcc()):
    self.num_channels = 1
    self.bits_per_sample = 16
    self.amplitude = 0.5

    self.p = pyaudio.PyAudio()
    self.stream = self.p.open(format = pyaudio.paInt16,
                  channels = 1,
                  rate = RATE,
                  output = True,
                  frames_per_buffer = AUDIOBUF_SIZE)
    self.coder = coder

  def string2sound(self, somestring):
    binform = ''.join('-001' + self.coder.get_encoded_bytes_string(i) for i in somestring) + '-010'#
    # 2進数にした後、2ビットずつに分割してそれぞれを10進数に変換
    multiple = [int(binform[i:i+4], 2) for i in range(len(binform)) if i % 4 == 0]#
    soundlist = np.hstack([self.getbit(CHAR_FREQ[i+2]) for i in multiple])
    return soundlist

  def encode2wav(self, somestring, filename):
    soundlist = self.string2sound(somestring)
    wavfile.write(filename, RATE,soundlist.astype(np.dtype('int16')))

  def encodeplay(self, somestring):
    soundlist = self.string2sound(somestring)
    self.stream.write(soundlist.astype(np.dtype('int16')))

  def getbit(self, freq):
    music = []
    t = np.arange(0, BIT_DURATION, 1./RATE) #time

    x = np.sin(2*np.pi*freq*t) #generated signals
    x = [int(val * 32000) for val in x]

    sigmoid = [1 / (1 + np.power(np.e, -t)) for t in np.arange(-6, 6, 0.02)] #0.01
    sigmoid_inv = sigmoid[::-1]

    xstart = len(x) - len(sigmoid)
    for i in range(len(sigmoid)):
      x[xstart + i] = x[xstart + i] * sigmoid_inv[i]
      x[i] = x[i] * sigmoid[i]

    music = np.hstack((music,x))
    return music

  def quit(self):
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="sound_encoder")
  parser.add_argument('text', help="The text to encode")
  parser.add_argument('filename', help="The file to generate.")
  args = parser.parse_args()

  enc = Encoder()
  enc.encode2play(args.text)
