from sound_decoder import *
from sound_encoder import *
import sys
from ecc import OnebyteReedSolomonEcc, EmptyEcc

class Transducer:
  def __init__(self, mode=1, debug=0, coder=EmptyEcc()):
    u"""
    @param mode = 1 : encoder , mode = 2 : decoder
    """
    if (mode == 1):
      self.enc = Encoder(coder=coder)
      self.dec = None
    else:
      self.enc = None
      self.dec = Decoder(debug, coder=coder)

  def send(self, byte_data):
    u"""
    @param byte_data bytearray class data.
    """
    if (self.enc == None):
      raise Exception("Invalid tranceducer mode.")
    # print("Transducer::Decimalize: %s" % [int(d) for d in byte_data])
    # print("Transducer::Binarize: %s" %  [format(int(d), 'b') for d in byte_data])
    self.enc.encodeplay(byte_data)
    # self.enc.encode2wav(byte_data)

  def write_to_file(self, byte_data, filename):
    u"""
    @param byte_data bytearray class data.
    """
    if (self.enc == None):
      raise Exception("Invalid tranceducer mode.")
    self.enc.encode2wav(byte_data, filename)

  def receive(self):
    u"""
    @return bytearray class data.
    """
    if (self.dec == None):
      raise Exception("Invalid tranceducer mode.")
    return self.dec.listen()

def main():
  if len(sys.argv) >= 2 and sys.argv[1] == 'enc':
    tranceducer = Transducer(mode=1)
    tranceducer.send(sys.argv[2].encode("UTF-8"))
  else:
    tranceducer = Transducer(mode=2, debug=1)
    while(True):
      data = tranceducer.receive()
      # print(data.decode("UTF-8"))
      print("Transducer::Decode Decimalize: %s" % [int(d) for d in data])
      print("Transducer::Decode Binarize: %s" %  [format(int(d), 'b') for d in data])

if __name__ == "__main__":
  main()
