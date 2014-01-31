"""
Matplotlib graphics for MEGUA.

AUTHORS:

- Pedro Cruz (2014-01): initial version

"""


#*****************************************************************************
#       Copyright (C) 2014 Pedro Cruz <PedroCruz@ua.pt>
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

import jinja2


"""
the following code is about templating.

TODO: incorporate other templating code into one module.

"""

#Templating (with Jinja2)
natlang = 'pt_pt'
if os.environ.has_key('MEGUA_TEMPLATE_PATH'):
    TEMPLATE_PATH = os.environ['MEGUA_TEMPLATE_PATH']
else:
    from pkg_resources import resource_filename
    TEMPLATE_PATH = os.path.join(resource_filename(__name__,''),'template',natlang)

#print "Templates in mathcommon.py:  '%s' language at %s" % (natlang,TEMPLATE_PATH)
env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH))




import numpy as np
import matplotlib.pyplot as plt
from pylab import savefig

    def sage_graphic(self,graphobj,varname,dimx=5,dimy=5, arrows=False):
        """This function is to be called by the author in the make_random or solve part.
        INPUT:

        - `graphobj`: some graphic object.

        - `varname`: user supplied string that will be part of the filename.

        - `dimx` and `dimy`: size in centimeters.

        - `arrows`: if ``arrows=True`` **try** to put arrows in the axis extremes.
        """ 
        #Arrows #TODO: this is not working
        if arrows:
            xmin = graphobj.xmin()
            xmax = graphobj.xmax()
            ymin = graphobj.ymin()
            ymax = graphobj.ymax()
            xdelta= (xmax-xmin)/10.0
            ydelta= (ymax-ymin)/10.0
            graphobj += arrow2d((xmin,0), (xmax+xdelta, 0), width=0.1, arrowsize=3, color='black') 
            graphobj += arrow2d((0,ymin), (0, ymax+ydelta), width=0.1, arrowsize=3, color='black') 

        gfilename = '%s-%s-%d'%(self.name,varname,self.ekey)
        #create if does not exist the "image" directory
        os.system("mkdir -p images") #The "-p" ommits errors if it exists.
        if arrows:
            #TODO: clip figure for avoid -->---  extra ---
            graphobj.save("images/"+gfilename+'.png',figsize=(dimx/2.54,dimy/2.54),dpi=100)
        else:
            graphobj.save("images/"+gfilename+'.png',figsize=(dimx/2.54,dimy/2.54),dpi=100)
        self.image_list.append(gfilename) 
        return r"<img src='images/%s.png'></img>" % gfilename




def doublebar_chart(sampleA,SampleB):

    N = 5
    menMeans = (20, 35, 30, 35, 27)
    menStd =   (2, 3, 4, 1, 2)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)

    womenMeans = (25, 32, 34, 20, 25)
    womenStd =   (3, 5, 2, 3, 3)
    rects2 = ax.bar(ind+width, womenMeans, width, color='y', yerr=womenStd)

    # add some
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )

    ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.show()

    savefig("fig.png")


N = 5
menMeans = (20, 35, 30, 35, 27)
menStd =   (2, 3, 4, 1, 2)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)

womenMeans = (25, 32, 34, 20, 25)
womenStd =   (3, 5, 2, 3, 3)
rects2 = ax.bar(ind+width, womenMeans, width, color='y', yerr=womenStd)

# add some
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )

ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.show()

savefig("fig.png")


