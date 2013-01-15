r"""
xsws.py

Export exercises from database to a zipped folder with sws files.
One for each exercise.

AUTHORS:

- Pedro Cruz (2012-06): initial version

LINKS::

   http://www.sagemath.org/doc/reference/sagenb/notebook/notebook.html
   http://www.sagemath.org/doc/reference/sagenb/notebook/worksheet.html
   http://www.sagemath.org/doc/reference/sagenb/notebook/cell.html#sagenb.notebook.cell.Cell 

"""


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

#python package
import os
import jinja2
import codecs
import subprocess
import re

#megua package
from localstore import ExIter
from csection import SectionClassifier, Section
from ex import *

TO_REST = 1
TO_HTML = 2

class SWSExporter:
    """
    Produce sws files from a database of exercises. SWS filename will be numbers of chapters as indicated on the tag  %summary.

    """

    #TODO: maybe not needed.
    #char_level = { 0: '#', 1: '*', 2: '=', 3:'-', 4:'^' }


    def __init__(self,megbook,where=None,tagstr='',optvalues=0, debug=False):
      
        #save megstore reference
        self.megbook = megbook
        self.megbook_store = self.megbook.megbook_store

        self.optvalues = optvalues
        self.tagstr = tagstr

        # --------------------    
        # Create SWS folder 
        # --------------------
        if where is None:
            self.sws_folder = self.megbook_store.local_store_filename + '_sws'
        else:
            self.sws_folder = os.path.join(where,'sws')

        if debug:
            print "Index folder: " + self.sws_folder

        #If does not exist create
        if not os.path.exists(self.sws_folder):
            os.makedirs(self.sws_folder)

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.sws_template = self.megbook.env.get_template("xsws_template.html")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing templates 'xsws_template.txt'."
            raise e


        #Create tree structure
        self.sc = SectionClassifier(self.megbook_store)
        
        #Save to a sws file.
        self._save_to_sws()


        #ZIP the folder
        #http://stackoverflow.com/questions/699325/suppress-output-in-python-calls-to-executables
        #fnull = open(os.devnull,'w')
        #note: use of tagstr for a filename. TODO: check this str if is a filename.
        #TODO: this is causing error
        #subprocess.check_call([ "zip", self.tagstr, os.path.join(self.sws_folder,'*.sws')],stdout=fnull,stderr=fnull) 
        #fnull.close()
        osstr = "zip %s %s" %  (self.tagstr, os.path.join(self.sws_folder,'*.sws') )
        os.system(osstr)


    def _save_to_sws(self):

        #Create notebook
        nb = sagenb.notebook.notebook.Notebook(self.sws_folder+'.sagenb')

        #Create a worksheet for each section
        for sec_number,sec_name in enumerate(self.sc.contents):

            #Create worksheet for sec_name
            W = nb.create_new_worksheet(sec_name, 'admin')

            #Get Section with sec_name (see class Section from csection.py)
            section = self.sc.contents[sec_name]

            #Write all section contents to a file.
            self.ofile = codecs.open( os.path.join( self.sws_folder, "sec%02d.html" % (sec_number+1) ),encoding='utf-8', mode='w+')
            self.sec_print(section, sec_name)
            self.ofile.close()

            #Read all section contents to a string.
            self.ofile = codecs.open( os.path.join( self.sws_folder, "sec%02d.html" % (sec_number+1) ),encoding='utf-8', mode='r')
            section_text = self.ofile.read()
            self.ofile.close()
            
            #Write to the worksheet
            W.edit_save(section_text)
            nb.save()
            
            nb.export_worksheet('admin/%d' % sec_number, os.path.join(self.sws_folder,'%02d.sws' % sec_number), title=self.tagstr + " " + sec_name)

        #print nb.worksheet_names()
        #Essencial to delete. Otherwise it will add new worksheets to this temporary notebook.
        nb.delete()
        




    def sec_print(self, section, secnames):

        if section.level==0:
            self.ofile.write('<h1>%s</h1>\n' % section.sec_name)
        elif section.level==1:
            self.ofile.write('<h2>%s</h2>\n' % section.sec_name)
        elif section.level==2:
            self.ofile.write('<h3>%s</h3>\n' % section.sec_name)
        else:
            self.ofile.write('<b>%s</b>\n' % section.sec_name)

        for e in section.exercises:

            row = self.megbook_store.get_classrow(e) #e is exer name (same as owner_keystring)
            etxt = self.sws_template.render(
                    ownerkey = e,
                    secnames = secnames,
                    summary=row['summary_text'],
                    problem=self.convert(row['problem_text']),
                    answer=self.convert(row['answer_text']),
                    sage_python=row['class_text']
            )
            self.ofile.write(etxt)

        for subsection in section.subsections.itervalues():
            self.sec_print(subsection, secnames + ";" + subsection.sec_name )


    def convert(self,input_str):
        if TO_REST & self.optvalues:
            return convert_to_rest(input_str)
        elif TO_HTML & self.optvalues:
            return convert_to_html(input_str)
        else:
            return input_str


