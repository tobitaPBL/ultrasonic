import sys

class Transducer:
  def __init__(self):
      pass
  def send(self, byte_data):
    u"""
    @param byte_data bytearray class data.
    """
    print("Transducer::Decimalize: %s" % [int(d) for d in byte_data])
    print("Transducer::Binarize: %s" %  [format(int(d), 'b') for d in byte_data])
    pass
  def receive(self):
    u"""
    @return bytearray class data.
    """
    pass