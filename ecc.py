# -*- coding: utf-8 -*-

u"""誤り訂正
"""
import reedsolo

class Ecc(object):
    def __init__(self, nsym):
        self.nsym = nsym

    def get_encoded_bytes_string(self, target):
        encoded = self.encode(target)
        s = ''
        for bb in encoded:
            s = s + format(bb, 'b').zfill(8)
        return s

    def split(self, li, num):
      res = []
      for bit_list in [li[i:i+num] for i in range(0,(self.nsym+1)*num, num)]:
        res.append(self.intint(bit_list))
      return res

    def intint(self, bit_list):
      ascii = 0
      for bit in bit_list:
        ascii = (ascii << 1) | bit
      return ascii

    def decode_from_bytes_string(self, target):
        sl = self.split(target, 8)
        decoded = self.decode(sl)
        return chr(decoded[0])

class ReadSolomonEcc(Ecc):
    def __init__(self, nsym):
        Ecc.__init__(self, nsym)
        self.coder = reedsolo.RSCodec(self.nsym)

    def encode(self, data):
        return self.coder.encode(data)

    def decode(self, data):
        return self.coder.decode(data)

class OnebyteReadSolomonEcc(ReadSolomonEcc):
    def __init__(self):
        Ecc.__init__(self, 2)
        self.coder = reedsolo.RSCodec(self.nsym)

    def encode(self, data):
        return self.coder.encode(data)

    def decode(self, data):
        return self.coder.decode(data)
