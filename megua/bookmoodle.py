r"""
bookmoodle.py -- Build your own database of exercises to the web.

bookmoodle is a template for creating exercises for moodle in xmlmoodle standard.

AUTHORS:

- Pedro Cruz (2012-10): initial version.


"""


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

#Python Modules
import re
import codecs


#Megua modules:
from bookbase import *


#TODO Is it necessary to import other libs?



class BookMoodle(BookBase):
    r"""
    Set of routines for exercise templating to the web using latex for mathjax engine.

    INPUT::

    - ``filename`` -- filename where the database is stored.

    This module provides means to use a database of exercises that can be seen as a book of some author or authors.

    Examples of use:

    .. test with: sage -python -m doctest bookbase.py

    Create or edit a database::

       >>> from all import *
       >>> meg = BookMoodle(r'.testoutput/moodle.sqlite')


    Save a new or changed exercise::

       >>> meg.save(r'''
       ... %Summary Primitives
       ... Here one can write few words, keywords about the exercise.
       ... For example, the subject, MSC code, and so on.
       ...   
       ... %Problem Simple Primitive
       ... What is the primitive of ap x + bp@() ?
       ... 
       ... %Answer
       ... The answer is prim+C, with C a real number.
       ... 
       ... class E28E28_pdirect_001(Exercise):
       ... 
       ...     def make_random(self):
       ...         self.ap = ZZ.random_element(-4,4)
       ...         self.bp = self.ap + QQ.random_element(1,4)
       ... 
       ...     def solve(self):
       ...         x=SR.var('x')
       ...         self.prim = integrate(self.ap * x + self.bp,x)
       ... ''',dest=r'.testoutput')


    """

    def __init__(self,filename=None,natlang='pt_pt'):
        r"""

        INPUT::
        - ``filename`` -- filename where the database is stored.
        - ``natlang`` -- natural language ('pt_pt', etc).

        """
        BookBase.__init__(self,filename=filename,natlang=natlang,markuplang='moodle')



    def __str__(self):
        return "BookMoodle('%s') for %s and markup language %s" % (self.local_store_filename,self.megbook_store.natural_language,self.megbook_store.markup_language)


    def __repr__(self):
        return "BookMoodle('%s')" % (self.local_store_filename)


    def export(self,what=[],repetitions=5,filename=None, header='')
        """Export all or a set of exercises to a file in Moodle XML format.
        """
        




#end class BookMoodle

