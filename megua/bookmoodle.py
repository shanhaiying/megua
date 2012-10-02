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



class MoodleBook(BookBase):
    r"""
    Set of routines for exercise templating to the web using latex for mathjax engine.

    INPUT::

    - ``filename`` -- filename where the database is stored.

    This module provides means to use a database of exercises that can be seen as a book of some author or authors.
    """

    def __init__(self,filename=None,natlang='pt_pt'):
        r"""

        INPUT::
        - ``filename`` -- filename where the database is stored.
        - ``natlang`` -- natural language ('pt_pt', etc).

        """
        BookBase.__init__(self,filename=filename,natlang=natlang,markuplang='moodle')



    def __str__(self):
        return "MoodleBook('%s') for %s and markup language %s" % (self.local_store_filename,self.megbook_store.natural_language,self.megbook_store.markup_language)


    def __repr__(self):
        return "MoodleBook('%s')" % (self.local_store_filename)







#end class MegBookWeb

