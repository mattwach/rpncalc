# rpncalc Overview

Why another calculator app?  That is an excellent question.  Knowing that your
time is valuable, this short block of text will give you the "short sell" for
`rpncalc`.

First, what is an RPN calculator? It's a calculator that uses a stack.  Once
learned, it allows many people to enter expressions more quickly and with fewer
mistakes.  Check out more here
http://en.wikipedia.org/wiki/Reverse_Polish_notation

rpncalc takes your basic RPN calculator design and adds many user convenience
tools.  These include the following:

## Basic Examples

5 + 5

    |> 5 5 +
    y = 10.0  

sqrt(3 * 3 + 4 * 4).  A few different ways.

    |> 3 3 * 4 4 * + sqrt
    y = 5.0            

    |> 3 2 ** 4 2 ** + sqrt
    y = 5.0            

    |> 3 d * 4 d * + sqrt
    y = 5.0            

Area of a circle of radius 5

    |> 5 2 ** v:pi *
    y = 78.5398163397

## Robust Conversion Support

    Q: How many acres in a square mile?
    A: 1 mi*mi>acres
    y = 640.00000038    | 640.000
  
    Q: How many teaspoons in a pint?
    A: 1 pint>tsp
    y = 96.000000073    | 96.000
  
    Q: How many inch-pounds is 10 newton-meters
    A: 10 n*m>in*lbs
    y = 88.5043147656   | 88.504
  
    Q: How many gallons does a 25x25 yd pool that is 4 feet deep hold?
    A: 4 ft>yards 25 25 * * yard*yard*yard>gallon
    y = 168311.688488   | 168311.688

## Time and Duration Support

    Q: How many days until Christmas?
    A: 12/25 today -
       y = 11404800.0      |    132d
  
    Q: How fast do I need to run to finish a 5k in < 20 minutes?
    A: 20:00 5000 meters>miles /
       y = 386.24256       |       06:26
  
    Q: What time will it be 92 hours from now?
    A: now 92:00:00 +
       y = 1313783186.93   | 08/19/2011+12:46:26 (Fri)

## Money Support

    Q: Calculate my bill with 9% tax
    A: $ 1.24 5.34 6.78 sum 1.09 *
       y = 14.5624         |  $14.56
  
    Q: Help me balance my checkbook (cent entry mode)
    A: cent -4234 -1215 -500 -2738 50000 

## Hex and Binary Support

Support for hexidecimal data entry and views along with standard operators

    0x80 - Enter a hex number
    0b1000 - Enter a binary number

## Multiple Undo & Redo

Have a typo that blitzed your stack?  Walk backward and forward through stack
states.

## Readline Support

All the readline goodness, such as persistent history and robust key editing
support

## Variables and Macros

Automate and simplify complex and repetitive tasks

## Batch and Interactive Modes

Supports easy piping of results when run with arguments and an interactive
mode when run without arguments.


# Detailed Documentation

## Stack Management
    
This section lists basic stack management functions.  Note that the "Clipboard"
operations (especially pc, px, and pv) are intended to augment the ones listed 
below for more advanced stack manipulations.
    
### Supported Commands

    .                     Dump Stack (short form)
    ..                    Dump Full Stack
    d                     Duplicate y
    y                     Drop y
    D                     Clear Stack
    R                     Reverse Stack
    s                     Swap x <-> y
    rd                    Roll Stack Down
    ru                    Roll Stack Up

## Numbers
    
rpncalc accepts a number of different number formats.  In many cases, choosing a
special number format will change the display mode to support output of that
format.  See "Display Modes" for more information on how this works and how to
change the behavior.

Note that rpncalc supports both integer and floating point operations but
converts all numbers to floating point by default.  Use the 'mixed' and
'floats' commands to change this behavior.  You can also use 't' to swap
the number at the top of the stack between integer and floating point.
    
### Supported Commands

    1.0, 1., .5           Floating point numbers
    1e6, 2.5e-6           Scientific numbers
    0x36, -0x1234         Hexidecimal numbers
    1001b, -1001b         Binary numbers
    1, -512               Integers
    4d, 15d               Time Duration, in days
    1d14:23:12            Time Duration, DdHH:MM:SS
    534:12:00             Time Duration H:MM:SS
    536:45                Time Duration M:SS
    01/14, 2/12           Date (this year)
    01/14/2010, 2/12/1990  Date
    07/30/2006+16:00:00   Date
    now                   Current time and date
    today                 Current date
    mixed                 Allow integers and floats
    floats                Convert everything to floats (Default)
    t                     Convert float to int (and visa versa)

