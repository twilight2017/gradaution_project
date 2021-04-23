import sys

class Logger(object):
    def __init__(self,filename):
        self.terminal = sys.stout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass