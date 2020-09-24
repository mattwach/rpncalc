#!/usr/bin/python
"""Runs IO tests on RPN."""

import logging
import select
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

# --- Operators ---

  I D 4 5 +
  O y = 9.0 |>

  I D 4 5 -
  O y = -1.0 |>

  I D 4 5 *
  O y = 20.0 |>

  I D 4 5 /
  O y = 0.8 |>

# --- Logic ---

  I D 0xF0 0x7F &
  O y = 112 | 0x70 |hex|mix|>

  I D 0x80 0x08 |
  O y = 136 | 0x88 |hex|mix|>

  I D 0x80 0xFF ^
  O y = 127 | 0x7F |hex|mix|>

  I D 0x80 4 >>
  O y = 8 | 0x08 |hex|mix|>

  I D 0x08 4 <<
  O y = 128 | 0x80 |hex|mix|>

# --- Scientific ---

  I normal floats D -12.34e6
  O y = -12340000.0 |>

  I D 12.34e-6
  O y = 1.234e-05 |>

  I D 100 log10
  O y = 2.0 |>

  I D v:e 5 ** log
  O y = 5.0 |>

  I D 5 sq
  O y = 25.0 |>

  I D 25 sqrt
  O y = 5.0 |>

  I D 10 3 %
  O y = 1.0 |>

  I D 5 !
  O y = 120.0 |>

  I D 10 inv
  O y = 0.1 |>

  I D 1234 neg
  O y = -1234.0 |>

  I D -1234 abs
  O y = 1234.0 |>

  I D 5 3 **
  O y = 125.0 |>

# --- Trig functions, in radians ---

  I D normal v:pi 6 / sin
  O y = 0.5 |>

  I D v:pi 3 / cos
  O y = 0.5 |>

  I D v:pi 4 / tan
  O y = 1.0 |>

  I D 1 asin v:pi 2 / -
  O y = 0.0 |>

  I D 0 acos v:pi 2 / -
  O y = 0.0 |>

  I D 1 atan v:pi 4 / -
  O y = 0.0 |>

# --- Trig functions, in degrees ---

  I D deg 30 sin
  O y = 0.5 |deg|>

  I D 60 cos
  O y = 0.5 |deg|>

  I D 45 tan
  O y = 1.0 |deg|>

  I D 1 asin
  O y = 90.0 |deg|>

  I D 0 acos
  O y = 90.0 |deg|>

  I D 1 atan 
  O y = 45.0 |deg|>

  I rad
  A

# --- Simple Clipboard ---

  I D 123 c v v
  O 123.0 x = 123.0 y = 123.0 |>

  I D 123 456 x 789 v
  O 123.0 x = 789.0 y = 456.0 |>

# --- Stack Clipboard ---

  I D 1 2 3 4 1 pc v
  O 1.0 2.0 3.0 x = 4.0 y = 3.0 |>

  I D 1 2 3 4 1 px v
  O 1.0 2.0 x = 4.0 y = 3.0 |>

  I D 1 2 3 4 c 2 pv
  O 1.0 2.0 4.0 x = 3.0 y = 4.0 |>

# --- Variable Clipboard ---

  I D 1234 c:myvar 0 v:myvar
  O 1234.0 x = 0.0 y = 1234.0 |>

  I D 5678 x:myvar 0 v:myvar
  O x = 0.0 y = 5678.0 |>

  I D l:v
  O c = 299792458.0 e = 2.71828182846 myvar = 5678.0 pi = 3.14159265359 |>

# --- Full Stack Clipboard ---

  I D 1 2 3 C
  O 1.0 x = 2.0 y = 3.0 |>

  I D V
  O 1.0 x = 2.0 y = 3.0 |>

  I D 4 5 6 X
  O |>

  I V
  O 4.0 x = 5.0 y = 6.0 |>

# --- Integers ---

  I D normal mixed 1 2.0
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

# --- Time Tests ---

  I D 1/14/2010
  O y = 1263456000.0 | 01/14/2010 (Thu) |time|>

  I D 07/30/2006+16:00:00
  O y = 1154300400.0  | 07/30/2006+16:00:00 (Sun) |time|>

  I D now
  A

  I D today
  A

