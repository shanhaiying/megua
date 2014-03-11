# -*- coding: utf-8 -*-
r"""
This module defines functions that use R software for statistics.

AUTHORS:

- Pedro Cruz (2014-03-07): initial version

LINKS:

 - http://www.sagemath.org/doc/reference/interfaces/sage/interfaces/r.html

"""

import rpy2
import rpy2.robjects as robjects

#from sage.rings.integer import Integer

def r_stem(p_list):
    """
    Return a string with a stem-and-leaf diagram based on R.

    INPUT:

    - `p_list': a python list
    
    OUTPUT:

       Return string with the diagram.

    EXAMPLES:

       sage: from megua.cr import r_stem2
       sage: r_stem( [random() for _ in range(20)] ) #random
       u'\n  O ponto decimal est\xe1 1 d\xedgitos para a esquerda de |\n\n  0 | 283\n  2 | 334\n  4 | 468117\n  6 | 3348169\n  8 | 5\n\n'
       sage: r_stem( [int(100*random()) for _ in range(20)] ) 
       u'\n  O ponto decimal est\xe1 1 d\xedgito para a direita de |\n\n  0 | 60\n  2 | 1660\n  4 | 169\n  6 | 03457\n  8 | 091779\n\n'
    """

    print "Entrou no r_stem"

    stemf = robjects.r['stem']

    buf = []
    def f(x):
        # function that append its argument to the list 'buf'
        buf.append(x)

    # output from the R console will now be appended to the list 'buf'
    rpy2.rinterface.setWriteConsole(f)


    if type(p_list[0])==int: # or type(p_list[0])==sage.rings.integer.Integer:
        stemf( robjects.IntVector(p_list) )
    else:
        stemf( robjects.FloatVector(p_list) )



    #Parsing: The decimal point is 1 digit(s) to the right of the |
    #The answer is a list of string in the "buf" variable.


    #if buf[1] == '  The decimal point is ':
    buf[1] = "  O ponto decimal está "
    
    #get space position after the number.
    sp = buf[2].index(' ')

    if 'left' in buf[2]:
        sideword = 'esquerda'
    else:
        sideword = 'direita'


    if buf[2][:sp]=='1':
        buf[2] = buf[2][:sp] + " dígito para a %s de |\n\n" % sideword
    else:
        buf[2] = buf[2][:sp] + " dígitos para a %s de |\n\n" % sideword

    jbuf = ''.join(buf)

    #print jbuf
    #print type(jbuf)

    return jbuf



if __name__=='__main__':

    from random import random
    l = [int(100*random()) for _ in range(20)]
    print l
    b = r_stem2( l ) 
    #b = r_stem( [random() for _ in range(30)] )
    print b


