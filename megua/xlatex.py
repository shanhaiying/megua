r"""
xlatex.py -- export to pdflatex.

AUTHORS:

- Pedro Cruz (2014-10): initial version

TODO:
- break long lines to fit 80 chars in verbatim environment
- trim to much blank lines (only one for each)

NOTES:
- first version based on xsphinx.py module of megua

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  


#python package
import os
import shutil
import codecs
import jinja2
from string import join
import re

#megua package
from localstore import ExIter
from csection import SectionClassifier, Section

class PDFLaTeXExporter:
    """
    Produce LaTeX code files from the database and an index reading first line of the %summary field.

    """

    def __init__(self,megbook,where=".",exerset=None,debug=False):
        r"""

        INPUT:
        - ``megbook`` - 
        - ``where`      
        - ``exerset``
        
      
        #save megstore reference
        self.megbook = megbook
        self.megbook_store = self.megbook.megbook_store


        """

        self.megbook = megbook
        self.megbook_store = self.megbook.megbook_store
        self.xlatex_folder = where

        #Filter exerset to remove integers
        self.exerset = [c[0] for c in exerset]

        #for c in exerset:
        #    print type(c)
        #    if type(c)==str:
        #        self.exerset.append( c )

        print "List of exercises:",self.exerset

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.exercise_template = self.megbook.env.get_template("xlatex_exercise.tex")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template xlatex_exercise.tex"
            raise e


        #Open file 
        #self.ofile = open( os.path.join(where,'megua_ex.tex'), 'w') 
        self.ofile = open( 'megua_ex.tex', 'w') 
        #self.ofile = codecs.open( os.path.join( self.xlatex_folder, "megua_ex.tex" ), encoding='utf-8', mode='w+')
        #self.ofile = codecs.open( "megua_ex.tex", encoding='utf-8', mode='w+') 
        #now see thesis_latexfile.texself.ofile.write(self.main_template.render().encode('latin1'))

        #Open pdflatex template

        #Create tree structure
        self.sc = SectionClassifier(self.megbook_store,exerset=self.exerset)
        
        #Save to files and build html.
        self._save_to_file()

        self.ofile.close()


    def _save_to_file(self):

        #Create index.rst from xsphinx_index.rst template.
        for sec_number,sec_name in enumerate(self.sc.contents):

            #Get Section with sec_name (see class Section from csection.py)
            section = self.sc.contents[sec_name]

            #Write 
            self.sec_print(section)

  

    def sec_print(self, section):

        if section.level==0: # \section
            self.ofile.write(r'\section{%s}' % section.sec_name.encode("latin1") + "\n\n")
        elif section.level==1: # \subsection
            self.ofile.write(r'\subsection{%s}' % section.sec_name.encode("latin1") + "\n\n")
        elif section.level==2: # \subsubsection
            self.ofile.write(r'\subsubsection{%s}' % section.sec_name.encode("latin1") + "\n\n")
        elif section.level==3: # \subsubsubsection
            self.ofile.write(r'\subsubsubsection{%s}' % section.sec_name.encode("latin1") + "\n\n")
        else: # it will just bold
            self.ofile.write(r'\textbf{%s}' % section.sec_name.encode("latin1") + "\n\n")


        for e in section.exercises:

            row = self.megbook_store.get_classrow(e) #e is exer name (same as owner_keystring)
            etxt = self.exercise_template.render(
                    problem_name=row['owner_key'],
                    slashedproblem_name=latexunderscore(row['owner_key']),
                    summary=str_indent(row['summary_text']),
                    problem=str_indent(row['problem_text']),
                    answer=str_indent(row['answer_text']),
                    sage_python=str_indent( row['class_text'] ),
                    sections_text = row["sections_text"],
                    suggestive_name= row["suggestive_name"]
            )

            self.ofile.write(etxt.encode("latin1"))
            self.ofile.write("\n\n")

        for subsection in section.subsections.itervalues():
            self.sec_print(subsection)



def latexunderscore(txt):
    """Put \_  in each underscore"""
    return re.subn("_","\_",txt)[0]

def str_indent(s):
    return "   " + s.replace("\n","\n   ")

def lang_set(s):
    if s == 'pt_pt':
        return 'pt_br'
    else:
        return s

