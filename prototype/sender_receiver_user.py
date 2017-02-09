# -*- coding: utf-8 -*-

u"""Sender, Receiver を介したエンコード・デコードテスト
"""

from ecc import EmptyEcc, OnebyteReedSolomonEcc
from receiver import Receiver
from sender import Sender
import argparse

__author__ = 'egg'

def launch_receiver(coder):
    receiver = Receiver(coder=coder)
    receiver.listen()

def send_by_sender(coder, target_str):
    sender = Sender(coder=coder)
    sender.send(target_str)


if __name__ == "__main__":
    u"""以下の 1から4のうち、動かしたい機能のコメントを外し、それ以外の行はコメントにする。
    """
    parser = argparse.ArgumentParser(prog="sender_receiver_user")
    parser.add_argument('text', help="The text to send")
    args = parser.parse_args()
    # ---------------------------------------------------------
    # 受信
    # ---------------------------------------------------------
    # 1. RS符号での復号を行うlisten
    # launch_receiver(OnebyteReedSolomonEcc())
    # 2. 誤り訂正なしでlisten
    # launch_receiver(EmptyEcc())

    # ---------------------------------------------------------
    # ストリーム送信
    # ---------------------------------------------------------
    # 3. RS符号化しストリーム送信
    # send_by_sender(OnebyteReedSolomonEcc(), args.text)
    # 4. 誤り訂正なしでストリーム送信
    send_by_sender(EmptyEcc(), args.text)
