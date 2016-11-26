from ultrasonic_network import *
import sys

class Transporter:
  DEFAULT_CHARSET = "US-ASCII"
  def __init__(self, coder=EmptyEcc()):
    self.network = UltrasonicNetwork(coder=coder)
    self.header = {}
    self.bdata = None

  def send(self, message):
    # data部をencodeする
    self.__parse_send_data(message)

    # データをNetwork層へ渡す
    self.network.send(self.bdata)

  def write_to_file(self, message, filename):
    # data部をencodeする
    self.__parse_send_data(message)

    # データをNetwork層へ渡す
    self.network.write_to_file(self.bdata, filename)

  def set_header(self, key, value):
    self.header[key] = value

  def attach_receive_callback(self, func):
    self.receive_callback = func

  def parse_receive_data(self, data):
    u"""
    @return encoded data.
    """
    # header算出のためにデフォルト文字コードでデコード
    charset = self.DEFAULT_CHARSET

    LF = "\n".encode(self.DEFAULT_CHARSET)[0]

    count = 0
    # 改行2つがある位置
    index = 0
    for index, value in enumerate(data):
      if value == LF:
        count += 1
      else:
        count = 0
      if count == 2:
        break

    headers = data[:index+1].decode(self.DEFAULT_CHARSET)
    for header in headers.split("\n"):
      if header.strip():
        key, value = header.strip().split("=")
        if key == "charset":
          charset = value

    return data[index+1:].decode(charset)

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

if __name__ == "__main__":
  transporter = Transporter()
  data = transporter.parse_receive_data("""
charset=UTF-8

あいうえお
""".encode("UTF-8"))
  print(data)