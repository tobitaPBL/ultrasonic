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
    # format((1^255)+1,'b') # -1 (2の補数)
    # format((2^255)+1,'b') # -2 (2の補数)
    # multi = [str(10000000) for i in range(20)]
    # multiple = ''.join(flatten for inner in multi for flatten in inner)
    # binary = [multiple[i:i+8] for i in range(len(multiple)) if i % 8 == 0] # 2
    binform = ''.join(format((1^255)+1,'b') + self.coder.get_encoded_bytes_string(i) for i in somestring) + format((2^255)+1,'b') # 1
    binary = [binform[i:i+8] for i in range(len(binform)) if i % 8 == 0] # 2
    idxlist = []
    for i in binary:
        index = -1
        idx = list()
        while index != -2:
            index = i.find('1', index+1)
            if index == -1:
                break
            idx.append(index) # 3
        idxlist.append(idx) # 4

    tmpsound = np.empty((0,2250), float)
    soundlist = []
    for j in idxlist:
        tmpsound = np.vstack([self.getbit(CHAR_FREQ[i]) for i in j])
        soundlist = np.hstack((soundlist, sum(tmpsound)/len(j)))

    return soundlist

    # 1. 文字を8ビットに変換
    # 2. 8ビットずつに分解して配列に
    # 3. 1があるインデックスを取得して配列にまとめる
    # 4. その配列をリストに追加
    # → [[-1], [1,3,6], [-1], [3,7,8], [-1], [2,3], [-1], [1,6,7,8], [-1], [2], [-2]]
    # 5. リストの中の各配列に含まれる値をCHAR_FREQのインデックスとみて、getbitに投げて、足し合わせる。↓[1,3,6]の例
    # → getbit(CHAR_FREQ[1]) + getbit(CHAR_FREQ[3]) + getbit(CHAR_FREQ[6])

  def encode2wav(self, somestring, filename):
    soundlist = self.string2sound(somestring)
    # print("data:" + str(soundlist.astype(np.dtype('int16'))))
    wavfile.write(filename, RATE, soundlist.astype(np.dtype('int16')))

  def encodeplay(self, somestring):
    soundlist = self.string2sound(somestring)
    data = soundlist.astype(np.dtype('int16'))
    data_to_send = data.tobytes()
    # print("data:" + str(data))
    # print("len:" + str(len(data)))
    # print("type:" + str(type(data)))
    # num_frames = int(len(data) / (self.stream._channels * self.stream._format))
    # print("num_frames:" + str(num_frames))
    # stream = self.stream
    # print("channels:" + str(stream._channels))
    # print("rate:" + str(stream._rate))
    # print("format:" + str(stream._format))
    # print("frames_per_buffer:" + str(stream._frames_per_buffer))
    self.stream.write(data_to_send)

  def getbit(self, freq):
    music = []
    t = np.arange(0, BIT_DURATION, 1./RATE) #time

    x = np.sin(2*np.pi*freq*t) #generated signals
    x = [int(val * 32000) for val in x]

    sigmoid = [1 / (1 + np.power(np.e, -t)) for t in np.arange(-6, 6, 0.02)] #0.01
    sigmoid_inv = sigmoid[::-1]

    xstart = len(x) - len(sigmoid)
    for i in range(len(sigmoid)):
      x[xstart + i] *= sigmoid_inv[i]
      x[i] *= sigmoid[i]

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
  enc.encode2wav(args.text, args.filename)
