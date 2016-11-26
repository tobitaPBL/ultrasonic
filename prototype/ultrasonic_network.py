from transducer import *
import sys
import threading

class UltrasonicNetwork:
  def __init__(self, version=1, mode=1, coder=EmptyEcc()):
    self.do_quit = False
    self.do_listen = False
    self.version = version
    self.transducer = Transducer(mode=mode, coder=coder)


  def send(self, data):
    u"""バイナリデータ送信
    @param data bytes or bytearray class data.
    """

    header_data = bytearray(self.__build_header(self.version))
    data = header_data + bytearray(data)
    print("Decimalize: %s" % [int(d) for d in data])
    print("Binarize: %s" %  [format(int(d), 'b') for d in data])
    # ヘッダを含めて全てバイナリ化
    # transducerへ渡す
    self.transducer.send(data)

  def write_to_file(self, data, filename):
    header_data = bytearray(self.__build_header(self.version))
    data = header_data + bytearray(data)
    self.transducer.write_to_file(data, filename)

  def start_listening(self):
    listen_thread = threading.Thread(target = self.listen)
    listen_thread.start()

  def stop_listening(self):
    self.do_listen = False

  def quit(self):
    self.do_quit = True

  def listen(self):
    u"""データ受信待機
    """
    self.do_listen = True
    while (True):
      if self.do_quit == True:
        break
      if self.do_listen == False:
        continue
      # transducerからバイナリ
      bdata = self.transducer.receive()
#       header = (16).to_bytes(1, "big")
#       bdata = bytearray(header) + bytearray(("""
# charset=UTF-8

# %s
#       """ % input()).encode("UTF-8"))
#       self.do_quit = True

      data = bytearray(bdata)
      # ヘッダ取得
      self.__parse_header(data)
      # データ部取得
      data_body = self.__parse_body(data)
      self.receive_callback(data_body)

  def attach_receive_callback(self, func):
    u"""データ受信時コールバック設定
    コールバック関数の引数は bytearray class.
    """
    self.receive_callback = func

  def __build_header(self, version):
    u"""
    |version(4bit)|padding(0, 4bit)|
    """
    binary_string = format(version, 'b').zfill(4).ljust(8, '0')
    return int(binary_string, 2).to_bytes(1, "big")

  def __parse_header(self, data):
      # version
      header = data[0]
      bin_version = format(header, 'b').rstrip("0")
      self.version = int(bin_version, 2)
      print("version : %s" % self.version)
      # データ長
      pass

  def __parse_body(self, data):
      # data body
      return data[1:]

