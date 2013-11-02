"""
Generic Mathematical routines for MEGUA.

AUTHORS:

- Pedro Cruz (2010-06): initial version
- Pedro Cruz (2013-11): added logb (and this module is now imported in ex.py)

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

r"""
Must import everything from sage.all::

    from sage.all import *

Avoiding this is impossible. For example::

      from sage.rings.real_double import RDF 

does not work.



.. test with: sage -t mathcommon.py


"""

from sage.all import *


#Sometimes needed.
x,y=var('x,y')


#For 4 digit numbers.
R15=RealField(15)


r"""
LOG function for "high school"

Use: usually ``log(105,base=10)`` is transformed by Sage (and many others) into ``log(105)/log(10)`` and sometimes this is not what we want to see as a result. This is an alternative.


Basic cases::

    sage: logb(e) #assume base=e
    1
    sage: logb(10,base=10)
    1
    sage: logb(1) #assume base=e
    0
    sage: logb(1,base=10) #assume base=e
    0
    sage: logb(e,base=10)
    logb(e, 10)
    sage: logb(10,base=e) #converted to Sage "log" function
    log(10) 
    sage: logb(sqrt(105)) #again, converted to Sage "log" function
    log(sqrt(105)) 

With and without factorization::

    sage: logb(3^5,base=10)  #no factorization
    logb(243, 10)
    sage: logb(3^5,base=10,factorize=True)  
    5*logb(3, 10)
    sage: logb(3^5*2^3,base=10) #no factorization
    logb(1944, 10)
    sage: logb(3^5*2^3,base=10,factorize=True)  
    5*logb(3, 10) + 3*logb(2, 10)

Latex printing of logb::

    sage: latex( logb(e) )
    1
    sage: latex( logb(1,base=10) )
    0
    sage: latex( logb(sqrt(105)) )
    \log\left(\sqrt{105}\right)
    sage: latex( logb(3^5,base=10) )
    \log_{10}(243)
    sage: latex( logb(3^5,base=10,factorize=True)  )
    5 \, \log_{10}(3)
    sage: latex( logb(3^5*2^3,base=10,factorize=True) )
    5 \, \log_{10}(3) + 3 \, \log_{10}(2)

"""

def _LOG_latex(fun,x,base=None):
    if b==e or b is None:
        return r'\ln(%s)' % latex(x)
    else:
        return r'\log_{%s}(%s)' % (latex(base),latex(x))    

x,b=SR.var('x,b')
LOG_ = function('logb', x, b, print_latex_func=_LOG_latex)


def logb(x,base=e,factorize=False):
    r"""logb is an alternative to log from Sage that keeps the base.

    Usually ``log(105,base=10)`` is transformed by Sage (and many others) 
    into ``log(105)/log(10)`` and sometimes this is not what we want to see as 
    a result. 

    The latex representation used ``\log_{base} (arg)``.

    INPUT:

    - ``x`` - the argument of log.

    - ``base`` - the base of logarithm.

    - ``factorize`` - decompose in a simple expression if argument if decomposable in prime factors.

    OUTPUT:

    - an expression based on ``logb``, Sage ``log`` or any other expression.

    """
    #e is exp(1) in sage
    r = log(x,base=base)
    if SR(r).denominator()==1:
        return r
    else:
        if factorize:
            F = factor(x)
        if factorize and type(F) == sage.structure.factorization_integer.IntegerFactorization:
            l = [ factor_exponent * LOG_(x=factor_base,b=base) for (factor_base,factor_exponent) in F ]
            return add(l) 
        else:
            return LOG_(x=x,b=base)






def showmul(x):
    """Deprecated:
    Old way of writing parentesis on negative numbers.
    """
    if x<0:
        return '(' + latex(x) + ')'
    else:
        return x



#END mathcommon.py

