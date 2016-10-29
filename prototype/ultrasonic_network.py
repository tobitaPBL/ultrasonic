from transducer import *
import sys
import threading

class UltrasonicNetwork:
  def __init__(self, version=1):
    self.version = version


  def send(self, data):
    u"""バイナリデータ送信
    @param data bytes or bytearray class data.
    """

    data = bytearray(data)
    print("Decimalize: %s" % [int(d) for d in data])
    print("Binarize: %s" %  [format(int(d), 'b') for d in data])
    # ヘッダを含めて全てバイナリ化
    # transducerへ渡す
    transducer.send(data)
    pass

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
      bdata = None
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

  def __parse_header(self, data):
      # version
      # データ長
      pass

  def __parse_body(self, data):
      # data body
      return data

