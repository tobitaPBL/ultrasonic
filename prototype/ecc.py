# -*- coding: utf-8 -*-

u"""誤り訂正
"""
import reedsolo

class Ecc(object):
    def __init__(self, nsym):
        self.nsym = nsym
        self.symbol_len_per_byte = 2

    def expected_size(self):
        u"""想定する処理単位のサイズを返す。"""
        return self.nsym * self.symbol_len_per_byte

    def get_encoded_bytes_string(self, target):
        u"""エンコードされたバイト文字列を返す"""
        pass

    def get_decoded_bytes(self, target):
        u"""デコードされたバイト文字列を返す"""
        pass

class EmptyEcc(Ecc):
    """ 何もしないEcc """
    def __init__(self):
        Ecc.__init__(self, 1)

    def get_encoded_bytes_string(self, target):
        return format(int(target), 'b').zfill(8)

    def get_decoded_bytes(self, target):
        ascii = int(''.join([format(i, 'b').zfill(4) for i in target]), 2)#
        return ascii

class ReedSolomonEcc(Ecc):
    """ RS符号 """
    def __init__(self, nsym):
        Ecc.__init__(self, nsym)
        self.coder = reedsolo.RSCodec(self.nsym)

    def expected_size(self):
        return (self.nsym + 1) * self.symbol_len_per_byte

    def encode(self, data):
        return self.coder.encode(data)

    def decode(self, data):
        return self.coder.decode(data)

class OnebyteReedSolomonEcc(ReedSolomonEcc):
    """ 1バイトを対象としたRS符号 """
    def __init__(self):
        ReedSolomonEcc.__init__(self, 2)

    def get_encoded_bytes_string(self, target):
        encoded = self.encode([target])
        s = ''
        for e in encoded:
            s = s + format(int(e), 'b').zfill(8)
        return s

    def decode(self, data):
        try:
            return self.coder.decode(data)
        except reedsolo.ReedSolomonError as e:
            print("error:" + str(e))
            return bytearray() # empty bytearray

    def get_decoded_bytes(self, target):
        paired = [target[i:i + 2] for i in range(0, len(target), 2)]
        sl = [((en[0] << 4) + en[1])for en in paired]
        decoded = self.decode(sl)
        return int(decoded[0]) if len(decoded) > 0 else None