## Operators
    
This section lists rpncalc's basic operators (+, -, etc) with syntax.
    
### Supported Commands

    *                     x * y
    +                     x + y
    -                     x - y
    /                     x / y

## Logical Operators
    
Logical operators are useful for programmers, especially in low-level languages
such as C and assembly.  Operators use the same syntax as you would see in the C
language.  By default, Hex mode is enabled automatically after the first hex
value is pushed to the stack.
    
### Example
    
    0x1234 2 >>          # Right-shift
    1 5 << 0xFFFFFFFF ^  # create a bit mask for bit 5
    
### Supported Commands

    &                     x & y (Logical And)
    |                     x | y (Logical Or)
    ~                     ~y (Logical XOR)
    ^                     x ^ y (Logical XOR)
    >>                    x >> y (Logical Shift Right)
    <<                    x << y (Logical Shift Left)

## Scientific
    
This section lists operators that you you likely not see on a basic calculator
but would see on a "scientific" one.
    
### Supported Commands

    log10                 Log (base 10)
    log                   Log (base e)
    sq                    Square
    sqrt                  Square Root
    %                     x % y (Mod)
    !                     y! (Factorial)
    inv                   1.0/y (inverse)
    neg                   -y (negate)
    abs                   abs(y) (absolute value)
    **                    x ** y  (power of)

## Trigonometry
    
rpncalc can calculate trigonometry results in either degrees or radians.  Use
'deg' and 'rad' to change the mode.
    
### Supported Commands

    sin                   Sin
    cos                   Cos
    tan                   Tan
    asin                  Arc Sin
    acos                  Arc Cos
    atan                  Arc Tan
    deg                   Use degrees for trig functions
    rad                   Use radians for trig functions (default)

## Clipboard
    
rpncalc supports 3 types of clipboards:
    
### Standard Clipboard
    
You can copy between this clipboard and the stack with 'c' and 'v'.  You can
also 'cut' (pop) the last value on the stack to the clipboard with 'x'.

You can also use pc, px, and pv to cut. copy and paste values deeper in the
stack.  Here is an example that solves the quadratic formula without creating
named global variables.  The Formula is (sqrt(b*b - 4ac) - b)/(2a)
    
### Variable Clipboard
    
This clipboard allows you to cut copy and paste to variable names, you can
also dump the current set of defined variables for reference
    
#### Examples:
    
    now c:start_time   # copy the current time into 'start_time'
    now v:start_time - # Find the delta between 'start_time' and the current
                       # time
    l:v                # see what variables are currently defined
    
### Stack Clipboard
    
You can also copy and paste the entire clipboard with the capitalized
operators 'X', 'C' and 'V'.  Note that 'V' completely overwrites the existing
stack.  The 'X' operator is also useful for cleaning up miscellaneous values
from a stack after a calculation.
    
#### Examples:
    
This example uses named variables.  The risks here are typical global variable
risks, such as submacros using the same varible names or a macro wiping out
a variable you assumed was safe:
    
    m:quadratic1              \ # assume the stack contains a, b, c, in order
      x:c x:b x:a             \ # grab the variables
      v:b d * 4 v:a v:c * * - \ # w = b*b-4*a*c  stack is: w
      sqrt v:b -              \ # x = sqrt(w) - b
      2 v:a * /                 # x/2a completes the equation
    
This mixup uses positional stack commands to keep the relevant variables on the
stack instead.  This is safer but slightly more complex to implement
    
    m:quadratic2                 \ # assume the stack contains a, b, c in order
      1 pc v v *                 \ # grab b and push w=b*b, stack is a b c w
      3 pc v 2 px v 4 * * - sqrt \ # Calculate x = sqrt(w - 4ac), stack is a b x
      s -                        \ # calculate y=x-b, stact is a y
      s 2 * /                      # y/2a completes the equation
    
#### Supported Commands

    c                     Copy y
    x                     Cut (Pop) y
    v                     Paste (Push) y
    pc                    Copy stack[y], where x is index 0
    px                    Cut stack[y], where x is index 0
    pv                    Paste (insert) at stack[y], where x is index 0
    c:<varname>           Copy y to varname
    x:<varname>           Cut y to varname
    v:<varname>           paste varname to stack
    l:v                   Show all defined variables
    x                     Cut (Pop) y
    v                     Paste (Push) y
    C                     Copy stack
    X                     Cut stack
    V                     Paste stack

