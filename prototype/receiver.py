from transporter import *
from ultrasonic_network import *
import sys
import argparse

class Receiver:
  def __init__(self):
    self.network = UltrasonicNetwork()
    self.transporter = Transporter()
    self.transporter.set_header("charset", "UTF-8") # TODO:必要？ unicodeだけで良いのかも？

  def parse_data(self, data):
    message = self.transporter.parse_receive_data(data)
    print("message is : %s" % message)

  def listen(self):
    self.network.attach_receive_callback(self.parse_data)
    self.network.start_listening()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="sender")
  args = parser.parse_args()

  receicer = Receiver()
  receicer.listen()