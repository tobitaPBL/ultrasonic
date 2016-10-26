from ultrasonic_network import *

import sys

class Transporter:
  def __init__(self):
    self.network = UltrasonicNetwork()
    self.header = {}
    print("init Transporter")

  def send(self, message):
    # data部をencodeする
    # データをNetwork層へ渡す
    pass

  def set_header(self, key, value):
    self.header[key] = value

  def attach_receive_callback(self, func):
    self.receive_callback = func
