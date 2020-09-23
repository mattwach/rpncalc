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
# --- Basic tests ---

  I 5
  O y = 5.0 |>

  I -5
  O x = 5.0 y = -5.0 |>

  I 0
  O 5.0 x = -5.0 y = 0.0 |>

  I D 5 5 +
  O y = 10.0 |>

  I D 5 5 + 2 /
  O y = 5.0 |>

  I D 3 3 * 4 4 * + sqrt
  O y = 5.0 |>

  I D 3 2 ** 4 2 ** + sqrt
  O y = 5.0 |>

  I D 3 d * 4 d * + sqrt
  O y = 5.0 |>

  I D 5 2 ** v:pi *
  O y = 78.5398163397 |>

  I D -12.34e6
  O y = -12340000.0 |>

  I D 12.34e-6
  O y = 1.234e-05 |>

# --- Integers ---

  I D mixed 1 2.0
  O x = 1 y = 2.0 |mix|>

  I +
  O y = 3.0 |mix|>

  I D 5 2 /
  O y = 2 |mix|>

  I D mixed 1 2.0 floats
  O x = 1 y = 2.0 |>

  I D 5.0 t
  O y = 5 |mix|>

  I t
  O y = 5.0 |mix|>

# --- Complex Numbers ---

  I floats D -1+5i
  O y = -1.0+5.0i |>

  I D 3.7-2.1j
  O y = 3.7-2.1j |>

# --- Trig functions, in radians ---

  I D normal 1 sin
  O y = 0.841470984808 |>

# --- Conversions ---

  I D 10 in>cm
  O y = 25.4 |>

  I D 25.4 cm>in
  O y = 10.0 |>

  I D 1 mi*mi>acres
  O y = 640.00000038 |>

  I D 1 pint>tsp
  O y = 96.000000073 |>

  I D 10 n*m>in*lbs
  O y = 88.5043147656 |>

  I D 4 ft>yards 25 25 * * yard*yard*yard>gallon
  O y = 168311.688488 |>

# --- Time Tests ---

  I D 12/25 12/24 -
  O y = 86400.0 | 1d |time|>

  I D 1/14/2010
  O y = 1263456000.0 | 01/14/2010 (Thu) |time|>

  I D 07/30/2006+16:00:00
  O y = 1154300400.0  | 07/30/2006+16:00:00 (Sun) |time|>

  I D now
  A

  I D today
  A

# -- Duration Tests ---

  I normal D 20:00 5000 meters>miles /
  O y = 386.24256 | 06:26 |dur|>

  I D 4d
  O y = 345600.0 | 4d |dur|>

  I D -4d
  O y = -345600.0 | -4d |dur|>

  I D 1d14:23:12
  O y = 138192.0 | 1d14:23:12 |dur|>

  I D 534:12:00
  O y = 1923120.0 | 22d06:12:00 |dur|>

  I D 536:45
  O y = 32205.0 | 08:56:45 |dur|>

# --- Money ---

  I normal D $ 1.24 5.34 6.78 sum 1.09 *
  O y = 14.5624 | $14.56 |$|>

  I D cent -4234 -1215 -500 -2738 50000 sum
  O y = 41313.0 | $413.13 |cent|>

# --- Hexadecimal ---

  I normal D 0x80
  O y = 128 | 0x80 |hex|mix|>

  I D -0x1234
  O y = -4660 | -0x1234 |hex|mix|>

# --- Binary ---

  I normal D 0b1001
  O y = 9 | 0b1001 |bin|mix|>

# --- Stack Management ---

  I normal floats D 1 2 3 4 5 6 7 8 9 10 11
  O ...  2.0  3.0  4.0  5.0  6.0  7.0  8.0  9.0 x = 10.0 y = 11.0 |>

  I .
  O ...  2.0  3.0  4.0  5.0  6.0  7.0  8.0  9.0 x = 10.0 y = 11.0 |>

  I ..
  O s11 = 1.0 s10 = 2.0 s9 = 3.0 s8 = 4.0 s7 = 5.0 s6 = 6.0 s5 = 7.0 s4 = 8.0 s3 = 9.0 s2 = 10.0 s1 = 11.0 |>

  I D 1 d
  O x = 1.0 y = 1.0 |>

  I D 1 2 y
  O y = 1.0 |>

  I D y
  E While parsing y: Not Enough Stack Arguments !!
  O |>

  I D 1 2 3 R
  O 3.0 x = 2.0 y = 1.0 |>

  I D R
  O |>

  I D 1 2 3 s
  O 1.0 x = 3.0 y = 2.0 |>

  I D 1 s
  E While parsing s: Not Enough Stack Arguments !!
  O |>

  I D 1 2 3 4 rd
  O 4.0 1.0 x = 2.0 y = 3.0 |>

  I ru
  O 1.0 2.0 x = 3.0 y = 4.0 |>

# --- Undo and Redo ---

  I normal D 1 2
  O x = 1.0 y = 2.0 |>

  I 3 4
  O 1.0 2.0 x = 3.0 y = 4.0 |>

  I 5 6
  O 1.0 2.0 3.0 4.0 x = 5.0 y = 6.0 |>

  I X
  O |>

  I u
  O 1.0 2.0 3.0 4.0 x = 5.0 y = 6.0 |>

  I u
  O 1.0 2.0 x = 3.0 y = 4.0 |>

  I u
  O x = 1.0 y = 2.0 |>

  I r
  O 1.0 2.0 x = 3.0 y = 4.0 |>

  I r
  O 1.0 2.0 3.0 4.0 x = 5.0 y = 6.0 |>

  I r
  O |>

  I r
  E While parsing r: No Redo History Available !!
  O |>
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
    if ((line_data[-1] == '>' and line_data[-2] == '|') or
        (line_data[-1] == '!' and line_data[-2] == '!')):
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
  elif cmd == 'E':
    compare_output(line_number, tokens[1:], get_output(p.stderr))
  elif cmd == 'A':
    get_output(p.stdout)
  else:
    raise UnknownCommandError('Unknown Command: %s' % line)

def main():
  p = subprocess.Popen(
      ['python', '-u', 'rpn'],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)

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
