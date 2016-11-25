# -*- coding: utf-8 -*-

u"""Transducer を介したエンコード・デコードテスト
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
            # print("Transducer::Decode Decimalize: %s" % [int(d) for d in data])
            # print("Transducer::Decode Binarize: %s" % [format(int(d), 'b') for d in data])
            data_string = data_to_ascii_string(data)
            print("Decoded: %s" % data_string)
            operate_keyboard_if_necessary(data_string)


def write_by_transducer(coder, target_str, file_name):
    print("Encoding...")
    tranceducer = Transducer(mode=1, debug=0, coder=coder)
    target_list = [ord(t) for t in target_str]
    tranceducer.write_to_file(target_list, file_name)


def send_by_transducer(coder, target_str):
    print("Encoding...")
    tranceducer = Transducer(mode=1, debug=0, coder=coder)
    target_list = [ord(t) for t in target_str]
    tranceducer.send(target_list)


if __name__ == "__main__":
    u"""以下の 1から6のうち、動かしたい機能のコメントを外し、それ以外の行はコメントにする。
    """

    # ---------------------------------------------------------
    # 受信 -> デコード
    # ---------------------------------------------------------
    # 1. RS符号での復号を行うデコーダースレッドを起動
    launch_decoder_through_transducer(OnebyteReedSolomonEcc())
    # 誤り訂正なしでデコーダースレッドを起動
    # 2. launch_decoder_through_transducer(EmptyEcc())

    # ---------------------------------------------------------
    # エンコード -> 保存
    # ---------------------------------------------------------
    # 3. RS符号化を行いエンコードして保存
    # write_by_transducer(OnebyteReedSolomonEcc(), "bbb", "back_encoded.wav")
    # 4. 誤り訂正なしでエンコードして保存
    # write_by_transducer(EmptyEcc(), "TakuyaIwanaga", "iwanaga_empty.wav")

    # ---------------------------------------------------------
    # エンコード -> ストリーム送信
    # ---------------------------------------------------------
    # 5. RS符号化しストリーム送信
    # send_by_transducer(OnebyteReedSolomonEcc(), "abcdefg")
    # 6. 誤り訂正なしでストリーム送信
    # send_by_transducer(EmptyEcc(), "abcdefg")
