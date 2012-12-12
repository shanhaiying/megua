#-*- coding: iso-8859-15 -*-
r"""
MSC60   (1940-now) Probability theory and stochastic processes
http://www.ams.org/mathscinet/freeTools.html

Helper routines.

AUTHORS:

- Pedro Cruz (2010-04-06): initial version


Examples:

::
    sage: None

"""

#*****************************************************************************
#       Copyright (C) 2010 Pedro Cruz <PedroCruz__@__ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

#melhorar meg.ex separando em funções para exercícios e randoms
#Does this work:
#from meg.ur import ur
#or this:
from ur import ur

from sage.all import RealNumber

def random_alpha():
    """
    Returns a random alpha value (significance level). 
    (Used in statistics).

    EXAMPLES::

    sage: from msc60 import random_alpha
    sage: random_alpha()
    (5.00000000000000, 0.0500000000000000)

    """
    #Significance Level
    d = ur.iunif(0,3)
    if d==0:
        return (RealNumber('0.1'),RealNumber('0.001'))
    elif d==2:
        return (RealNumber('1'),RealNumber('0.01'))
    elif d==3:
        return (RealNumber('5'),RealNumber('0.05'))
    else:
        return (RealNumber('10'),RealNumber('0.1'))


def Percent(value):
    """
    Given an alpha or 1-alpha value return the textual version without %.

    EXAMPLES::

    sage: from msc60 import Percent
    sage: Percent(0.1) + "%"
    '10%'
    sage: Percent(0.12) + "%"
    '12%'
    """
    value = float(value)
    if value == 0.01:
        return r"1"
    elif value == 0.05:
        return r"5"
    elif value == 0.10:
        return r"10"
    elif value == 0.90:
        return r"90"
    elif value == 0.95:
        return r"95"
    elif value == 0.975:
        return r"97.5"
    elif value == 0.99:
        return r"99"
    elif value == 0.995:
        return r"99.5"
    else:
        return r"{0:g}".format(value*100)




#def random_pmf(n=6):
#    #restart random number generator
#    # See class Exercise for seed.activate()
#    #Support (random)
#    x0 = ur.iunif(-2,3) #start x_0
#    h = ur.runif(0,2,1) #h space between
#    #n = iunif(4,6) # fixed for start
#    values = [x0 + h * i for i in range(n)]
#    #Probabilities (random)
#    lst = [runif(0,1,1) for i in range(n)]
#    sumlst = sum(lst)#weighted sum
#    probabilities = [fround(i/sumlst,2) for i in lst]
#    #Correction
#    newsum = sum(probabilities)
#    probabilities[0] =  probabilities[0] + (1-newsum)
#    return {'values': values,'probabilities': probabilities}



 
