r"""
This module defines functions that use R software for statistics.

AUTHORS:

- Pedro Cruz (2014-03-07): initial version

LINKS:

 - http://www.sagemath.org/doc/reference/interfaces/sage/interfaces/r.html


"""

"""
import rpy2
import rpy2.robjects as robjects
stemf = robjects.r['stem']
runif = robjects.r['runif']
rprint =robjects.r['print'] 
buf = []
def f(x):
    # function that append its argument to the list 'buf'
    buf.append(x)

# output from the R console will now be appended to the list 'buf'
rpy2.rinterface.setWriteConsole(f)

stemf( runif(int(100)) )

rprint( runif(int(100)) )

#date = rpy2.rinterface.baseenv['date']
#rprint = rpy2.rinterface.baseenv['print']
#rprint("date()")

# the output is in our list (as defined in the function f above)
print(buf)

print ''.join(buf)


"""