# TODO: see pandoc: http://johnmacfarlane.net/pandoc/installing.html


def indent_repl(matchobj):
    #Debug
    #print "Grupo:"
    #print matchobj.group(1)
    #print "Fim do grupo"

    txt = "   " + matchobj.group(1).replace("\n","\n   ")
    return '\n\n.. math::\n\n%s\n\n' % txt


def convert_to_rest(input_str):
    """

    TODO:
    1. Keep tikz pictures without convertion.
    1. Keep tabular pictures without convertion.

    LINKS:

    1. About MathJax and Latex: http://www.mathjax.org/docs/2.0/tex.html

    NOTES:

    1. Using 
        #Convertion of $$ form $$ into ..math: notation
        #txt = re.sub(r'\b\$\$(.+)\$\$\b', indent_repl, input_str, re.M|re.DOTALL)
        #txt = re.sub(r'\$(.+)\$',r':math:`\1`', txt, re.M|re.DOTALL) 
    does not work because it matches $$ and end of line and not the next one.

    2. This routine is using version "pandoc 1.5.1.1". Should be adapted for other version.
    """

    #TODO: filter /; because "pandoc 1.5" application does not like them.

    f = codecs.open('temp.tex',encoding='utf-8', mode='w+')
    #f =open('temp.tex','w')
    f.write(input_str)
    f.close()
    try:
        #TODO: review error code of this.
        os.system("pandoc -f latex -t rst temp.tex -o temp.rst")
    except:
        return input_str
    f = codecs.open('temp.rst',encoding='utf-8', mode='r')
    #f =open('temp.rst','r')
    output_str = f.read()
    f.close()

    #os.system("rm temp.tex temp.rst")

    #Convertion of :math:`$$ ... $$` into ..math: notation
    #TODO: if line contains $$...$$ and $$...$$ then a probem: inside $$ are going to be ignored.
    txt = re.sub(ur':math:`\$\$(.+)\$\$`', indent_repl, output_str, re.DOTALL|re.U)

    #Replace `$ and $` only by `  and ` 
    txt = re.sub(ur'`\$', r'`', txt, re.DOTALL|re.U)
    txt = re.sub(ur'\$`', r'`', txt, re.DOTALL|re.U)

    #TODO:
    #This does not work by the above reason.
    #txt = re.sub(r':math:`\$(.+)\$`', r':math:`\1`', txt, re.DOTALL)

    print type(txt)
    return txt



def convert_to_html(input_str):
    """

    See convert_to_rest notes.

    """

    #TODO: filter /; because "pandoc 1.5" application does not like them.

    #Save latex string to a temp file for pandoc to translate.
    f = codecs.open('temp.tex',encoding='utf-8', mode='w+')
    #f =open('temp.tex','w')
    f.write(input_str)
    f.close()

    #pandoc will translate it
    try:
        #TODO: review error code of this.
        os.system("pandoc -f latex -t html temp.tex -o temp.rst")
    except:
        return input_str
    f = codecs.open('temp.rst',encoding='utf-8', mode='r')
    #f =open('temp.rst','r')
    output_str = f.read()
    f.close()

    #os.system("rm temp.tex temp.rst")

    #Convertion of :math:`$$ ... $$` into ..math: notation
    #TODO: if line contains $$...$$ and $$...$$ then a probem: inside $$ are going to be ignored.
    txt = re.sub(ur':math:`\$\$(.+)\$\$`', indent_repl, output_str, re.DOTALL|re.U)

    #Replace `$ and $` only by `  and ` 
    txt = re.sub(ur'`\$', r'`', txt, re.DOTALL|re.U)
    txt = re.sub(ur'\$`', r'`', txt, re.DOTALL|re.U)

    #TODO:
    #This does not work by the above reason.
    #txt = re.sub(r':math:`\$(.+)\$`', r':math:`\1`', txt, re.DOTALL)

    print type(txt)
    return txt



def str_indent(s):
    return "   " + s.replace("\n","\n   ")


#END of File

