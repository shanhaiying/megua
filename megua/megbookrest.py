r"""
MegBookRest -- Build your own database of exercises using Rest, Tikz and MathJax.

AUTHORS:

- Pedro Cruz (2012-07): initial version.


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
from megbookbase import *
from platex import pcompile



#TODO Is it necessary to import other libs?



class MegBookRest(MegBookBase):
    r"""
    Build your own database of exercises using Rest, Tikz and MathJax.

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
        MegBookBase.__init__(self,filename=filename,natlang=natlang,markuplang='rest')



    def __str__(self):
        return "MegBookRest('%s') for %s and markup language %s" % (self.local_store_filename,self.megbook_store.natural_language,self.megbook_store.markup_language)


    def __repr__(self):
        return "MegBookRest('%s')" % (self.local_store_filename)


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
        # Testing REST compilation. TODO: how to do this?
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
        html_string = self.template("print_instance_rest.html",sname=sname,summtxt=summtxt,probtxt=probtxt,answtxt=answtxt,ekey=ex_instance.ekey)

        #Produce files for pdf and png graphics if any tikz code embed on exercise
        html_string = self.publish_tikz(sname,ex_instance.ekey,html_string)
        #Produce files for pdf and png tables if any embeded on exercise
        html_string = self.publish_tabular(sname,ex_instance.ekey,html_string)


        #if is_notebook():
        # ---------------
        # Using notebook.
        # ---------------

        #To be viewed on browser
        f = open(sname+'.html','w')
        f.write(html_string.encode('latin1'))
        f.close()

        #To be used on sphinx
        f = codecs.open("%s-%03d.rst" % (sname,ex_instance.ekey), mode='w', encoding='utf-8')
        f.write(html_string)
        f.close()

        #else:
        #    # -------------------
        #    # Using command line.
        #    # -------------------
        #    #TODO: check this.
        #    print html_string



    def publish_tikz(self,sname,ekey,html_str):
        """ 
        Receives a string with latex tikz begin{}...end{} environments. Extracts and produce pdf and png file for each tikz graphic.
        TODO: impove this algorithm
        """

        #important \\ and \{
        tikz_pattern = re.compile(r'\\begin\{tikzpicture\}(.+)\\end\{tikzpicture\}', re.DOTALL|re.UNICODE)

        #Cycle through existent tikz code and produce pdf and png files.
        graphic_number = 0
        match_iter = re.finditer(tikz_pattern,html_str)#create an iterator
        for match in match_iter:
            #Graphic filename
            gfilename = '%s-%03d-g%02d'%(sname,ekey,graphic_number)
            #Compile tikz picture
            tikz_picture = match.group() 
            tikz_tex = self.template("tikz_graphics.tex", pgfrealjobname=r"\pgfrealjobname{%s}"%sname, beginname=r"\beginpgfgraphicnamed{%s}"%gfilename, tikz_picture=tikz_picture)
            pcompile(tikz_tex,'.',gfilename,hideoutput=True)
            #convert -density 600x600 pic.pdf -quality 90 -resize 800x600 pic.png
            #TODO: improve options: size, subprocess
            os.system("convert -density 300x300 '%s.pdf' -quality 90 -resize 400x300 '%s.png'"  % (gfilename,gfilename))
            graphic_number += 1

        #Cycle through existent tikz code and produce a new html string .
        graphic_number = 0
        gfilename = '%s-%03d-g%02d'%(sname,ekey,graphic_number)
        (new_html,number) = tikz_pattern.subn(r"\n\n.. image:: %s.png\n\n" % gfilename, html_str, count=1)
        while number>0:
            graphic_number += 1
            gfilename = '%s-%03d-g%02d'%(sname,ekey,graphic_number)
            (new_html,number) = tikz_pattern.subn(r"\n\n.. image:: %s.png\n\n" % gfilename, new_html, count=1)
        
        return new_html


    def publish_tabular(self,sname,ekey,html_str):
        """ 
        Receives a string with latex begin{tabular}...end{tabular} environments. Extracts and produce pdf and png file for each tabular graphic.
        TODO: impove this algorithm
        """

        #important \\ and \{
        tab_pattern = re.compile(r'\\begin\{tabular\}.+?\\end\{tabular\}', re.DOTALL|re.UNICODE)

        #Cycle through existent tikz code and produce pdf and png files.
        graphic_number = 0
        match_iter = re.finditer(tab_pattern,html_str)#create an iterator
        for match in match_iter:
            #Graphic filename
            gfilename = '%s-%03d-t%02d'%(sname,ekey,graphic_number)
            #Compile tikz picture
            tab_picture = match.group() 
            tab_tex = self.template("tabular_graphics.tex", tabular_tex=tab_picture)
            pcompile(tab_tex,'.',gfilename,hideoutput=True)
            #convert -density 600x600 pic.pdf -quality 90 -resize 800x600 pic.png
            #TODO: improve options: size, subprocess
            os.system("convert -density 300x300 '%s.pdf' -quality 90 -resize 400x300 '%s.png'"  % (gfilename,gfilename))
            graphic_number += 1

        #Cycle through existent tabular code and produce a new html string .
        graphic_number = 0
        gfilename = '%s-%03d-t%02d'%(sname,ekey,graphic_number)
        (new_html,number) = tab_pattern.subn(r"\n\n.. image:: %s.png\n\n" % gfilename, html_str, count=1)
        while number>0:
            graphic_number += 1
            gfilename = '%s-%03d-t%02d'%(sname,ekey,graphic_number)
            (new_html,number) = tab_pattern.subn(r"\n\n.. image:: %s.png\n\n" % gfilename, new_html, count=1)
        
        return new_html


#end class MegBookRest

