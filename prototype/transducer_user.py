# -*- coding: utf-8 -*-

u"""Transducer を介したエンコード・デコードテスト
"""

from ecc import EmptyEcc, OnebyteReedSolomonEcc
from transducer import Transducer

__author__ = 'egg'

def data_to_ascii_string(target):
    return "".join([chr(int(format(int(d), 'b'), 2)) for d in target])

def launch_decoder_through_transducer(coder):
    print("Listening...")
    tranceducer = Transducer(mode=2, debug=0, coder=coder)
    while (True):
        data = tranceducer.receive()
        if len(data) > 0:
            print("Transducer::Decode Decimalize: %s" % [int(d) for d in data])
            print("Transducer::Decode Binarize: %s" % [format(int(d), 'b') for d in data])
            print("Decoded: %s" % data_to_ascii_string(data))

def encode_by_transducer(coder, target_str, file_name):
    print("Encoding...")
    tranceducer = Transducer(mode=1, debug=0, coder=coder)
    target_list = [ord(t) for t in target_str]
    tranceducer.write_to_file(target_list, file_name)

if __name__ == "__main__":
    # RS符号での復号を行うデコーダースレッドを起動
    # launch_decoder_through_transducer(OnebyteReedSolomonEcc())
    # 誤り訂正なしでデコーダースレッドを起動
    launch_decoder_through_transducer(EmptyEcc())

    # RS符号化を行いエンコードして保存
    # encode_by_transducer(OnebyteReedSolomonEcc(), "hogehoge", "hogera_org2.wav")
    # 誤り訂正なしでエンコードして保存
    #encode_by_transducer(EmptyEcc(), "hogehoge", "hogera_org2.wav")