# -- Duration Tests ---

  I D normal 4d
  O y = 345600.0 | 4d |dur|>

  I D -4d
  O y = -345600.0 | -4d |dur|>

  I D 1d14:23:12
  O y = 138192.0 | 1d14:23:12 |dur|>

  I D 534:12:00
  O y = 1923120.0 | 22d06:12:00 |dur|>

  I D 536:45
  O y = 32205.0 | 08:56:45 |dur|>

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

# --- Sourcing An External File ---

  I D s:sample.txt
  O y = 9.0 |>

# --- Statistics ---

  I D 0.67 36 37 C sum
  O y = 73.67 |>

  I V mean
  O y = 24.5566666667 |>

  I V median
  O y = 36.0 |>

# --- Fixed Display Mode ---

  I D 3 fixed 10 0.567 -1.6789
  O 10.0 x = 0.567 | 0.567 y = -1.6789 | -1.679 |fixed3|>

  I 2 fixed
  O 10.0 x = 0.567 | 0.57 y = -1.6789 | -1.68 |fixed2|>

  I ..
  O s3 = 10.0 | 10.00 s2 = 0.567 | 0.57 s1 = -1.6789 | -1.68 |fixed2|>

  I D 0 fixed 5.1
  O y = 5.1 | 5 |fixed0|>

  I D -1 fixed
  E While parsing fixed: Fixed Mode: value out of range: -1 !!
  O |fixed0|>

  I D 2 fixed i 5+i -1.123-2.234i
  O 1.0i x = 5.0+1.0i | 5.00+1.00i y = -1.123-2.234i | -1.12-2.23i |fixed2|>

  I ..
  O s3 = 1.0i | 1.00i s2 = 5.0+1.0i | 5.00+1.00i s1 = -1.123-2.234i | -1.12-2.23i |fixed2|>

  I D 2 fixed j 5+j -1.123-2.234j
  O 1.0j x = 5.0+1.0j | 5.00+1.00j y = -1.123-2.234j | -1.12-2.23j |fixed2|>

  I ..
  O s3 = 1.0j | 1.00j s2 = 5.0+1.0j | 5.00+1.00j s1 = -1.123-2.234j | -1.12-2.23j |fixed2|>

# --- Hexidecimal Display Mode ---

  I D hex 10.1 -10.5 0xabf -0xABF ..
  O s4 = 10.1 | 0x0A s3 = -10.5 | -0x0A s2 = 2751 | 0x0ABF s1 = -2751 | -0x0ABF |hex|mix|>

  I D i -2i -10.1+11.2i 171-205i ..
  O s4 = 1.0i | 0x00 s3 = -2.0i | 0x00 s2 = -10.1+11.2i | -0x0A s1 = 171.0-205.0i | 0xAB |hex|mix|>

# --- Binary Display Mode ---

  I D bin 10.0 -10.5 0b100 -0b100 5.4+4.5i ..
  O s5 = 10.0 | 0b1010 s4 = -10.5 | -0b1010 s3 = 4 | 0b100 s2 = -4 | -0b100 s1 = 5.4+4.5i | 0b101 |bin|mix|>

# --- Duration Display Mode ---

  I D floats dur 1234 12345678.9 3.14 10.5+4.2i ..
  O s4 = 1234.0 | 20:34 s3 = 12345678.9 | 142d21:21:18 s2 = 3.14 | 00:03 s1 = 10.5+4.2i | 00:10 |dur|> 

# --- Date and Time Display Modes - Due to time zones, just make sure that it doesn't crash ---

  I D date 1234 1600964826.4 10.5+4.2i -1234 ..
  A

  I D time 1234 1600964826.4 10.5+4.2i -1234 ..
  A

# --- Money display Mode ---

  I D $ 12.345 -0.11 10.5+4.2i ..
  O s3 = 12.345 | $12.35 s2 = -0.11 | -$0.11 s1 = 10.5+4.2i | $10.50 |$|>

# --- Cent display Mode ---

  I D cent 1234.5 -11 10.5+4.2i ..
  O s3 = 1234.5 | $12.35 s2 = -11.0 | -$0.11 s1 = 10.5+4.2i | $0.11 |cent|>

# --- Time Auto Enter ---

  I normal D 12/25 12/24 -
  O y = 86400.0 | 1d |time|>

# --- Duration Auto Enter ---

  I normal D 20:00 5000 meters>miles /
  O y = 386.24256 | 06:26 |dur|>

