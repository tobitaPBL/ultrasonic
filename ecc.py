# -*- coding: utf-8 -*-

u"""誤り訂正
"""
import reedsolo

class Ecc(object):
    def __init__(self, nsym):
        self.nsym = nsym
        self.symbol_len = 8

    def expected_size(self):
        return self.nsym * self.symbol_len

    def get_encoded_bytes_string(self, target):
        encoded = self.encode(target)
        if type(encoded) == str:
            encoded = [ord(encoded)]
        s = ''
        for e in encoded:
            s = s + format(e, 'b').zfill(8)
        return s

    def split(self, li, num):
      res = []
      for bit_list in [li[i:i+num] for i in range(0,(self.nsym+1)*num, num)]:
        res.append(self.bit_list_to_int(bit_list))
      return res

    def bit_list_to_int(self, bit_list):
      ascii = 0
      for bit in bit_list:
        ascii = (ascii << 1) | bit
      return ascii

    def decode_from_bytes_string(self, target):
        sl = self.split(target, self.symbol_len)
        decoded = self.decode(sl)
        return chr(decoded[0]) if len(decoded) > 0 else ''

class EmptyEcc(Ecc):
    """ 何もしないEcc """
    def __init__(self):
        Ecc.__init__(self, 1)

    def encode(self, data):
        return data

    def decode(self, data):
        return data

class ReedSolomonEcc(Ecc):
    """ 何もしないEcc """
    def __init__(self, nsym):
        Ecc.__init__(self, nsym)
        self.coder = reedsolo.RSCodec(self.nsym)

    def expected_size(self):
        return (self.nsym + 1) * self.symbol_len

    def encode(self, data):
        return self.coder.encode(data)

    def decode(self, data):
        return self.coder.decode(data)

class OnebyteReedSolomonEcc(ReedSolomonEcc):
    def __init__(self):
        ReedSolomonEcc.__init__(self, 2)

    def encode(self, data):
        return self.coder.encode(data)

    def decode(self, data):
        try:
            return self.coder.decode(data)
        except reedsolo.ReedSolomonError as e:
            print("error:" + str(e))
            return bytearray()
