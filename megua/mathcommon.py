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



#END mathcommon.py

