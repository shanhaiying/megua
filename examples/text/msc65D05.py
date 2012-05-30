# -*- coding: iso-8859-15 -*-

r"""
MSC 65D05 (1973-now) Interpolation
http://www.ams.org/mathscinet/freeTools.html

AUTHORS:

- Pedro Cruz (2011-01-11): initial version

"""

#*****************************************************************************
#       Copyright (C) 2010 Pedro Cruz
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

# Main package, ex module
#from meg.ex import Exercise, iunif, showmul,var,exp, runif
from meg.ex import *

# Module with routines for msc65 Numerical analysis (in this folder)
from msc65  import *

class E65D05_forwarddifference_001(Exercise):
    """
    Lagrange interpolation of degree 2
    Solved by forward difference.
    Integers

    Authors:
    - Pedro Cruz (2010) initial version

    """

    def make_random(self,seed):
        #Call base class function
        Exercise.make_random(self,seed)

        # Data Generation
        
        #Support    
        self.inh  = runif(0.5,1.5,1)
        self.inx0 = iunif(-5,5)
        self.inx1 = self.inx0+self.inh
        self.inx2 = self.inx1+self.inh

        self.iny0 = iunif(-1,5)
        self.iny1 = iunif(-1,5)
        self.iny2 = iunif(-1,5)

        #Generate x in the domain x0..x2
        self.inxv = runif(self.inx0,self.inx2,1)

        
    def solve(self):
        #Call base class
        Exercise.solve(self)
        #Solve
        self.ondp1 = self.iny1-self.iny0
        self.ondp2 = self.iny2-self.iny1
        self.ondp3 = self.ondp2 - self.ondp1

        self.onresultexact =  self.iny0 + self.ondp1 * (self.inxv-self.inx0) + self.ondp3 / 2 * (self.inxv-self.inx0)* (self.inxv-self.inx1)
        self.onresultapprox =  self.onresultexact.n(digits=4)
        
        self.onx0 = showmul(self.inx0)
        self.onx1 = showmul(self.inx1)
        
e65D05_forwarddifference_001 = E65D05_forwarddifference_001('e65D05_forwarddifference_001')



class E65D05_forwarddifference_002(Exercise):
    """
    Lagrange interpolation of degree 2
    Solved by forward difference.
    Real numbers with 2 decimals.
    
    Authors:
    - Pedro Cruz (2010) initial version

    """

    def make_random(self,seed):
        #Call base class function
        Exercise.make_random(self,seed)

        # Data Generation
        
        #Support       
        self.inh  = runif(0.5,1.5,1)
        self.inx0 = iunif(-5,5)
        self.inx1 = self.inx0+self.inh
        self.inx2 = self.inx1+self.inh

        self.iny0 = iunif(-1,5)
        self.iny1 = iunif(-1,5)
        self.iny2 = iunif(-1,5)

        #Generate x in the domain x0..x2
        self.inxv = runif(self.inx0,self.inx2,1)

        
    def solve(self):
        #Call base class
        Exercise.solve(self)
        #Solve
        self.ondp1 = self.iny1-self.iny0
        self.ondp2 = self.iny2-self.iny1
        self.ondp3 = self.ondp2 - self.ondp1

        self.onresultexact =  self.iny0 + self.ondp1 * (self.inxv-self.inx0) + self.ondp3 / 2 * (self.inxv-self.inx0)* (self.inxv-self.inx1)
        self.onresultapprox =  self.onresultexact.n(digits=4)
        
        self.onx0 = showmul(self.inx0)
        self.onx1 = showmul(self.inx1)
        
e65D05_forwarddifference_002 = E65D05_forwarddifference_002('e65D05_forwarddifference_002')




class E65D05_forwarddifference_003(Exercise):
    """
    Lagrange interpolation of degree 2
    Solved by forward difference.
    Real numbers with 2 decimals.
    Function randomly selected.
    
    Authors:
    - Pedro Cruz (2010) initial version

    """

    def make_random(self,seed):
        #Call base class function
        Exercise.make_random(self,seed)

        # Data Generation
        
        #Support    
        #x=var('x')   
        self.infx = lambda x : exp(4-2*x)
        self.inh  = iunif(1,3)
        self.inx0 = iunif(-2,5)
        self.inx1 = self.inx0+self.inh
        self.inx2 = self.inx1+self.inh

        #Generate x in the domain x0..x2
        self.inxv = runif(self.inx0,self.inx2,1)

        
    def solve(self):
        #Call base class
        Exercise.solve(self)
        #Solve
        R15 = RealField(15)
        x=var('x')
        self.onfx = latex(self.infx(x))
        self.ony0 = self.infx(R15(self.inx0))
        self.ony1 = self.infx(R15(self.inx1))
        self.ony2 = self.infx(R15(self.inx2))

        self.ondp1 = self.ony1-self.ony0
        self.ondp2 = self.ony2-self.ony1
        self.ondp3 = self.ondp2 - self.ondp1

        self.onresult =  self.ony0 + self.ondp1 / self.inh * (self.inxv-self.inx0) + self.ondp3 / (2*self.inh**2) * (self.inxv-self.inx0) * (self.inxv-self.inx1)
        
        self.onx0 = showmul(self.inx0)
        self.onx1 = showmul(self.inx1)
        
        self.onfxv = self.infx(self.inxv)
        self.onrelativo = (abs( (self.onresult-self.onfxv) / self.onfxv ))

e65D05_forwarddifference_003 = E65D05_forwarddifference_003('e65D05_forwarddifference_003')