## Undo/Redo
    
In interactive mode, every time you hit [Enter], rpncalc snapshots the state of
your stack (if it changed) before executing any commands.  You can then use 'u'
and 'r' to step forward and backward though historical stack states.  This can
be used to correct mistakes or (slightly) abused to assist with calculations.
    
### Supported Commands

    r                     Redo last undo (only if it was last command)
    u                     Undo to last [Enter] state

## Exiting
    
You can exit with 'q'.  [Ctrl-D] also works.
    
## Misc
    
Miscellaneous functions include showing help, and sourcing files that contain
commands.
    
### Supported Commands

    s:<path>              Execute commands found in <path>
    ?                     Short Help
    ??                    Verbose Help
    ???                   Full Documentation

## Statistics
    
Statistics funtions are listed here.  Statistics function treat the entire stack
as a list of relevant data points.  To help manage this, the "Clipboard"
function 'C', 'X' and 'V' can be useful for storeing and retrieving the stack.
    
### Example:
    
    batch
    5 0.67 36 37 C
      37.0           
    sum
      78.67          
    V mean
      19.6675        
    V median
      36.0           
    
### Supported Commands

    sum                   Sum All Arguments
    mean                  Mean All Arguments
    median                Median All Arguments

## Display Modes
    
On startup, rpncalc will show results in either floating point or integer format, like
this:
    
    10.0  42.0
    x = 1234.0         
    y = 3.14159265359
    
There are, however, a number of optional display modes available that  also
show the data in a converted format.  Here is the basic catalogue:
    
    3 fixed # Fixed Mode (variable number of digits):
    
    10.0  42.0
    x = 1234.0          | 1234.000
    y = 3.14159265359   | 3.142
    
    hex # Hexidecimal
    
    10.0  42.0
    x = 1234.0          | 0x04D2
    y = 3.14159265359   | 0x03
    
    bin # Binary
    
    0b1000 0b1001
    x = 8               | 0b1000
    y = 9               | 0b1001
    
    dur # Convert from seconds to time duration
    
    10.0  42.0
    x = 1234.0          |       20:34
    y = 3.14159265359   |       00:03
    
    date # Assume epoch time
    
    10.0  42.0
    x = 1234.0          | 12/31/1969+16:20:34 (Wed)
    y = 3.14159265359   | 12/31/1969+16:00:03 (Wed)
    
    time # Guess if this is a duration or epoch time
    
    10.0  42.0
    x = 1234.0          |       20:34
    y = 3.14159265359   |       00:03
    
    $ # Money display
    
    10.0  42.0
    x = 1234.0          |  $1234.00
    y = 3.14159265359   |  $3.14
    
    cent # Cent-wise money
    
    10.0  42.0
    x = 1234.0          |  $12.34
    y = 3.14159265359   |  $0.03
    
Note that only x and y are converted by default.  Use the .. command to see the whole stack converted:
    
    ..
    
    s4 = 10.0            |  $0.10
    s3 = 42.0            |  $0.42
    s2 = 1234.0          |  $12.34
    s1 = 3.14159265359   |  $0.03
    
To turn off special display modes, use the normal command:
    
    normal
    
    10.0  42.0
    x = 1234.0         
    y = 3.14159265359
    
### Automatic mode changes
    
rpncalc will automatically enable certain display modes based on your input patterns under
these conditions:
    
   - If you enter a hexidecimal number or use a logical operator (e.g. 0x1234), 
     hex mode is auto-enabled
   - If you enter a duration (e.g. 2:47:56), duration mode is auto-enabled
   - If you enter a time or date (e.g. 01/01/2010), time mode is auto-enabled
   - If you do any conversions, fixed mode is auto-enabled
    
To disable auto-enabling of modes, use the 'manual' command.  Use the 'auto'
command to re-enable display mode auto-enabling.
    
## Batch and Interactive Modes
    
Batch mode will only print out the formatted result of the bottom of the stack.
Interactive mode prints a more compete stack view.  Batch is default when
running rpncalc from the command line (e.g. rpncalc '4 5 +'), while
interactive is the interactive default.
    
### Example
    
    batch 4 5 +
      9.0            
    interactive 5 6 +
     x = 9.0            
     y = 11.0
    
