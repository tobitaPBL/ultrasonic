from ultrasonic_network import *
import sys

class Transporter:
  DEFAULT_CHARSET = "US-ASCII"
  def __init__(self):
    self.network = UltrasonicNetwork()
    self.header = {}
    self.bdata = None

  def send(self, message):
    # data部をencodeする
    self.__parse_send_data(message)

    # データをNetwork層へ渡す
    self.network.send(self.bdata)

  def set_header(self, key, value):
    self.header[key] = value

  def attach_receive_callback(self, func):
    self.receive_callback = func

  def parse_receive_data(self, data):
    # header算出のためにデフォルト文字コードでデコード
    # 改行2つがある位置
    # "\n".encode(self.DEFAULT_CHARSET)[0]
    # header = data.decode(data)
    # header.split("\n")
    pass

  def __parse_send_data(self, data):
    # FIXME: 文字以外のデータを処理する場合には修正
    if self.header["charset"] != None:
      charset = self.header["charset"]
    else:
      charset = self.DEFAULT_CHARSET
    print("charset: %s" % charset)
    data = "charset=%s\n\n%s\n" % (charset, data)
    print("transport data body:\n%s" % data)
    self.bdata = data.encode(charset)
