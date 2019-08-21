#
# Convert between unit types.
# For example mph -> min/mile
#

import math
import sys

#
# Implementation:
#
# Step 1: interpret the type string via a series of aliases
# Step 2: flip term 1 if needed, or return an error if there is no way to
#   convert
# Step 3: convert numerators
# Step 4: If needed
#  a) invert
#  b) convert numerators
#  c) invert
#
# Done!

#
# Conversions to meters
#

DISTANCE_CONVERT = (
  (    1.0000, 'meter', 'm', 'meters', 'metre', 'metres'),
  ( 1609.3440, 'mile', 'miles', 'mi'),
  (    0.0254, 'inch', 'inches', 'in'),
  (    0.0100, 'centimeter', 'centimeters', 'cm'),
  (    0.1000, 'decimeter', 'decimeters'),
  (    0.0010, 'millimeter', 'millimeters', 'mm'),
  ( 1000.0000, 'kilometer', 'kilometers', 'km'),
  (    0.3048, 'foot', 'feet', 'ft'),
  (    0.9144, 'yard', 'yards', 'yd'),
  (    0.155849127913, '_gallonmeters'),
  (    0.0779245639837, '_pintmeter'),
  (    0.0170183442005, '_teaspoonmeters'),
  (    0.0245446996271, '_tablespoonmeters'),
  (    0.098178798467, '_quartmeter'),
  (   63.6149072152, '_acremeter'),
)

#
# Conversion to seconds
#

TIME_CONVERT = (
  (      1.0000, 'second', 'seconds', 'sec', 's'),
  (      0.0010, 'millisecond', 'milliseconds', 'ms'),
  (      1.0e-6, 'microsecond', 'microseconds', 'us'),
  (      1.0e-9, 'nanesecond', 'nanoseconds', 'ns'),
  (     60.0000, 'minute', 'minutes', 'min'),
  (   3600.0000, 'hour', 'hours', 'hr', 'h'),
  (  86400.0000, 'day', 'days'),
  ( 604800.0000, 'week', 'weeks'),
)

#
# Weight/Mass Conversions (planet earth :) )
#

MASS_CONVERT = (
  (      1.00000,   'gram', 'grams', 'g' ),
  (   1000.00000,   'kilogram', 'kilograms', 'kg' ),
  (     28.3495231, 'ounce', 'ounces', 'oz' ),
  (    453.59237,   'pound', 'pounds', 'lbs', 'lb' ),
  ( 907184.74000,   'ton', 'tons'),
  (     101.9680,   'newton', 'newtons', 'n'),
  (  101968.0000,   'kilonewton', 'kilonewtons'),
  (  10196800.0000,   '_barnewton'),
)

#
# Cycles
#

CYCLE_CONVERT = (
  (          1.0000, 'cycle', 'cycles' ),
  (    1000000.0000, 'kilacycle', 'kilacycles' ),
  (    1000000.0000, 'megacycle', 'megacycles' ),
  ( 1000000000.0000, 'gigacycle', 'gigacycles' ),
)

#
# Memory
#

MEMORY_CONVERT = (
  (             1.0000, 'bit', 'bits' ),
  (          1024.0000, 'kilobit', 'kilobits' ),
  (             8.0000, 'byte', 'bytes' ),
  (          8192.0000, 'kilobyte', 'kilobytes', 'kb' ),
  (       8388608.0000, 'megabyte', 'megabytes', 'mb' ),
  (    8589934592.0000, 'gigabyte', 'gigabytes', 'gb' ),
  ( 8796093022208.0000, 'terabyte', 'terabytes', 'tb' ),
)

#
# Angles
#

ANGLE_CONVERT = (
  ( 1.0000, 'radians', 'rad' ),
  ( math.pi / 180.0, 'degrees', 'deg'),
)

#
# Energy
#

ENERGY_CONVERT = (
  (         1.0000, 'joules', 'j' ),
  (      1000.0000, 'kilojoules', 'kj' ),
  (   1000000.0000, 'megajoules', 'mj' ),
  (   3600000.0000, 'kwh' ),
  (       745.699872, 'hps' ),
  (      1055.0600, 'btu'), # EC standard
  ( 105506000.0000, 'therm'), # EC standard
  (         4.2000, 'calorie', 'cal', 'calories'), 
  (       4200.0000, 'kilocalorie', 'kilocalories'), 
)

#
# Temperature
#

TEMPERATURE_CONVERT = (
  (1.0, 'c', 'celsius'),
  ((5.0/9.0, -32), 'f', 'fahrenheit'),
  ((1.0, -273.15), 'k', 'kelvin'),
)

