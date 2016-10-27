from ultrasonic_network import *

import sys

class Transporter:
  def __init__(self):
    self.network = UltrasonicNetwork()
    self.header = {}
    self.bdata = None

  def send(self, message):
    # data部をencodeする
    self.__parse_data(message)

    # データをNetwork層へ渡す
    self.network.send(self.bdata)

  def set_header(self, key, value):
    self.header[key] = value

  def attach_receive_callback(self, func):
    self.receive_callback = func

  def __parse_data(self, data):
    # FIXME: 文字以外のデータを処理する場合には修正
    if self.header["charset"] != None:
      charset = self.header["charset"]
    else:
      charset = "US-ASCII"
    print("charset: %s" % charset)
    self.bdata = data.encode(charset)
