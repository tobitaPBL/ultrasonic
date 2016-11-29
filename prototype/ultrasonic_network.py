from transducer import *
import sys
import threading

class UltrasonicNetwork:
  def __init__(self, version=1, mode=1, coder=EmptyEcc()):
    self.do_quit = False
    self.do_listen = False
    self.version = version
    self.payload_length = None
    self.payload_checksum = None
    self.header_chechsum = None
    self.transducer = Transducer(mode=mode, coder=coder)


  def send(self, data):
    u"""バイナリデータ送信
    @param data bytes or bytearray class data.
    """

    header_data = bytearray(self.__build_header(self.version, data))
    data = header_data + bytearray(data)
    print("Decimalize: %s" % [int(d) for d in data])
    print("Binarize: %s" %  [format(int(d), 'b') for d in data])
    # ヘッダを含めて全てバイナリ化
    # transducerへ渡す
    self.transducer.send(data)

  def write_to_file(self, data, filename):
    header_data = bytearray(self.__build_header(self.version, data))
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
      if len(data) > 0:
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

  def __build_header(self, version, data):
    u"""
    @param data bytes or bytearray class data.
    version(4bit)
    payload length(12bit)
    payload checksum(8bit)
    header checksum(8bit)
    """
    payload_length = len(data)
    payload_checksum = self.__calc_checksum(data)
    header_chechsum = 0

    temp_binary = self.__build_header_binary(version, \
                                             payload_length, \
                                             payload_checksum, \
                                             header_chechsum)
    header_chechsum = self.__calc_checksum(temp_binary)

    print("version          : %d" % version)
    print("payload_length   : %d" % payload_length)
    print("payload_checksum : %d" % payload_checksum)
    print("header_chechsum  : %d" % header_chechsum)

    return self.__build_header_binary(version, \
                                      payload_length, \
                                      payload_checksum, \
                                      header_chechsum)

  def __build_header_binary(self, version, payload_length, payload_checksum, header_chechsum):
    binary_string = format(version, 'b').zfill(4) \
                  + format(payload_length, 'b').zfill(12) \
                  + format(payload_checksum, 'b').zfill(8) \
                  + format(header_chechsum, 'b').zfill(8)
    return int(binary_string, 2).to_bytes(4, "big")

  def __calc_checksum(self, data):
    u"""
    @param data bytes or bytearray class data.
    """
    checksum = 0
    for b in data:
      # 1の補数を足す
      checksum += (255 - b)
      if checksum > 255:
        # 補数の和なので繰り上げはカットして1足すために255を引く
        checksum -= 255
    return checksum

  def __parse_header(self, data):
    header = data[0:4]
    # 全体を1つの整数にする
    concat = sum([b << ((3 - index) * 8) for index, b in enumerate(header)])

    # version(上位4bitを取得)
    self.version          = concat >> 28 & 0b1111
    # データ長(上位16bit中の下位12bitを取得)
    self.payload_length   = concat >> 16 & 0b111111111111
    # データchecksum(上位24bit中の下位8bitを取得)
    self.payload_checksum = concat >> 8  & 0b11111111
    # ヘッダchecksum(下位8bitを取得)
    self.header_chechsum  = concat       & 0b11111111
    print("version          : %d" % self.version)
    print("payload_length   : %d" % self.payload_length)
    print("payload_checksum : %d" % self.payload_checksum)
    print("header_chechsum  : %d" % self.header_chechsum)

    temp_binary = self.__build_header_binary(self.version, \
                                             self.payload_length, \
                                             self.payload_checksum, \
                                             0)
    calcurated_header_checksum = self.__calc_checksum(temp_binary)
    if calcurated_header_checksum != self.header_chechsum:
      raise "Invalid header checksum"

    calcurated_payload_checksum = self.__calc_checksum(data)
    if calcurated_payload_checksum != self.payload_checksum:
      raise "Invalid payload checksum"

    if len(data) != self.payload_length + 4:
      raise "Invalid payload length"

  def __parse_body(self, data):
      # data body
      return data[4:]

