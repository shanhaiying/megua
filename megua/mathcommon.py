"""
Several unrelated stuff for Meg.

AUTHORS:

- Pedro Cruz (2010-06): initial version

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

"""
Importing everything from sage.all

NOTE::

   Avoid this is very difficult or even impossible.
   For example:
      from sage.rings.real_double import RDF 
   does not work.

"""
from sage.all import *


#Sometimes needed.
x=var('x')


#For 4 digit numbers.
R15=RealField(15)


#Negative numbers in (...)
def showmul(x):
    """Old way of writing parentesis on negative numbers."""
    if x<0:
        return '(' + latex(x) + ')'
    else:
        return x

r"""
LOG function for high school
"""

def _LOG_latex(fun,x,base=None):
    if b==exp(1) or b is None:
        return r'\ln(%s)' % latex(x)
    else:
        return r'\log_{%s}(%s)' % (latex(base),latex(x))    

x,b=SR.var('x,b')
LOG_ = function('LOG', x, b, print_latex_func=_LOG_latex)


def LOG(x,base=None):
    r = log(x,base=base)
    if SR(r).denominator()==1:
        return r
    else:
        F = factor(x)
        l = [ factor_exponent * LOG_(x=factor_base,b=base) for (factor_base,factor_exponent) in F ]
        return add(l) 




#END mathcommon.py