#
# Aliases to help things along
#

ALIASES = {
  'acre': '_acremeter*_acremeter',
  'acres': 'acre',
  'bar': '_barnewton/meter*meter',
  'cadence': 'cycles/minute',
  'gallon': '_gallonmeters*_gallonmeters*_gallonmeters',
  'gallons': 'gallon',
  'ghz': 'gigacycles/second',
  'hp': 'hps/second',
  'hz': 'cycles/second',
  'khz': 'kilacycles/second',
  'kilowatt': 'kilojoules/second',
  'kilowatts': 'kilowatt',
  'kw': 'kilojoules/second',
  'liter': 'decimeter*decimeter*decimeter',
  'litre': 'liter',
  'liters': 'liter',
  'litres': 'liter',
  'milliliter': 'cm*cm*cm',
  'milliliters': 'milliliter',
  'ml': 'milliliter',
  'megawatt': 'megajoules/second',
  'megawatts': 'megawatt',
  'mw': 'megajoules/second',
  'mhz': 'megacycles/second',
  'mph': 'miles/hour',
  'pascal': 'newton/meter*meter',
  'pascals': 'pascal',
  'pa': 'pascal',
  'kilopascal': 'kilonewtons/meter*meter',
  'kilopascals': 'kilopascal',
  'kpa': 'kilopascal',
  'pint': '_pintmeter*_pintmeter*_pintmeter',
  'pints': 'pint',
  'psi': 'pounds/inch*inch',
  'quart': '_quartmeter*_quartmeter*_quartmeter',
  'quarts': 'quart',
  'rpm': 'cycles/minute',
  'tablespoon': '_tablespoonmeters*_tablespoonmeters*_tablespoonmeters',
  'tablespoons': 'tablespoon',
  'tsp': '_teaspoonmeters*_teaspoonmeters*_teaspoonmeters',
  'teaspoon': 'tsp',
  'teaspoons': 'tsp',
  'watt': 'joules/second',
  'watts': 'watt',
}

#
# Classes
#

class Error(Exception):
  def __init__(self, msg=None):
    Exception.__init__(self, msg)


class DuplicateKey(Error):
  def __init__(self, keyname):
    Error.__init__(self, keyname)


class IllegalConversionBetweenRatioAndScalar(Error):
  pass


class UnknownConversionType(Error):
  def __init__(self, type_name):
    Error.__init__(self, type_name)


class IncompatibleConversionTypes(Error):
  def __init__(self, source_type, target_type):
    Error.__init__(self, '%s -> %s' % (source_type, target_type))


