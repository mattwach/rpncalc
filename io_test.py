#!/usr/bin/python
"""Runs IO tests on RPN."""

import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO)

# Data Format
#
# Basically a single letter command, followed by tokens.
# Example
#
# I 5 5 +
# O x=10.0
#
# Some rules:
#  - Blank lines in the data are ignored
#  - The output is tokenized meaning that CRs and whitespace is ignored
#  - Prompts and intro messages are filtered away
#
# Commands:
#   # : A comment
#   I : Send some data to rpn
#   O : Expect this data to be returned
DATA = """
# Basic tests

I 5
O y = 5.0 |>

I -5
O x = 5.0 y = -5.0 |>

I 0
O 5.0 x = -5.0 y = 0.0 |>
"""

class Error(Exception):
  pass


class MaxLinesError(Error):
  pass


class OutputMismatch(Error):
  pass


class UnknownCommandError(Error):
  pass


def get_output(fout, max_chars=8192):
  line_data = []
  while max_chars > 0:
    fout.flush()
    line_data.append(fout.read(1))
    max_chars -= 1
    if line_data[-1] == '>' and line_data[-2] == '|':
      line = ''.join(line_data)
      data = line.strip().split()
      logging.debug('data -> %s', data)
      return data
  raise MaxLinesError('max_chars exceeded.')


def compare_output(line_number, expected, actual):
  if expected != actual:
    raise OutputMismatch('Line %d.  Expected: %s.  Got %s' % (
          line_number, expected, actual))


def parse_line(line_number, line, p):
  """Parses a single line of DATA."""

  line = line.strip()
  if not line:
    return

  if line.startswith('#'):
    return

  tokens = line.split()
  cmd = tokens[0]
  if cmd == 'I':
    p.stdin.write(' '.join(tokens[1:]))
    p.stdin.write('\n')
  elif cmd == 'O':
    compare_output(line_number, tokens[1:], get_output(p.stdout))
  else:
    raise UnknownCommandError('Unknown Command: %s' % line)

def main():
  p = subprocess.Popen(
    ['python', '-u', 'rpn'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE)

  get_output(p.stdout)

  for line_number, line in enumerate(DATA.split('\n')):
    try:
      parse_line(line_number + 1, line, p)
    except OutputMismatch as e:
      p.terminate()
      p.wait()
      sys.exit(e)

  # Wrap up
  p.terminate()
  p.wait()

if __name__ == '__main__':
  main()
