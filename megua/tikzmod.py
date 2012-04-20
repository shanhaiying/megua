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
  

def tikz_getpointsstr(pointlist):
    return join( [ str( (round(p[0],3),round(p[1],3)) ) for p in pointlist ], ' ' )