class Conversion(object):

  def __init__(self):
    self.convert_dict = {}
    self._InsertKeys('Distance',            DISTANCE_CONVERT)
    self._InsertKeys('Time',                TIME_CONVERT)
    self._InsertKeys('Force/Weight/Mass (Planet Earth)', MASS_CONVERT)
    self._InsertKeys('Cycles',              CYCLE_CONVERT)
    self._InsertKeys('Memory',              MEMORY_CONVERT)
    self._InsertKeys('Angles',              ANGLE_CONVERT)
    self._InsertKeys('Energy',              ENERGY_CONVERT)
    self._InsertKeys('Temperature',         TEMPERATURE_CONVERT)

  def Convert(self, value, value_type, target_type):

    # extract type and class information

    source = self._AnalyzeType(value_type)
    target = self._AnalyzeType(target_type)

    # check for ratio incompatibility

    if source.IsRatio() != target.IsRatio():
      raise IllegalConversionBetweenRatioAndScalar()

    # check for inversion eligibility

    if (target.IsRatio() and 
        (source.numerator_name == target.denominator_name)):
      target.Invert()

    # check for numerator compatibility

    if source.numerator_name != target.numerator_name:
      raise IncompatibleConversionTypes(source.numerator_name,
                                        target.numerator_name)

    # check for denominator compatibility, if needed

    if (source.IsRatio() and
        (source.denominator_name != target.denominator_name)):
      raise IncompatibleConversionTypes(source.denominator_name,
                                        target.denominator_name)

    # scale the value by each numerator

    for snum in source.numerator:
      value = self._ScaleUp(value, snum.scale_factor)
    for tnum in target.numerator:
      value = self._ScaleDown(value, tnum.scale_factor)

    # if needed, scale by each denominator

    if source.IsRatio():
      for sden in source.denominator:
        value = self._ScaleDown(value, sden.scale_factor)
      for tden in target.denominator:
        value = self._ScaleUp(value, tden.scale_factor)
      if target.inverted:
        value = 1.0 / value

    return value

  def _ScaleUp(self, value, scale_factor):
    if type(scale_factor) is tuple:
      return (value + scale_factor[1]) * scale_factor[0]
    else:
      return value * scale_factor

  def _ScaleDown(self, value, scale_factor):
    if type(scale_factor) is tuple:
      return (value / scale_factor[0]) - scale_factor[1]
    else:
      return value / scale_factor

  def DumpHelp(self):

    classes = {}

    for conversion_name, conversion in self.convert_dict.iteritems():
      if conversion.class_name not in classes:
        classes[conversion.class_name] = []
      classes[conversion.class_name].append(conversion_name)

    for class_name in sorted(classes):
      sys.stdout.write('\n%s:\n' % class_name)
      names = sorted(classes[class_name])
      names.reverse()
      sub_names = []
      while names:
        name = names.pop()
        if name.startswith('_'):
          continue
        sub_names.append(name)
        if len(sub_names) == 4:
          self._DumpColumns(sub_names)
          sub_names = []
      if sub_names:
        self._DumpColumns(sub_names)

    sys.stdout.write('\nUseful Aliases:\n')
    for alias_name in sorted(ALIASES):
      sys.stdout.write('  %-15s ->  %s\n' % (alias_name, ALIASES[alias_name]))

  def _DumpColumns(self, name_list):

    sys.stdout.write('  ')
    for name in name_list:
      sys.stdout.write('%-15s ' % name)
    sys.stdout.write('\n')

  def _AnalyzeType(self, type_str):

    numerator_type_list, denominator_type_list = self._AnalyzeTypeStr(type_str)

    self._CheckForAliases(numerator_type_list, denominator_type_list)
    self._CheckForAliases(denominator_type_list, numerator_type_list)

    numerator = []
    denominator = []

    for numerator_type in numerator_type_list:
      if numerator_type not in self.convert_dict:
        raise UnknownConversionType(numerator_type)
      numerator.append(self.convert_dict[numerator_type])

    for denominator_type in denominator_type_list:
      if denominator_type not in self.convert_dict:
        raise UnknownConversionType(denominator_type)
      denominator.append(self.convert_dict[denominator_type])

    return ConversionData(numerator, denominator)

  def _CheckForAliases(self, numerator, denominator):

    index = 0
    while index < len(numerator):
      if numerator[index] in ALIASES:
        alias = ALIASES[numerator[index]]
        del(numerator[index])
        if '/' in alias:
          n, d = alias.split('/')
          numerator.extend(n.split('*'))
          denominator.extend(d.split('*'))
        else:
          numerator.extend(alias.split('*'))
        index = 0
      else:
        index += 1

    numerator.sort()
    denominator.sort()

  def _AnalyzeTypeStr(self, type_str):
    if '/' in type_str:
      num, den = type_str.split('/')
      numerator_type = sorted(num.split('*'))
      denominator_type = sorted(den.split('*'))
    else:
      numerator_type = sorted(type_str.split('*'))
      denominator_type = []
    return numerator_type, denominator_type


  def _InsertKeys(self, class_name, data):
    
    for conversion_tuple in data:
      scale_factor = conversion_tuple[0]
      keys = conversion_tuple[1:]
      for key in keys:
        if key in self.convert_dict:
          raise DuplicateKey(key)
        self.convert_dict[key] = ConversionType(class_name, scale_factor)


class ConversionData(object):

  def __init__(self, numerator, denominator):
    """Constructor.

    Args:
      numerator: ConversionType
      denominator: ConversionType for a ratio, None otherwise
    """

    self.numerator = numerator
    self.denominator = denominator
    self.inverted = False
    self.numerator_name = self._BuildClassName(self.numerator, self.denominator)
    self.denominator_name = self._BuildClassName(self.denominator, self.numerator)

  def IsRatio(self):
    return self.denominator is not None

  def Invert(self):
    self.numerator, self.denominator = self.denominator, self.numerator
    self.numerator_name, self.denominator_name = self.denominator_name, self.numerator_name
    self.inverted = not self.inverted

  def _BuildClassName(self, numerator, denominator):

    name_list = [x.class_name for x in numerator]
    for check_name in [x.class_name for x in denominator]:
      if check_name in name_list:
        name_list.remove(check_name)
    return '*'.join(sorted(name_list))

class ConversionType(object):

  def __init__(self, class_name, scale_factor):
    self.class_name = class_name
    self.scale_factor = scale_factor
