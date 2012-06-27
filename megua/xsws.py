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

#megua package
from localstore import ExIter
from csection import SectionClassifier, Section
from ex import *


class SWSExporter:
    """
    Produce sws files from a database of exercises. SWS filename will be numbers of chapters as indicated on the tag  %summary.

    """

    #TODO: maybe not needed.
    #char_level = { 0: '#', 1: '*', 2: '=', 3:'-', 4:'^' }


    def __init__(self,megbook,where=None,tagstr='',debug=False):
      
        #save megstore reference
        self.megbook = megbook
        self.megbook_store = self.megbook.megbook_store


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
        fnull = open(os.devnull,'w')
        #note: use of tagstr for a filename. TODO: check this str if is a filename.
        subprocess.check_call([ "zip", self.tagstr, os.path.join(self.sws_folder,'*.sws')],stdout=fnull,stderr=fnull) 
        fnull.close()


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
                    problem=row['problem_text'],
                    answer=row['answer_text'],
                    sage_python=row['class_text']
            )
            self.ofile.write(etxt)

        for subsection in section.subsections.itervalues():
            self.sec_print(subsection, secnames + ";" + subsection.sec_name )


