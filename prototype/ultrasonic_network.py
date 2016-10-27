
import sys

class UltrasonicNetwork:
  def __init__(self, version=1):
    self.version = version

  def send(self, data):
    data = bytearray(data)
    print("Decimalize: %s" % [int(d) for d in data])
    print("Binarize: %s" %  [format(int(d), 'b') for d in data])
    # ヘッダを含めて全てバイナリ化
    # Physical Layerへ渡す
    pass

  def attach_receive_callback(self, func):
    self.receive_callback = func
