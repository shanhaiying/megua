r"""
MegBookWeb -- Build your own database of exercises to the web.

AUTHORS:

- Pedro Cruz (2012-06): initial version.


"""


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

#Meg modules:
from megbookbase import *

#TODO Is it necessary to import other libs?



class MegBookWeb(MegBookBase):
    r"""
    Set of routines for exercise templating to the web.

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
        MegBookBase.__init__(self,filename=filename,natlang=natlang,markuplang='web')



    def __str__(self):
        return "MegBookWeb('%s') for %s and markup language %s" % (self.local_store_filename,self.megbook_store.natural_language,self.megbook_store.markup_language)


    def __repr__(self):
        return "MegBookWeb('%s')" % (self.local_store_filename)


    def is_exercise_ok(self,row,dest,silent=True):
        r"""
        Check if exercise is ready for compilation and for python/sage errors.
        """

        # --------------------------------
        # Testing the new python class for 
        # programming errors:
        #     syntax and few instances execution. 
        # -------------------------------
        if not self.exercise_pythontest(row,silent=silent):
            return False


        # --------------------------
        # Testing html compilation. TODO: how to do this?
        # --------------------------
        #if not self.exercise_htmltest(row,dest,silent=silent):
        #    return False

        # Exercise Ok
        return True



    def search_print_row(self,exrow):
        r"""
        This is an helper function of ``Meg.search`` function to print the contents of a search.
        Not to be called by meg user.

        INPUT:

        - ``exrow`` -- an sqlite row structure_ where fields are accessible by name.

        OUTPUT:

        - html or text.

        NOTES:
            unicode is in utf-8 -> string
            http://en.wikipedia.org/wiki/ISO/IEC_8859-1
            Sage html() requires string.
        """
    
        sname = 'Exercise name %s' % exrow['owner_key'].encode('utf8')
        if is_notebook():
            html('<b>' + sname + ': </b><br/>' + exrow['problem_text'].encode('utf8') + '<br/>')
        else:
            print sname + '\n' + exrow['problem_text'].encode('utf8') + '\n'



    def print_instance(self, ex_instance):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """

        summtxt =  ex_instance.summary()
        probtxt =  ex_instance.problem()
        answtxt =  ex_instance.answer()
        sname   =  ex_instance.name

        #Use jinja2 template to generate LaTeX.
        html_string = self.template("print_instance_html.html",sname=sname,summtxt=summtxt,probtxt=probtxt,answtxt=answtxt,ekey=ex_instance.ekey)


        if is_notebook():
            # ---------------
            # Using notebook.
            # ---------------

            #show in notebook
            html(html_string.encode('utf-8'))

            #file with html to export.
            f = open(sname+'.html.txt','w')
            f.write(html_string.encode('latin1'))
            f.close()

        else:
            # -------------------
            # Using command line.
            # -------------------
            print html_string




#end class MegBookWeb

