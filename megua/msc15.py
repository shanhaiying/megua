r"""
Group together matrix and linear algebra routines (MSC 15). 

See MSC 15 at http://www.ams.org/mathscinet/msc/msc2010.html.

AUTHORS:

- Pedro Cruz (2012-04-10): initial version.


EXAMPLES

.. test with: sage -t msc15.py

"""



#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


from sage.all import *  


def before_minor(M,pivot_row,pivot_col):
    """
    A minor is the determinant of a submatrix of M.
    This routine gives the matrix to which the determinant is calculated.
    
    INPUT:
        
    - ``M``: a square matrix n by n.

    - ``pivot_row, pivot_col``: row and column nunbers (0 to n-1).
    
    OUTPUT:
        
        The submatrix of ``M`` extracting row ``pivot_row`` and column ``pivot_col``.

    EXAMPLES::

       sage: from msc15 import before_minor 
       sage: M = matrix(ZZ, [ [  1, -25,  -1,   0], [  0,  -2,  -5,  -2], [  2,   1,  -1,   0], [  3,   1,  -2, -13] ]); M
       [  1 -25  -1   0]
       [  0  -2  -5  -2]
       [  2   1  -1   0]
       [  3   1  -2 -13]
       sage: before_minor(M,0,0)
       [ -2  -5  -2]
       [  1  -1   0]
       [  1  -2 -13]
       sage: before_minor(M,0,3)
       [ 0 -2 -5]
       [ 2  1 -1]
       [ 3  1 -2]
       sage: before_minor(M,3,3)
       [  1 -25  -1]
       [  0  -2  -5]
       [  2   1  -1]
       sage: before_minor(M,3,0)
       [-25  -1   0]
       [ -2  -5  -2]
       [  1  -1   0]
       sage: before_minor(M,0,2)
       [  0  -2  -2]
       [  2   1   0]
       [  3   1 -13]
       sage: before_minor(M,3,2)
       [  1 -25   0]
       [  0  -2  -2]
       [  2   1   0]
       sage: before_minor(M,2,0)
       [-25  -1   0]
       [ -2  -5  -2]
       [  1  -2 -13]
       sage: before_minor(M,2,3)
       [  1 -25  -1]
       [  0  -2  -5]
       [  3   1  -2]
       sage: before_minor(M,1,1)
       [  1  -1   0]
       [  2  -1   0]
       [  3  -2 -13]


    AUTHORS:
    - Pedro Cruz (2012/April)
    - Paula Oliveira (2012/April)
    
    """
    
    nrows,ncols = M.parent().dims()
    
    #put values in 0-n-1 range.
    nrows -= 1
    ncols -= 1
    
    if pivot_row==0 and pivot_col==0:
        #pivot is at left top corner
        return M[1:,1:]

    elif pivot_row==0 and pivot_col==ncols:
        #pivot is at right top corner
        return M[1:,:-1]

    elif pivot_row==nrows and pivot_col==ncols: 
        #pivot is at right bottom corner
        return M[:-1,:-1]

    elif pivot_row==nrows and pivot_col==0:     
        #pivot is at left bottom corner
        return M[:-1,1:]

    elif pivot_row==0: 
        #pivot is at first row any other col
        M.subdivide( 1, [pivot_col,pivot_col+1])
        return block_matrix( [ [M.subdivision(1,0),M.subdivision(1,2)]], subdivide=False)

    elif pivot_row==nrows: 
        #pivot is at last row any other col
        M.subdivide( nrows, [pivot_col,pivot_col+1])
        return block_matrix( [ [M.subdivision(0,0),M.subdivision(0,2)]], subdivide=False)

    elif pivot_col==0:
        #pivot is at column 0 and any other row
        M.subdivide( [pivot_row,pivot_row+1], 1)
        return block_matrix( [ [M.subdivision(0,1)],[M.subdivision(2,1)]], subdivide=False)

    elif pivot_col==ncols: 
        #pivot is at last column and any other row
        M.subdivide( [pivot_row,pivot_row+1], ncols)
        return block_matrix( [ [M.subdivision(0,0)],[M.subdivision(2,0)]], subdivide=False)

    else:
        M.subdivide( [pivot_row,pivot_row+1], [pivot_col,pivot_col+1])
        return block_matrix( [ [M.subdivision(0,0),M.subdivision(0,2)], [M.subdivision(2,0),M.subdivision(2,2)] ], subdivide=False)


