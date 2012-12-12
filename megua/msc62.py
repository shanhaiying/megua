# -*- coding: iso-8859-15 -*-

r"""
MSC 62   (1940-now) Statistics
http://www.ams.org/mathscinet/freeTools.html

AUTHORS:

- Pedro Cruz (2010-11-16): initial version

"""

#*****************************************************************************
#       Copyright (C) 2010 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#Talvez isto não seja útil porque all.py contém tudo!
#importar tudo do primeiro grupo msc que abrange a estatística
#from meg.msc60.msc60 import *
#esclarecer o ststistics.py em meg/




#Random numbers from R using RPy2
# 1. Always do casts to python rpy2 commands.
# 2. To do: study how does rpy2 works.
import rpy2.robjects as robjects

def qt(p,df,prec=None):
    """
    Quantil from a t-student distribution.

    NOTES:

    * Based on RPy2 module (seed is from RPy2).

    INPUT:

    - ``p`` -- probability.
    - ``df`` -- degree of freedom (distribution parameter).
    - ``prec`` -- number of decimal digits (default all).

    OUTPUT:
        Quantil from t-student distribution.

    EXAMPLES::

        sage: from msc62 import qt
        sage: qt(0.95,12)
        1.7822875556493196
        sage: qt(0.95,12,2)
        1.78

    """
    #qt(p, df, ncp, lower.tail = TRUE, log.p = FALSE)
    qt = robjects.r['qt']
    res = qt(float(p),int(df))[0]
    if prec:
        res = round(res,prec)
    return res

def pnorm(x,mean,stdev,prec=None):
    """
    Probability of a normal distribution(mean, stdev).

    NOTES:

    * Based on RPy2 module (seed is from RPy2).

    INPUT:

    - ``x`` -- some quantil.
    - ``mean`` -- mean of the normal distribution.
    - ``stdev`` -- standar deviation.
    - ``prec`` -- number of decimal digits (default all).

    OUTPUT:
        :math:``P(X<=x) where X~Norm(mean,stdev).

    EXAMPLES::

        sage: from msc62 import pnorm
        sage: pnorm(0,0,1)
        0.5
        sage: pnorm(1.644854,0.0,1.0)
        0.95000003847458692

    """
    #qt(p, df, ncp, lower.tail = TRUE, log.p = FALSE)
    pnorm = robjects.r['pnorm']
    res = pnorm(float(x),float(mean),float(stdev))[0]
    if prec:
        res = round(res,prec)
    return res


