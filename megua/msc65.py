# -*- coding: iso-8859-15 -*-

r"""
MSC 65D30 (1973-now) Numerical integration
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


from sage.all import *
from mathcommon import R15

"""
About polynomials

https://groups.google.com/group/sage-support/msg/4abc7d2c5ea97c2b?hl=pt
http://ask.sagemath.org/question/202/identification-polynomial

http://www.sagemath.org/doc/reference/sage/rings/polynomial/polynomial_ring_constructor.html
http://www.sagemath.org/doc/reference/sage/rings/polynomial/multi_polynomial_ring_generic.html
 P.<x,y,z> = PolynomialRing(QQ)
 P.random_element(2, 5)
-6/5*x^2 + 2/3*z^2 - 1
 P.random_element(2, 5, choose_degree=True)
-1/4*x*y - 1/5*x*z - 1/14*y*z - z^2

"""



def support_set(fun,a,b,n,rdecimals):
    """ 
    INPUT:
     - ``fun``: some expression or function.
     - ``a``: lower interval limit.
     - ``b``: upper interval limit.
     - ``n``: number of intervals.
    OUTPUT:
     -
    """
    h = (b-a)/n
    xset = [a + i * h for i in range(n+1)] #n+1points
    xyset = [ (xv,fun.subs(x=xv)) for xv in xset]
    return xyset


def random_basicLU3():
    """
    Generate random matrix A (3x3) and decomposition LU where A=LU without permutation.

    TODO: create a random dominant diagonal matrix module. MatrixSpace(QQ,3,3).
    Used on exercise: E65F05_LU_001. Any change could afect it.
    """

    A = random_matrix(ZZ,3,x=-3,y=3)
    #d = A.diagonal()
    A[0,0] = max( abs(A[0,0]) , abs(A[0,1])+abs(A[0,2])+ZZ.random_element(1,3) ) 
    A[1,1] = max( abs(A[1,1]) , abs(A[1,0])+abs(A[1,2])+ZZ.random_element(1,3) )
    A[2,2] = max( abs(A[2,2]) , abs(A[2,0])+abs(A[2,1])+ZZ.random_element(1,3) )

    import numpy as np
    import scipy.linalg as sl
    npA = np.matrix(A)
    npP,npL,npU = sl.lu(npA)
    #print "MATRIZ A=",A
    #print sl.lu(npA)
    L = matrix(R15,npL)
    U = matrix(R15,npU)
    return A,L,U



