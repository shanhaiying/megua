r"""
TikZmod -- Routines to convert sage plots into latex TikZ markup.

AUTHORS:

- Pedro Cruz (2012-04): initial version

"""


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


from sage.all import *

R20 = RealField(20)

def getpoints_str(pointlist):
    return join( [ str( ( R20(p[0]), R20(p[1]) ) ) for p in pointlist ], ' ' )