# --- Money Auto Enter ---

  I normal D $ 1.24 5.34 6.78 sum 1.09 *
  O y = 14.5624 | $14.56 |$|>

  I D cent -4234 -1215 -500 -2738 50000 sum
  O y = 41313.0 | $413.13 |cent|>

# --- Hexadecimal Auto Enter ---

  I normal D 0x80
  O y = 128 | 0x80 |hex|mix|>

  I D -0x1234
  O y = -4660 | -0x1234 |hex|mix|>

# --- Binary Auto Enter ---

  I normal D 0b1001
  O y = 9 | 0b1001 |bin|mix|>

# --- Disable and re-enable autoenter ---

  I normal floats manual D 0x80
  O y = 128.0 |manual|>

  I auto D 0x80
  O y = 128 | 0x80 |hex|mix|>

# --- Batch and interactive modes ---

  I normal floats D batch 4 5 +
  O 9.0 |batch|>

  I interactive .
  O y = 9.0 |>

# --- Expression Debugging ---

  I D debug 4 5 +
  O Exec: debug Exec: 4 y = 4.0 Exec: 5 x = 4.0 y = 5.0 Exec: + y = 9.0 |debug|>
  
  I nodebug
  O |>

# --- Type Conversion ---

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

  I l:c
  A
"""
# eot (for searching)

class Error(Exception):
  pass


class MaxLinesError(Error):
  pass


class OutputMismatch(Error):
  pass


class UnknownCommandError(Error):
  pass


class ExtraOutputError(Error):
  pass


def get_output(fout, max_chars=8192):
  line_data = []
  while max_chars > 0:
    fout.flush()
    line_data.append(fout.read(1))
    max_chars -= 1
    if len(line_data) < 2:
      continue
    if ((line_data[-1] == '>' and line_data[-2] == '|') or
        (line_data[-1] == '!' and line_data[-2] == '!')):
      line = ''.join(line_data)
      data = line.strip().split()
      logging.debug('data -> %s', data)
      return data
  raise MaxLinesError('max_chars exceeded.')


def compare_output(line_number, expected, actual):
  if expected != actual:
    raise OutputMismatch('Line %d:\n  Expected: %s\n       Got: %s' % (
        line_number, ' '.join(expected), ' '.join(actual)))


def check_for_extra_output(p, line_number, line):
  # Check stdout, stderr for unexpected stray output
  read_list, _, _ = select.select((p.stdout, p.stderr), (), (), 0)
  if p.stdout in read_list:
    has_extra_output('stdout', p.stdout, line_number, line)
  if p.stderr in read_list:
    has_extra_output('stderr', p.stderr, line_number, line)


def has_extra_output(name, f, line_number, line):
  data = []
  while True:
    read_list, _, _ = select.select((f,), (), (), 0)
    if not read_list:
      break
    data.append(f.read(1))

  data = ''.join(data).strip()

  if data:
    raise ExtraOutputError(
        '%s contains extra output: "%s" on line %d: %s' % (
            name,
            data,
            line_number,
            line))


def parse_line(line_number, line, p):
  """Parses a single line of DATA."""

  line = line.strip()
  if not line:
    return 0

  if line.startswith('#'):
    return 0

  tokens = line.split()
  cmd = tokens[0]
  if cmd == 'I':
    check_for_extra_output(p, line_number, line)
    p.stdin.write(' '.join(tokens[1:]))
    p.stdin.write('\n')
    return 0
  elif cmd == 'O':
    compare_output(line_number, tokens[1:], get_output(p.stdout))
  elif cmd == 'E':
    compare_output(line_number, tokens[1:], get_output(p.stderr))
  elif cmd == 'A':
    get_output(p.stdout)
  else:
    raise UnknownCommandError('Unknown Command: %s' % line)

  return 1

def main():
  p = subprocess.Popen(
      ['python', '-u', 'rpn'],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)

  get_output(p.stdout)
  tests_passed = 0
  tests_failed = 0

  for line_number, line in enumerate(DATA.split('\n')):
    try:
      tests_passed += parse_line(line_number + 1, line, p)
    except OutputMismatch as e:
      sys.stderr.write('%s\n' % e)
      tests_failed += 1
  check_for_extra_output(p, len(DATA), "EOF")

  # Wrap up
  sys.stdout.write('%s: %d / %d tests passed\n' % (
      __file__, tests_passed, tests_passed + tests_failed))
  p.terminate()
  p.wait()

  if tests_failed:
    sys.exit(1)

if __name__ == '__main__':
  main()
