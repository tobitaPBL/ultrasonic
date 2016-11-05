from transporter import *
import sys
import argparse

class Sender:
  def __init__(self):
    self.transporter = Transporter()
    self.transporter.set_header("charset", "UTF-8") # TODO:必要？ unicodeだけで良いのかも？

  def send(self, message):
    self.transporter.send(message)

  def write_to_file(self, message, filename):
    self.transporter.write_to_file(message, filename)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="sender")
  parser.add_argument('text', help="The text to send")
  parser.add_argument('-f', '--filename', help="The file to generate.", default=None)
  args = parser.parse_args()

  sender = Sender()
  if args.filename:
    sender.write_to_file(args.text, args.filename)
  else:
    sender.send(args.text)
