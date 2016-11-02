from sound_decoder import *
from sound_encoder import *
import sys

class Transducer:
  def __init__(self, mode=1):
    u"""
    @param mode = 1 : encoder , mode = 2 : decoder
    """
    if (mode == 1):
      self.enc = Encoder()
      self.dec = None
    else:
      self.enc = None
      self.dec = Decoder()

  def send(self, byte_data):
    u"""
    @param byte_data bytearray class data.
    """
    if (self.enc == None):
      raise Exception("Invalid tranceducer mode.")
    print("Transducer::Decimalize: %s" % [int(d) for d in byte_data])
    print("Transducer::Binarize: %s" %  [format(int(d), 'b') for d in byte_data])
    pass
  def receive(self):
    u"""
    @return bytearray class data.
    """
    if (self.dec == None):
      raise Exception("Invalid tranceducer mode.")