#### Supported Commands

    fixed                 Turn on fixed-width mode (y holds sig digits)
    hex                   Turn on hexadecimal display
    bin                   Turn on binary display
    dur                   Turn on duration (time) display
    date                  Turn on date display
    time                  Turn on date or duration (auto select) display
    $                     Turn on Money Display mode
    cent                  Turn on Cent-Wise Money Display mode
    normal                Turn off special display modes
    batch                 Only output formatted results
    interactive           Show interactive stack dump
    manual                Do not automatically change display modes
    auto                  Automatically change display modes based on input syntax (default)

## Expression Debugging
    
Normally, when stack terms are entered on the same line, there is no output
printed until the last element on the line is reached.  When 'debug' is
activated, the stack is printed after each operator.  This can be useful when
defining a complex macro or investigating a suspicious calculation result.
    
### Example
    
    |> m:dist d * s d * + sqrt
    Defined macro: dist
    |> 3 4 @dist
      y = 5.0            
    |> X debug 3 4 @dist
      Stack Cut To Clipboard
      Exec: debug
  
      Exec: 3
      y = 3.0            
      
      Exec: 4
      x = 3.0            
      y = 4.0            
      
      Exec: d
      3.0
      x = 4.0            
      y = 4.0            
      
      Exec: *
      x = 3.0            
      y = 16.0           
      
      Exec: s
      x = 16.0           
      y = 3.0            
      
      Exec: d
      16.0
      x = 3.0            
      y = 3.0            
      
      Exec: *
      x = 16.0           
      y = 9.0            
      
      Exec: +
      y = 25.0           
      
      Exec: sqrt
      
      Exec: @dist
      
      y = 5.0     
    
#### Supported Commands

    debug                 Turn on expression debug (show all stack steps)
    nodebug               Turn off expression debug

## Type Conversion
    
rpncalc has a fairly robust conversion mode that can handle conversion between
different ratios of products or inverses.  Some good examples of this are:
    
### Examples:
    
    10 mph>min/mile
    5 gallons>in*in*in
    90 kwh>kj
    
The basic pattern is:
    
    old>new
    
Where wither old or new can be a single unit type or a product of types.  The
conversion engine is smart enough to invert old, if needed for a unit match.
The engine is also smart enough to detect unit mismatch, for example:
    
    1 acre>feet  (Error)
    1 acre>feet*feet (Ok)
    
use the `l:c` command to list all known conversion types.
    
### Supported Commands

    mph>min/mile, yard*yard>ft*ft  Convert between number types
    l:c                   Dump all known conversion keys

## Macros and Conditionals
    
Macros and conditionals allow for simple programming concepts to be implemented.
The m: syntax is used to define a macro.  Later @macro can be used to execute
it.  The stack is used for argument passing and return values for the most part,
although you can also use the clipboard to hold variables.  Be aware that these
variables are global though!

For an example, let's first define a macro that can produce the next fibonacci number
in a series, assuming that the pattern is already seeded with 0, 1 on the stack:
    
    m:fib_next \
      d 2 pc v +  # z = x+y
    
Now to complete the concept by defining fibonacci to set up the stack initially
and `fib_test` and `fib_iter` helper macros to push the process along
    
    m:fibonacci   \
        2 - x:i   \ # Subtract 2 from arg and push 
        0 1       \ # Push the first 2 numbers in the series
        @fib_test   # kick off the iterator
    
    m:fib_test \
        v:i 0 > ?fib_iter  # If iterator is not expired then make another digit
    
    m:fib_iter      \
        @fib_next   \ # Make the digit
        v:i 1 - x:i \ # Decrement the counter
        @fib_test     # See if there is more to do
    
    15 @fibonacci # Generate the first 15 numbers
    
As you can see, programming with this calculator is possible but complex
implementations are beyond the current goals.

Note that turning on debug mode can be a valuable aid in testing macros.
    
### Supported Commands

    m:<name> x y z...     Define a macro
    @<name>               Execute a defined macro
    ?<name>               Pop y and execute <macro> only if non-zero
    l:m                   List defined macros
    >                     1 if x > y, 0 otherwise
    <                     1 if x < y, 0 otherwise
    >=                    1 if x >= y, 0 otherwise
    <=                    1 if x <= y, 0 otherwise
    ==                    1 if x == y, 0 otherwise
    !=                    1 if x != y, 0 otherwise
    not                   1 if y == 0, 0 otherwise
