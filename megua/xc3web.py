r"""
xc3web.py

Export exercises to work with c3web folder organization. See link below.
Exercises must be atached to the section and subsections should not exist.

AUTHORS:

- Pedro Cruz (2012-06): initial version

LINKS::

   http://c3web.web.ua.pt/

"""


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  
#TODO: check what libraries must be in use.

#python package
import os
import jinja2

#megua package
from localstore import ExIter
from csection import SectionClassifier, Section
from ex import *

class C3WebExporter:
    """
    Produce html files from a database of exercies based on the chapter indicated on the tag  %summary.
    """

    #TODO: maybe not needed.
    #char_level = { 0: '#', 1: '*', 2: '=', 3:'-', 4:'^' }


    def __init__(self,megbook,where=None,debug=False):
      
        #save megstore reference
        self.megbook = megbook
        self.megbook_store = self.megbook.megbook_store


        # --------------------    
        # Create c3web folder 
        # --------------------
        if where is None:
            self.c3web_folder = self.megbook_store.local_store_filename + '_c3web'
        else:
            self.c3web_folder = os.path.join(where,'c3web')

        if debug:
            print "Index folder: " + self.c3web_folder

        #If does not exist create
        if not os.path.exists(self.c3web_folder):
            os.makedirs(self.c3web_folder)

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.problem_template = self.megbook.env.get_template("xc3web_problem.html")
            self.problemanswer_template = self.megbook.env.get_template("xc3web_problemanswer.html")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing templates 'xc3web_problem.html' or 'xc3web_problemanswer.html'."
            raise e


        #Create tree structure
        self.sc = SectionClassifier(self.megbook_store)
        
        #Save to files and build html.
        self._save_to_files()

        #ZIP the folder
        #http://stackoverflow.com/questions/699325/suppress-output-in-python-calls-to-executables
        #fnull = open(os.devnull,'w')
        import subprocess
        #subprocess.check_call([ "zip", self.c3web_folder, self.c3web_folder],stdout=fnull,stderr=fnull) 
        subprocess.call("zip %s %s" % (self.c3web_folder, self.c3web_folder+r'/*'), shell=True) 
        #fnull.close()


        #Output links to chapters in current cell
        #TODO or do it in megbookweb


    def _save_to_files(self):
        """
        Print exercises of a section.
        Exercises must be atached to the section and subsections should not exist.
        """
        
        for sec_number,sec_name in enumerate(self.sc.contents):

            print sec_number,sec_name

            #Get Section with sec_name (see class Section from csection.py)
            section = self.sc.contents[sec_name]

            #Create each exx-yyy-Rzz.html where R is P or A
            self._print_section(section,sec_number)


    def _print_section(self, section, sec_number):
        """
        Print exercises of a section.
        Exercises must be atached to the section and subsections should not exist.

        NOTES: 
          Use
            self.ofile = codecs.open( os.path.join( self.c3web_folder, "e%02d.rst" % (sec_number+1) ),encoding='utf-8', mode='w+')
          if utf8 is needed.
        """
	if sec_number==0:
            fn="2"
        else:
            fn="3"

        for e_number,exer in enumerate(section.exercises):   

            for ekey in range(10):

		#Continuous numeration of exercises
		exnr = e_number*10 + (ekey+1)

                #Create exercise instance
                row = self.megbook_store.get_classrow(exer) #e is exer name (same as owner_keystring)
                ex_instance = exerciseinstance(row, ekey=ekey)


                #Print problem
                #Template fields:
                # {{ extitle }} Ex. Q.1
                # {{ exsmall }} Ex. L.1
 
                problem_html = self.problem_template.render(
                    extitle = "Ex. L.%d" % exnr,
                    exsmall = "Res. Ex. L.%d" % exnr,
                    problem = ex_instance.problem()
                )
                #ofile = open( os.path.join( self.c3web_folder, "e%02d-%02d-P%02d.aspx" % (sec_number+1,e_number+1,ekey+1) ), 'w')
                ofile = open( os.path.join( self.c3web_folder, "e%s%2d.aspx" % (fn,exnr) ), 'w')
                ofile.write(problem_html.encode('latin1'))
                ofile.close()

                #Print problem and answer
                problemanswer_html = self.problemanswer_template.render(
                    extitle = "Ex. Q.%d" % exnr,
                    exsmall = "Res. L.%d" % exnr,
                    problem = ex_instance.problem(),
                    answer = ex_instance.answer()
                )
                #ofile = open( os.path.join( self.c3web_folder, "e%02d-%02d-A%02d.aspx" % (sec_number+1,e_number+1,ekey+1) ), 'w')
                ofile = open( os.path.join( self.c3web_folder, "r%s%2d.aspx" % (fn,exnr) ), 'w')
                ofile.write(problemanswer_html.encode('latin1'))
                ofile.close()


def lang_set(s):
    if s == 'pt_pt':
        return 'pt_br'
    else:
        return s

