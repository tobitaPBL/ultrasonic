# -*- coding: utf-8 -*-

u"""次へ前へキーを送信してスライドを進める
"""

from ecc import EmptyEcc, OnebyteReedSolomonEcc
from transducer import Transducer
import pyautogui

__author__ = 'egg'


def data_to_ascii_string(target):
    return "".join([chr(int(format(int(d), 'b'), 2)) for d in target])


def operate_keyboard_if_necessary(data_string):
    key = "down" if "n" in data_string else "up" if "b" in data_string else ""
    if len(key) > 0:
        pyautogui.press(key)


def launch_decoder_through_transducer(coder):
    print("Listening...")
    tranceducer = Transducer(mode=2, debug=0, coder=coder)
    while (True):
        data = tranceducer.receive()
        if len(data) > 0:
            print("Transducer::Decode Decimalize: %s" % [int(d) for d in data])
            print("Transducer::Decode Binarize: %s" % [format(int(d), 'b') for d in data])
            data_string = data_to_ascii_string(data)
            print("Decoded: %s" % data_string)
            operate_keyboard_if_necessary(data_string)


def encode_by_transducer(coder, target_str, file_name):
    print("Encoding...")
    tranceducer = Transducer(mode=1, debug=0, coder=coder)
    target_list = [ord(t) for t in target_str]
    tranceducer.write_to_file(target_list, file_name)

if __name__ == "__main__":
    # RS符号での復号を行うデコーダースレッドを起動
    launch_decoder_through_transducer(OnebyteReedSolomonEcc())
    # 誤り訂正なしでデコーダースレッドを起動
    # launch_decoder_through_transducer(EmptyEcc())

    # RS符号化を行いエンコードして保存
    # encode_by_transducer(OnebyteReedSolomonEcc(), "bbb", "back_encoded.wav")
    # 誤り訂正なしでエンコードして保存
    # encode_by_transducer(EmptyEcc(), "TakuyaIwanaga", "iwanaga_empty.wav")
