from transporter import *
import sys
import argparse

class Sender:
  def __init__(self):
    self.transporter = Transporter()
    self.transporter.set_header("content-type", "text/plain; charset=US-ASCII")

  def send(self, message):
    self.transporter.send(message)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="sender")
  parser.add_argument('text', help="The text to send")
  args = parser.parse_args()

  sender = Sender()
  sender.send(args.text)
