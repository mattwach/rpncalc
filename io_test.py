#i!/usr/bin/python3
"""Runs IO tests on RPN."""

#pylint: disable=consider-using-with

import inspect
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
FIRST_DATA_LINE = inspect.currentframe().f_lineno + 1
DATA = """
  I interactive
  O interactive |>

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

  I D 5 2 ** $pi *
  O y = 78.53981633974483 |>

  I D 1e6 2.5e-4
  O x = 1000000.0 y = 0.00025 |>

# --- Operators ---

  I D 4 5 +
  O y = 9.0 |>

  I D 4 5 -
  O y = -1.0 |>

  I D 4 5 *
  O y = 20.0 |>

  I D 4 5 /
  O y = 0.8 |>

  I D 1+i 2+i +
  O y = 3.0+2.0i |>

  I D 1+i 2+i -
  O y = -1.0 |>

  I D 1+i 2+i *
  O y = 1.0+3.0i |>

  I D 1+i 2+i /
  O y = 0.6+0.2i |>

  I D +
  E While parsing +: Not Enough Stack Arguments !!
  O |>

  I D 5 -
  E While parsing -: Not Enough Stack Arguments !!
  O |>

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

  I normal nomix D 7+i 2+i &
  E While parsing &: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex' !!
  O |>

  I D 7+i 2+i |
  E While parsing |: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex' !!
  O |>

  I D 7+i 2+i ^
  E While parsing ^: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex' !!
  O |>

  I D 7+i 2 >>
  E While parsing >>: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex' !!
  O |>

  I D 7 2+i >>
  E While parsing >>: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex' !!
  O |>

  I D 7+i 2 <<
  E While parsing <<: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex' !!
  O |>

  I D 7 2+i <<
  E While parsing <<: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex' !!
  O |>

# --- Scientific ---

  I normal nomix D -12.34e6
  O y = -12340000.0 |>

  I D 12.34e-6
  O y = 1.234e-05 |>

  I D 100 log10
  O y = 2.0 |>

  I D $e 5 ** log
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

  I D 100+i log10
  O y = 2.000021713638431+0.004342800062890486i |>

  I D 100+i log
  O y = 4.605220183488258+0.009999666686665238i |>

  I D 5+i sq
  O y = 24.0+10.0i |>

  I D 25+i sqrt
  O y = 5.000999500419572+0.09998001398681428i |>

  I D 5+i !
  E While parsing !: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex' !!
  O |>

  I D 1+i inv
  O y = 0.5-0.5i |>

  I D 1234+i neg
  O y = -1234.0-1.0i |>

  I D -1234-i abs
  O y = 1234.0004051863193 |>

  I D 5 3+i **
  O y = -4.828996241741916+124.90668835293506i |>

  I D 5+i 3 **
  O y = 110.0+74.0i |>

  I D 5+i 3+i **
  O y = -65.89794145463469+86.60563035026283i |>

  I D 5e6i
  O y = 5000000.0i |>

  I D -5e6i
  O y = -5000000.0i |>

  I D 5e-6i
  O y = 5e-06i |>

  I D -5e-6i
  O y = -5e-06i |>

  I D 5.1e6i
  O y = 5100000.0i |>

  I D -5.1e6i
  O y = -5100000.0i |>

  I D 5.1e-6i
  O y = 5.1e-06i |>

  I D -5.1e-6i
  O y = -5.1e-06i |>

  I D 1+5e6i
  O y = 1.0+5000000.0i |>

  I D 1-5e6i
  O y = 1.0-5000000.0i |>

  I D 1+5e-6i
  O y = 1.0+5e-06i |>

  I D 1-5e-6i
  O y = 1.0-5e-06i |>

  I D 1+5.1e6i
  O y = 1.0+5100000.0i |>

  I D 1-5.1e6i
  O y = 1.0-5100000.0i |>

  I D 1.0+5.1e-6i
  O y = 1.0+5.1e-06i |>

  I D 1.0-5.1e-6i
  O y = 1.0-5.1e-06i |>

  I D -1+5e6i
  O y = -1.0+5000000.0i |>

  I D -1-5e6i
  O y = -1.0-5000000.0i |>

  I D -1+5e-6i
  O y = -1.0+5e-06i |>

  I D -1-5e-6i
  O y = -1.0-5e-06i |>

  I D -1+5.1e6i
  O y = -1.0+5100000.0i |>

  I D -1-5.1e6i
  O y = -1.0-5100000.0i |>

  I D -1+5.1e-6i
  O y = -1.0+5.1e-06i |>

  I D -1-5.1e-6i
  O y = -1.0-5.1e-06i |>

  I D 1.2+5e6i
  O y = 1.2+5000000.0i |>

  I D 1.2-5e6i
  O y = 1.2-5000000.0i |>

  I D 1.2+5e-6i
  O y = 1.2+5e-06i |>

  I D 1.2-5e-6i
  O y = 1.2-5e-06i |>

  I D 1.2+5.1e6i
  O y = 1.2+5100000.0i |>

  I D 1.2-5.1e6i
  O y = 1.2-5100000.0i |>

  I D 1.2+5.1e-6i
  O y = 1.2+5.1e-06i |>

  I D 1.2-5.1e-6i
  O y = 1.2-5.1e-06i |>

  I D -1.2+5e6i
  O y = -1.2+5000000.0i |>

  I D -1.2-5e6i
  O y = -1.2-5000000.0i |>

  I D -1.2+5e-6i
  O y = -1.2+5e-06i |>

  I D -1.2-5e-6i
  O y = -1.2-5e-06i |>

  I D -1.2+5.1e6i
  O y = -1.2+5100000.0i |>

  I D -1.2-5.1e6i
  O y = -1.2-5100000.0i |>

  I D -1.2+5.1e-6i
  O y = -1.2+5.1e-06i |>

  I D -1.2-5.1e-6i
  O y = -1.2-5.1e-06i |>

  I D 1.2e3+5e6i
  O y = 1200.0+5000000.0i |>

  I D 1.2e3-5e6i
  O y = 1200.0-5000000.0i |>

  I D 1.2e3+5e-6i
  O y = 1200.0+5e-06i |>

  I D 1.2e3-5e-6i
  O y = 1200.0-5e-06i |>

  I D 1.2e3+5.1e6i
  O y = 1200.0+5100000.0i |>

  I D 1.2e3-5.1e6i
  O y = 1200.0-5100000.0i |>

  I D 1.2e3+5.1e-6i
  O y = 1200.0+5.1e-06i |>

  I D 1.2e3-5.1e-6i
  O y = 1200.0-5.1e-06i |>

  I D -1.2e3+5e6i
  O y = -1200.0+5000000.0i |>

  I D -1.2e3-5e6i
  O y = -1200.0-5000000.0i |>

  I D -1.2e3+5e-6i
  O y = -1200.0+5e-06i |>

  I D -1.2e3-5e-6i
  O y = -1200.0-5e-06i |>

  I D -1.2e3+5.1e6i
  O y = -1200.0+5100000.0i |>

  I D -1.2e3-5.1e6i
  O y = -1200.0-5100000.0i |>

  I D -1.2e3+5.1e-6i
  O y = -1200.0+5.1e-06i |>

  I D -1.2e3-5.1e-6i
  O y = -1200.0-5.1e-06i |>

  I D 1.2e-3+5e6i
  O y = 0.0012+5000000.0i |>

  I D 1.2e-3-5e6i
  O y = 0.0012-5000000.0i |>

  I D 1.2e-3+5e-6i
  O y = 0.0012+5e-06i |>

  I D 1.2e-3-5e-6i
  O y = 0.0012-5e-06i |>

  I D 1.2e-3+5.1e6i
  O y = 0.0012+5100000.0i |>

  I D 1.2e-3-5.1e6i
  O y = 0.0012-5100000.0i |>

  I D 1.2e-3+5.1e-6i
  O y = 0.0012+5.1e-06i |>

  I D 1.2e-3-5.1e-6i
  O y = 0.0012-5.1e-06i |>

  I D -1.2e-3+5e6i
  O y = -0.0012+5000000.0i |>

  I D -1.2e-3-5e6i
  O y = -0.0012-5000000.0i |>

  I D -1.2e-3+5e-6i
  O y = -0.0012+5e-06i |>

  I D -1.2e-3-5e-6i
  O y = -0.0012-5e-06i |>

  I D -1.2e-3+5.1e6i
  O y = -0.0012+5100000.0i |>

  I D -1.2e-3-5.1e6i
  O y = -0.0012-5100000.0i |>

  I D -1.2e-3+5.1e-6i
  O y = -0.0012+5.1e-06i |>

  I D -1.2e-3-5.1e-6i
  O y = -0.0012-5.1e-06i |>

  I D 1 2e2<
  O y = 108.06046117362796+168.2941969615793i | 200.0<1.0 |polar|>

  I D 1 2e-2<
  O y = 0.010806046117362796+0.01682941969615793i | 0.020000000000000004<1.0 |polar|>

  I D 1 -2e2<
  O y = -108.06046117362796-168.2941969615793i | 200.0<-2.141592653589793 |polar|>

  I D 1 -2e-2<
  O y = -0.010806046117362796-0.01682941969615793i | 0.020000000000000004<-2.141592653589793 |polar|>

  I D 1 2.3e2<
  O y = 124.26953034967215+193.5383265058162i | 230.0<1.0 |polar|>

  I D 1 2.3e-2<
  O y = 0.012426953034967214+0.019353832650581618i | 0.023<0.9999999999999999 |polar|>

  I D 1 -2.3e2<
  O y = -124.26953034967215-193.5383265058162i | 230.0<-2.141592653589793 |polar|>

  I D 1 -2.3e-2<
  O y = -0.012426953034967214-0.019353832650581618i | 0.023<-2.141592653589793 |polar|>

  I D 2e2<1
  O y = 108.06046117362796+168.2941969615793i | 200.0<1.0 |polar|>

  I D 2e-2<1
  O y = 0.010806046117362796+0.01682941969615793i | 0.020000000000000004<1.0 |polar|>

  I D -2e2<1
  O y = -108.06046117362796-168.2941969615793i | 200.0<-2.141592653589793 |polar|>

  I D -2e-2<1
  O y = -0.010806046117362796-0.01682941969615793i | 0.020000000000000004<-2.141592653589793 |polar|>

  I D 2.3e2<1
  O y = 124.26953034967215+193.5383265058162i | 230.0<1.0 |polar|>

  I D 2.3e-2<1
  O y = 0.012426953034967214+0.019353832650581618i | 0.023<0.9999999999999999 |polar|>

  I D -2.3e2<1
  O y = -124.26953034967215-193.5383265058162i | 230.0<-2.141592653589793 |polar|>

  I D -2.3e-2<1
  O y = -0.012426953034967214-0.019353832650581618i | 0.023<-2.141592653589793 |polar|>

  I D 5<2e2
  O y = 2.4359383750350294-4.366486486069973i | 5.0<-1.0619298297467672 |polar|>

  I D 5<2e-2
  O y = 4.999000033332889+0.0999933334666654i | 5.0<0.02 |polar|>

  I D 5<-2e2
  O y = 2.4359383750350294+4.366486486069973i | 5.0<1.0619298297467672 |polar|>

  I D 5<-2e-2
  O y = 4.999000033332889-0.0999933334666654i | 5.0<-0.02 |polar|>

  I D 5<2.3e2
  O y = -3.93847970822529-3.0803210202668225i | 5.0<-2.4778563656446995 |polar|>

  I D 5<2.3e-2
  O y = 4.99867755829918+0.11498986110151091i | 5.0<0.023 |polar|>

  I D 5<-2.3e2
  O y = -3.93847970822529+3.0803210202668225i | 5.0<2.4778563656446995 |polar|>

  I D 5<-2.3e-2
  O y = 4.99867755829918-0.11498986110151091i | 5.0<-0.023 |polar|>

  I D 4.5e6<1.2e3
  O y = 4482431.201334612-397253.7291227677i | 4500000.0<-0.0883936713010171 |polar|>

  I D 4.5e6<1.2e-3
  O y = 4499996.760000389+5399.998704000092i | 4500000.0<0.0011999999999999997 |polar|>

  I D 4.5e6<-1.2e3
  O y = 4482431.201334612+397253.7291227677i | 4500000.0<0.0883936713010171 |polar|>

  I D 4.5e6<-1.2e-3
  O y = 4499996.760000389-5399.998704000092i | 4500000.0<-0.0011999999999999997 |polar|>

  I D 4.5e-6<1.2e3
  O y = 4.482431201334612e-06-3.972537291227677e-07i | 4.5e-06<-0.0883936713010171 |polar|>

  I D 4.5e-6<1.2e-3
  O y = 4.499996760000389e-06+5.399998704000092e-09i | 4.5e-06<0.0011999999999999997 |polar|>

  I D 4.5e-6<-1.2e3
  O y = 4.482431201334612e-06+3.972537291227677e-07i | 4.5e-06<0.0883936713010171 |polar|>

  I D 4.5e-6<-1.2e-3
  O y = 4.499996760000389e-06-5.399998704000092e-09i | 4.5e-06<-0.0011999999999999997 |polar|>

  I D -4.5e6<1.2e3
  O y = -4482431.201334612+397253.7291227677i | 4500000.0<3.053198982288776 |polar|>

  I D -4.5e6<1.2e-3
  O y = -4499996.760000389-5399.998704000092i | 4500000.0<-3.1403926535897932 |polar|>

  I D -4.5e6<-1.2e3
  O y = -4482431.201334612-397253.7291227677i | 4500000.0<-3.053198982288776 |polar|>

  I D -4.5e6<-1.2e-3
  O y = -4499996.760000389+5399.998704000092i | 4500000.0<3.1403926535897932 |polar|>

  I D -4.5e-6<1.2e3
  O y = -4.482431201334612e-06+3.972537291227677e-07i | 4.5e-06<3.053198982288776 |polar|>

  I D -4.5e-6<1.2e-3
  O y = -4.499996760000389e-06-5.399998704000092e-09i | 4.5e-06<-3.1403926535897932 |polar|>

  I D -4.5e-6<-1.2e3
  O y = -4.482431201334612e-06-3.972537291227677e-07i | 4.5e-06<-3.053198982288776 |polar|>

  I D -4.5e-6<-1.2e-3
  O y = -4.499996760000389e-06+5.399998704000092e-09i | 4.5e-06<3.1403926535897932 |polar|>

  I normal D 1e
  E Value Error: could not convert string to float: '1e' !!
  O |>

  I normal D e1
  E While parsing e1: Unknown Argument (try ? for help) !!
  O |>

  I 1-2
  E Value Error: could not convert string to float: '1-2' !!
  O |>

  I 1.2.3
  E While parsing 1.2.3: Unknown Argument (try ? for help) !!
  O |>

# --- Trig functions, in radians ---

  I D normal $pi 6 / sin
  O y = 0.49999999999999994 |>

  I D $pi 3 / cos
  O y = 0.5000000000000001 |>

  I D $pi 4 / tan
  O y = 0.9999999999999999 |>

  I D 1 asin $pi 2 / -
  O y = 0.0 |>

  I D 0 acos $pi 2 / -
  O y = 0.0 |>

  I D 1 atan $pi 4 / -
  O y = 0.0 |>

  I D 1+i sin
  O y = 1.2984575814159773+0.6349639147847361i |>

  I asin
  O y = 1.0+1.0i |>

  I D 1+i cos
  O y = 0.8337300251311491-0.9888977057628651i |>

  I acos
  O y = 0.9999999999999999+1.0i |>

  I D 1+i tan
  O y = 0.2717525853195118+1.0839233273386946i |>

  I atan
  O y = 1.0+0.9999999999999999i |>

  I D sin
  E While parsing sin: Not Enough Stack Arguments !!
  O |>

# --- Trig functions, in degrees ---

  I D deg 30 sin
  O y = 0.49999999999999994 |deg|>

  I D 60 cos
  O y = 0.5000000000000001 |deg|>

  I D 45 tan
  O y = 0.9999999999999999 |deg|>

  I D 1 asin
  O y = 90.0 |deg|>

  I D 0 acos
  O y = 90.0 |deg|>

  I D 1 atan 
  O y = 45.0 |deg|>

  I D 1+i sin
  E While parsing sin: Degree mode is not supported for complex trigonometry !!
  O |deg|>

  I D sin
  E While parsing sin: Not Enough Stack Arguments !!
  O |deg|>

  I rad
  A

# --- Simple Clipboard ---

  I D 123+i c v v
  O 123.0+1.0i x = 123.0+1.0i y = 123.0+1.0i |>

  I D 123 456 x 789 v
  O 123.0 x = 789.0 y = 456.0 |>
  
  I D c
  E While parsing c: Not Enough Stack Arguments !!
  O |>

  I D x
  E While parsing x: Not Enough Stack Arguments !!
  O |>

# --- Stack Clipboard ---

  I D 1 2 3 4 1 pc v
  O 1.0 2.0 3.0 x = 4.0 y = 3.0 |>

  I D 1 2 3 4 1 px v
  O 1.0 2.0 x = 4.0 y = 3.0 |>

  I D 1 2 3 4 c 2 pv
  O 1.0 2.0 4.0 x = 3.0 y = 4.0 |>

  I D 1 1 pc
  E While parsing pc: Not Enough Stack Arguments !!
  O y = 1.0 |>

# --- Variables ---

  I D 5678 myvar= 0 $myvar
  O myvar = 5678.0 x = 0.0 y = 5678.0 |>

  I D set
  O c = 299792458.0 e = 2.718281828459045 myvar = 5678.0 pi = 3.141592653589793 |>

  I D myvar=
  E While parsing myvar=: Not Enough Stack Arguments !!
  O |>

  I D $foo
  E While parsing $foo: KeyError !!
  O |>

  I D 5 x= .
  O x = 5.0 |>

  I myvar!=
  O |>

  I myvar!=
  E While parsing myvar!=: KeyError !!
  O |>
  
  I set
  O c = 299792458.0 e = 2.718281828459045 pi = 3.141592653589793 x = 5.0 |>

  I pushv
  O |>

  I set
  O c = 299792458.0 e = 2.718281828459045 pi = 3.141592653589793 x = 5.0 |>

  I 4 a= 6 x=
  O a = 4.0 x = 6.0 |>

  I popv set
  O c = 299792458.0 e = 2.718281828459045 pi = 3.141592653589793 x = 5.0 |>

# --- Full Stack Clipboard ---

  I V
  O |>

  I D 1 2 3 C
  O 1.0 x = 2.0 y = 3.0 |>

  I D V
  O 1.0 x = 2.0 y = 3.0 |>

  I D 4 5 6 X
  O |>

  I V
  O 4.0 x = 5.0 y = 6.0 |>

# --- Integers ---

  I D normal mix 1 2.0
  O x = 1 y = 2.0 |mix|>

  I +
  O y = 3.0 |mix|>

  I D 5 2 /
  O y = 2.5 |mix|>

  I D mix 1 2.0 nomix
  O x = 1 y = 2.0 |>

  I D nomix 5.0 int
  O y = 5 |mix|>

  I nomix float
  O y = 5.0 |mix|>

  I nomix D 5+i int
  O y = 5 |mix|>

  I nomix D 5+i float
  O y = 5.0 |mix|>

  I manual nomix D 1 2.0
  O x = 1.0 y = 2.0 |manual|>

  I D 5.0 int
  E While parsing int: Can not automatically enter mixed mode because auto mode is disabled. !!
  O y = 5.0 |manual|>

  I D mix 5.0 int
  O y = 5 |mix|manual|>

  I D mix 5+i int
  O y = 5 |mix|manual|>

  I D nomix 5 float
  O y = 5.0 |manual|>

  I D 5+i float
  O y = 5.0 |manual|>

# --- Complex Numbers ---

  I auto nomix normal D i
  O y = 1.0i |>

  I D -i
  O y = -1.0i |>

  I D 5+4i
  O y = 5.0+4.0i |>

  I -6-2j
  O x = 5.0+4.0j y = -6.0-2.0j |>

  I D 1+i
  O y = 1.0+1.0i |>

  I D 6 i 7 * -
  O y = 6.0-7.0i |>

  I D -1 sqrt
  O y = 1.0i |>

  I D 5+5i 4-5i +
  O y = 9.0 |>

  I D 5<3.14
  O y = -4.999993658637697+0.00796326458243414i | 4.999999999999999<3.14 |polar|>

  I deg
  O y = -4.999993658637697+0.00796326458243414i | 4.999999999999999<179.9087476710785 |polar|deg|>

  I D -6<90
  O y = -3.6739403974420594e-16-6.0i | 6.0<-90.00000000000001 |polar|deg|>

  I rad
  O y = -3.6739403974420594e-16-6.0i | 6.0<-1.5707963267948968 |polar|>

  I D $pi 2 / 5<
  O y = 3.061616997868383e-16+5.0i | 5.0<1.5707963267948966 |polar|>

  I deg
  O y = 3.061616997868383e-16+5.0i | 5.0<90.0 |polar|deg|>

  I D 5 45 1< *
  O y = 3.5355339059327378+3.5355339059327373i | 5.0<45.0 |polar|deg|>

  I D rad 6 1 1< *
  O y = 3.2418138352088386+5.048825908847379i | 6.0<0.9999999999999999 |polar|>

  I normal D 3+4i real
  O y = 3.0 |>

  I D 3+4i imag
  O y = 4.0 |>

  I D 3+4i mag
  O y = 5.0 |>

  I D 3+4i phase
  O y = 0.9272952180016122 |>

  I deg D 3+4i phase
  O y = 53.13010235415598 |deg|>

  I rad D 5 real
  O y = 5.0 |>

  I D 5 imag
  O y = 0.0 |>

  I D 5 mag
  O y = 5.0 |>

  I D 5 phase
  O y = 0.0 |>

# --- Time Tests ---

  I D 1/14/2010
  O y = 1263456000.0 | 01/14/2010 (Thu) |time|>

  I D 07/30/2006+16:00:00
  O y = 1154300400.0  | 07/30/2006+16:00:00 (Sun) |time|>

  I D 1/14/2020 1+i +
  O y = 1578988801.0+1.0i | 01/14/2020+00:00:01 (Tue) |time|>

  I D now
  A

  I D today
  A

# -- Duration Tests ---

  I D normal 4d
  O y = 345600.0 | 4d |dur|>

  I D -4d
  O y = -345600.0 | -4d |dur|>

  I D 1d 66+100i +
  O y = 86466.0+100.0i | 1d00:01:06 |dur|>

  I D 1d14:23:12
  O y = 138192.0 | 1d14:23:12 |dur|>

  I D 534:12:00
  O y = 1923120.0 | 22d06:12:00 |dur|>

  I D 536:45
  O y = 32205.0 | 0d08:56:45 |dur|>

# --- Stack Management ---

  I normal nomix D 1 2 3 4 5 6 7 8 9 10 11
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
  O y = 24.55666666666667 |>

  I V median
  O y = 36.0 |>

  I D 1+i 1+2i 3-i C sum
  O y = 5.0+2.0i |>

  I V mean
  O y = 1.6666666666666667+0.6666666666666666i |>

  I V median
  E While parsing median: TypeError: '<' not supported between instances of 'complex' and 'complex' !!
  O |>

  I D sum
  E While parsing sum: Stack is empty !!
  O |>

  I D mean
  E While parsing mean: Stack is empty !!
  O |>

  I D median
  E While parsing median: Stack is empty !!
  O |>

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

# --- Significant Display Mode ---

  I D 3 sig 10 0.567 -1.6789
  O 10.0 x = 0.567 | 0.567 y = -1.6789 | -1.68 |sig3|>

  I 2 sig
  O 10.0 x = 0.567 | 0.57 y = -1.6789 | -1.7 |sig2|>

  I ..
  O s3 = 10.0 | 10 s2 = 0.567 | 0.57 s1 = -1.6789 | -1.7 |sig2|>

  I D 0 sig
  E While parsing sig: Fixed Mode: value out of range: 0 !!
  O |sig2|>

  I D 2 sig i 5+i -1.123-2.234i
  O 1.0i x = 5.0+1.0i | 5+i y = -1.123-2.234i | -1.1-2.2i |sig2|>

  I ..
  O s3 = 1.0i | i s2 = 5.0+1.0i | 5+i s1 = -1.123-2.234i | -1.1-2.2i |sig2|>

  I D 2 sig j 5+j -1.123-2.234j
  O 1.0j x = 5.0+1.0j | 5+j y = -1.123-2.234j | -1.1-2.2j |sig2|>

  I ..
  O s3 = 1.0j | j s2 = 5.0+1.0j | 5+j s1 = -1.123-2.234j | -1.1-2.2j |sig2|>

# --- Fixed Polar Display Mode ---

  I D 1+i deg 3 fixedpolar
  O y = 1.0+1.0i | 1.414<45.000 |fixedpolar3|deg|>

  I rad
  O y = 1.0+1.0i | 1.414<0.785 |fixedpolar3|>

# --- Significant Polar Display Mode ---

  I D 1+i deg 3 sigpolar
  O y = 1.0+1.0i | 1.41<45 |sigpolar3|deg|>

  I rad
  O y = 1.0+1.0i | 1.41<0.785 |sigpolar3|>

# --- Hexidecimal Display Mode ---

  I D hex 10.1 -10.5 0xabf -0xABF ..
  O s4 = 10.1 | 0x0A s3 = -10.5 | -0x0A s2 = 2751 | 0x0ABF s1 = -2751 | -0x0ABF |hex|mix|>

  I D i -2i -10.1+11.2i 171-205i ..
  O s4 = 1.0i | 0x00 s3 = -2.0i | 0x00 s2 = -10.1+11.2i | -0x0A s1 = 171.0-205.0i | 0xAB |hex|mix|>

# --- Binary Display Mode ---

  I D bin 10.0 -10.5 0b100 -0b100 5.4+4.5i ..
  O s5 = 10.0 | 0b1010 s4 = -10.5 | -0b1010 s3 = 4 | 0b100 s2 = -4 | -0b100 s1 = 5.4+4.5i | 0b101 |bin|mix|>

# --- Duration Display Mode ---

  I D nomix dur 1234 12345678.9 3.14 10.5+4.2i ..
  O s4 = 1234.0 | 0d00:20:34 s3 = 12345678.9 | 142d21:21:18 s2 = 3.14 | 0d00:00:03 s1 = 10.5+4.2i | 0d00:00:10 |dur|>

# --- Date and Time Display Modes - Due to time zones, just make sure that it doesn't crash ---

  I D date 1234 1600964826.4 10.5+4.2i -1234 ..
  A

  I D time 1234 1600964826.4 10.5+4.2i -1234 ..
  A

# --- Polar Display Mode ---

  I D 1+i deg polar
  O y = 1.0+1.0i | 1.4142135623730951<45.0 |polar|deg|>

# --- Money display Mode ---

  I rad D $ 12.345 -0.11 10.5+4.2i ..
  O s3 = 12.345 | $12.35 s2 = -0.11 | -$0.11 s1 = 10.5+4.2i | $10.50 |$|>

# --- Cent display Mode ---

  I D cent 1234.5 -11 10.5+4.2i ..
  O s3 = 1234.5 | $12.35 s2 = -11.0 | -$0.11 s1 = 10.5+4.2i | $0.11 |cent|>

# --- Time Auto Enter ---

  I normal D 12/25 12/24 -
  O y = 86400.0 | 1d |time|>

# --- Duration Auto Enter ---

  I normal D 20:00 5000 meters>miles /
  O y = 386.24256 | 0d00:06:26 |dur|>

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

  I normal nomix manual D 0x80
  O y = 128.0 |manual|>

  I auto D 0x80
  O y = 128 | 0x80 |hex|mix|>

# --- Expression Debugging ---

  I normal nomix D debug 4 5 +
  O Exec: debug Exec: 4 y = 4.0 Exec: 5 x = 4.0 y = 5.0 Exec: + y = 9.0 |debug|>
  
  I nodebug
  O |>

# --- Type Conversion ---

  I D 10 in>cm
  O y = 25.4 |>

  I D 25.4 cm>in
  O y = 10.0 |>

  I D 1 mi*mi>acres
  O y = 640.0000003797903 |>

  I D 1 pint>tsp
  O y = 96.00000007299742 |>

  I D 10 n*m>in*lbs
  O y = 88.50431476562046 |>

  I D 4 ft>yards 25 25 * * yard*yard*yard>gallon
  O y = 168311.68848798322 |>

  I D 10+i in>cm
  O y = 25.4+2.54i |>

  I D in>cm
  E While parsing in>cm: Not Enough Stack Arguments !!
  O |>

  I l:c
  A

# --- Macros ---

  I m:pyth 2 ** s 2 ** + sqrt
  O |>
  
  I D 3 4 @pyth
  O y = 5.0 |>
  
  I D 6 8 1 ?pyth
  O y = 10.0 |>
  
  I D 6 8 0 ?pyth
  O x = 6.0 y = 8.0 |>

  I D m:foo
  E While parsing m:foo: Unknown Argument (try ? for help) !!
  O |>

  I l:m
  O pyth | 2 ** s 2 ** + sqrt q | q |>

  I m:local 5 a=
  O |>

  I @local
  O a = 5.0 |>

  I $a
  E While parsing $a: KeyError !!
  O |>

# --- Conditionals ---

  I D 1 2 > 2 1 > 2 2 >
  O 0.0 x = 1.0 y = 0.0 |>

  I D 1 2 < 2 1 < 2 2 <
  O 1.0 x = 0.0 y = 0.0 |>

  I D 1 2 >= 2 1 >= 2 2 >=
  O 0.0 x = 1.0 y = 1.0 |>

  I D 1 2 <= 2 1 <= 2 2 <=
  O 1.0 x = 0.0 y = 1.0 |>

  I D 1 2 == 2 1 == 2 2 ==
  O 0.0 x = 0.0 y = 1.0 |>

  I D 1 2 != 2 1 != 2 2 !=
  O 1.0 x = 1.0 y = 0.0 |>

  I D 0 not 1 not 1+i not
  O 1.0 x = 0.0 y = 0.0 |>

  I D 1 1+i <
  E While parsing <: TypeError: '<' not supported between instances of 'float' and 'complex' !!
  O |>

  I D 1 1+i >
  E While parsing >: TypeError: '>' not supported between instances of 'float' and 'complex' !!
  O |>

  I D 1 1+i <=
  E While parsing <=: TypeError: '<=' not supported between instances of 'float' and 'complex' !!
  O |>

  I D 1 1+i >=
  E While parsing >=: TypeError: '>=' not supported between instances of 'float' and 'complex' !!
  O |>

  I D 1 1+i ==
  O y = 0.0 |>

  I D 1+i 1+i ==
  O y = 1.0 |>

  I D 1 1+i !=
  O y = 1.0 |>

  I D 1+i 1+i !=
  O y = 0.0 |>

  I D >
  E While parsing >: Not Enough Stack Arguments !!
  O |>

  I D 1 >
  E While parsing >: Not Enough Stack Arguments !!
  O |>

  I D >=
  E While parsing >=: Not Enough Stack Arguments !!
  O |>

  I D 1 >=
  E While parsing >=: Not Enough Stack Arguments !!
  O |>

  I D <
  E While parsing <: Not Enough Stack Arguments !!
  O |>

  I D 1 <
  E While parsing <: Not Enough Stack Arguments !!
  O |>

  I D <=
  E While parsing <=: Not Enough Stack Arguments !!
  O |>

  I D 1 <=
  E While parsing <=: Not Enough Stack Arguments !!
  O |>

  I D ==
  E While parsing ==: Not Enough Stack Arguments !!
  O |>

  I D 1 ==
  E While parsing ==: Not Enough Stack Arguments !!
  O |>

  I D !=
  E While parsing !=: Not Enough Stack Arguments !!
  O |>

  I D 1 !=
  E While parsing !=: Not Enough Stack Arguments !!
  O |>

  I D not
  E While parsing not: Not Enough Stack Arguments !!
  O |>
"""
# eot (for searching)

class Error(Exception):
  pass


class NoDataError(Exception):
  pass

class MaxLinesError(Error):
  pass


class OutputMismatch(Error):
  pass


class UnknownCommandError(Error):
  pass


class ExtraOutputError(Error):
  pass


def get_output(fout, max_chars=65536):
  line_data = []
  while max_chars > 0:
    fout.flush()
    c = fout.read(1)
    line_data.append(c)
    max_chars -= 1
    if len(line_data) < 2:
      continue
    if ((line_data[-1] == '>' and line_data[-2] == '|') or
        (line_data[-1] == '!' and line_data[-2] == '!')):
      line = ''.join(line_data)
      data = line.strip().split()
      logging.debug('data -> %s', data)
      return data
  raise MaxLinesError('max_chars exceeded: %s' % ''.join(line_data))


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
    p.stdin.flush()
    return 0

  if cmd == 'O':
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
      ['python3', '-u', 'rpn'],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      encoding='utf8')

  tests_passed = 0
  tests_failed = 0

  for line_number, line in enumerate(DATA.split('\n')):
    try:
      tests_passed += parse_line(line_number + FIRST_DATA_LINE, line, p)
    except OutputMismatch as e:
      sys.stderr.write('%s\n' % e)
      tests_failed += 1
  check_for_extra_output(p, len(DATA) + FIRST_DATA_LINE, "EOF")

  # Wrap up
  sys.stdout.write('%s: %d / %d tests passed\n' % (
      __file__, tests_passed, tests_passed + tests_failed))
  p.terminate()
  p.wait()

  if tests_failed:
    sys.exit(1)

if __name__ == '__main__':
  main()
