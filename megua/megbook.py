r"""
MegBook -- Build your own database of exercises.

AUTHORS:

- Pedro Cruz (2011-06): initial version (use of pdflatex)
- Pedro Cruz (2011-10): another version
- Pedro Cruz (2011-11): another version
- Pedro Cruz (2012-01): including jinja2 templating.

- Pedro Cruz (2012-06): starting project for use of web and pdflatex.

- Pedro Cruz (2013-03-01): megbook will contains all exercise types.

"""


#*****************************************************************************
#       Copyright (C) 2011,2012,2013 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

#MEGUA modules:
from localstore import LocalStore,ExIter
from ex import *
from exerparse import exerc_parse
from xsphinx import SphinxExporter
from platex import pcompile
from xsws import SWSExporter


#Because sage.plot.plot.EMBEDDED_MODE
#This variable indicates if notebook is present.
#Trying no include now the EMBEDDED_MODE and wait for some place else:
from sage.all import *


#Sage modules:
#Check if sage.all includes this:
from sage.misc.latex import JSMath, Latex, _run_latex_, _latex_file_
from sage.misc.html import html

#Python modules:
import sqlite3 #for row objects as result from localstore.py
import shutil
import os
import StringIO
import sys
#import codecs


# Jinja2 package
import jinja2
#from jinja2 import Environment, PackageLoader,FileSystemLoader,Template, TemplateNotFound
#Note on Jinja2:
# di = { 'ex_10_0_4': 10 }
# template.stream(di).dump('new.tex')
# print "Template folders are: " + str(env.loader.searchpath)


class MegBook:
    r"""
    MEGUA set of routines for exercise templating.

    INPUT::

    - ``filename`` -- filename where the database is stored.

    This module provides a means to produce a database of exercises that can be seen as a book of some author or authors.

    Using exercices:

    - create, edit and delete exercises from a database.
    - search for an exercise or set of exercises.
    - create a random instance from a set or single exercise
    - create an instance based on specific parameters
    - create latex (and PDF) from a single or a set of exercises.


    Examples of use:

    .. test with: sage -python -m doctest megbook.py

    Create or edit a database::

       >>> from all import *
       >>> meg = MegBook(r'.testoutput/megdb.sqlite',outputdir=r'.testoutput')
       MegBook opened. Execute `MegBook?` for examples of usage.
       Templates for 'pt_pt' language.


    Save a new or changed exercise::

       >>> meg.save(r'''
       ... %Summary Primitives
       ... Here one can write few words, keywords about the exercise.
       ... For example, the subject, MSC code, and so on.
       ...   
       ... %Problem A sum problem
       ... What is the primitive of $a x + b@()$ ?
       ... 
       ... %Answer
       ... The answer is $prim+C$, for $C in \mathbb{R}$.
       ... 
       ... class E28E28_pdirect_001(Exercise):
       ... 
       ...     def make_random(self):
       ...         self.a = ZZ.random_element(-4,4)
       ...         self.b = self.a + QQ.random_element(1,4)
       ... 
       ...     def solve(self):
       ...         x=var('x')
       ...         self.prim = integrate(self.a * x + self.b,x)
       ... ''')
       Each problem can have a suggestive name. 
       Write in the '%problem' line a name, for ex., '%problem The Fish Problem'.
       <BLANKLINE>
       Testing python/sage class 'E28E28_pdirect_001' with 100 different keys.
           No problems found in this test.
          Compiling 'E28E28_pdirect_001' with pdflatex.
          No errors found during pdflatex compilation. Check E28E28_pdirect_001.log for details.
       Exercise name E28E28_pdirect_001 inserted or changed.

    Search an exercise:

      >>> meg.search("primitive")
      Exercise name E28E28_pdirect_001
      <BLANKLINE>
      %problem 
      What is the primitive of $a x + b@()$ ?
      <BLANKLINE>
      <BLANKLINE>
      <BLANKLINE>

    Remove an exercise:

       >>> meg.remove('E28E28_pdirect_001',dest=r'.testoutput')
       Exercise 'E28E28_pdirect_001' stored on text file .testoutput/E28E28_pdirect_001.txt.
       >>> meg.remove('E28E28_nonexistant',dest=r'.testoutput')
       Exercise E28E28_nonexistant is not on the database.
    """

    #TODO 1: increase docstring examples.

    #TODO 2: assure that there is a natlang folder in templates (otherwise put it in english). Warn for existing languages if specifies lan does not exist.

    #TODO 3: remove html_output and latex_debug=False; create debug only.


    def __init__(self,filename,natlang='en_en',outputdir='.'):
        r"""

        INPUT::
        - ``filename`` -- filename where the database is stored.
        - ``default_natlang`` -- For example 'pt_pt' for portuguese (of portugal), 'en_us' for english from USA.

        """
        #Variable DATA is only defined after worksheet is opened so it cannot be imported to here.

        if not filename:
            raise IOError("MegBook needs database filename to be specified.")

        self.local_store_filename  = filename

        #Create or open the database
        try:
            self.megbook_store = LocalStore(filename=self.local_store_filename,default_natlang=default_natlang)
            #TODO: fazer aparecer aqui um make_index
            #TODO: http://www.sagemath.org/doc/reference/sagenb/notebook/interact.html
            #http://interact.sagemath.org/
            print "MegBook opened. Execute `MegBook?` for examples of usage."
        except sqlite3.Error as e:
            print "MegBook couldn't be opened: ", e.args[0]
            return

        #Templating (with Jinja2)
        megenv.setlang(default_natlang)


        #For template. See template_create function.
        self.template_row = None



    def __str__(self):
        return "MegBook(%s)" % (self.local_store_filename)

    def __repr__(self):
        return "MegBook(%s)" % (self.local_store_filename)

    #TODO: inject exercise name as a class on to global workspace
    def save(self,exercisestr):
        r"""
        Save an exercise defined on a `python string`_ using a specific sintax defined here_.

        INPUT::

        - ``exercisestr`` -- a `python string`_ text containing a summary, problem, answer and class according to meg exercise sintax.
        - ``dest`` -- directory where latex compilation will be done.

        OUTPUT::

            Textual messages with errors.
            Check ``dest`` directory (default is current) for compilation results.

        .. _python string: http://docs.python.org/release/2.6.7/tutorial/introduction.html#strings
 
        """

        #print "TYPE OF INPUT ", str(type(exercisestr))

        if type(exercisestr)==str:
            exercisestr = unicode(exercisestr,'utf-8')

        #TODO: orgnizar os outputs em algo de HTML

        # ---------------------------------------
        # Check exercise syntax: 
        #    exer_parse return tuple:    
        #       summary, problem, answer and classtext.
        # ---------------------------------------
        if is_notebook():
            stdout_current = sys.stdout
            sys.stdout = open('parse_exercise.log', 'w')

        row = exerc_parse(exercisestr)
        if not row:
            print self.template('exercise_syntax.txt')
            print "==================================="
            print "Exercise was not saved on database."
            print "==================================="
            return
        if is_notebook():
            sys.stdout.close()
            sys.stdout = stdout_current

        # (0 owner_key, 1 txt_sections, 2 txt_summary, 3 txt_problem, 4 txt_answer, 5 txt_class)
        #row = {'owner_key': p[0], 'summary_text': p[2], 'problem_text': p[3], 'answer_text': p[4], 'class_text': p[5]}


        # -------------
        # Exercise ok?
        # -------------
        if not self.is_exercise_ok(row,self.outputdir,silent=False):
            print "==================================="
            print "Exercise was not saved on database."
            print "==================================="
            return


        # ----------------------------
        # Exercise seems ok: store it.
        # ----------------------------
        inserted_row = self.megbook_store.insertchange(row)
        if inserted_row: 
            print 'Exercise name %s inserted or changed.' % inserted_row['owner_key']
        else:
            print 'Problem in access to the database. Could not save the exercise on the database.'




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
        # Testing latex compilation.
        # --------------------------
        if not self.exercise_compiletest(row,dest,silent=silent):
            return False

        # Exercise Ok
        return True


    def exercise_pythontest(self,row,start=0,many=5, edict=None,silent=False):
        r"""
        Test an exercise with random keys.

        INPUT:

         - ``row`` -- dictionary with class textual definitions.
         - ``start`` -- the parameteres will be generated for this random seed for start.
         - ``many`` -- how many keys to generate. 
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.

        OUTPUT:

            Printed message and True/False value.

        TODO: change this function name to exercise_test.
        """


        #output = cStringIO.StringIO()
        #output.write('First line.\n')
        #print >>output, 'Second line.'


        success = True

        #Testing        
        try:
            #Do the test for other keys
            if not silent:
                print  "Testing python/sage class '%s' with %d different keys." % (row['owner_key'],many)

            #Create a class and a first instance for ekey=start.
            ekey = start #for exceptions
            print  "Testing for ekey =",start
            ex_instance = exerciseinstance(row,ekey=start,edict=edict)

            for ekey in range(start+1,start+many):
                print  "Testing for ekey =",ekey
                ex_instance.update(ekey=ekey,edict=edict))

            #return this
            ex_instance.update(ekey=start,edict=edict)

        except SyntaxError as se:
            print  "   Exercise class '%s' contains a syntax error on line %d." % (row['owner_key'],se.lineno)
            cl = row['class_text'].split()
            if len(cl)>se.lineno:
                print  "      check line: %s" % cl[se.lineno-1]
            success = False
        except Exception as ee: # Exception will be in memory.
            print  "Error on exercise '{0}' with parameters edict={1} and ekey={2}".format(row['owner_key'],edict,ekey)
            print  "   error description: ", ee
            if is_notebook():
                print  "   Copy exercise code, only the class part, to a new cell. Then add the following command"
                print  "%s().update(ekey=%d)" % (row['owner_key'],ekey)
                print  "and execute with shift+enter. This may help finding the error line."
            else:
                print  "   Test the exercise code, only the class part using the following command"
                print  "%s().update(ekey=%d)" % (row['owner_key'],ekey)
                print  "This may help finding the error line."
            success = False
        
        #Conclusion
        if not silent:
            if success:
                print  "    No problems found in this test."
            else:
                print  "Review exercise '%s' based on the reported cases." % row['owner_key']

        # Retrieve file contents -- this will be
        # 'First line.\nSecond line.\n'
        #contents = output.getvalue()

        # Close object and discard memory buffer --
        # .getvalue() will now raise an exception.
        #output.close()

        return success


    def exercise_compiletest(self,row,dest='.',silent=False):
        r"""
        pdflatex compilation test to check for error. 
        A new exercise is not entering the database if it has latex errors.
        """

        #create an instance
        ex_instance = exerciseinstance(row)

        #Use jinja2 template to generate LaTeX.
        latex_string = self.template("print_instance_latex.tex",
            sname=ex_instance.name,
            summtxt=ex_instance.summary(),
            probtxt=ex_instance.problem(),
            answtxt=ex_instance.answer(),
            ekey = ex_instance.ekey,
        )

        if not silent:
            print "   Compiling '%s' with pdflatex." % row['owner_key']
        return pcompile(latex_string,dest,row['owner_key'], hideoutput=True,silent=silent)


    def check_all(self,dest='.'):
        r""" 
        Check all exercises of this megbook for errrors.

        INPUT:

        OUTPUT:

            Printed message and True/False value.
        """

        all_ex = []
        for row in ExIter(self.megbook_store):
            if not self.is_exercise_ok(row,dest,silent=True):
                print "   Exercise '%s' have python/sage or latex errors." % row['owner_key']
                all_ex.append(row['owner_key'])
        if all_ex:
            print "Review the following exercises:"
            for r in all_ex:
                print r
        else:
            print "No problem found."

    def search(self,regex):
        r"""
        Performs a search of a regular expression ``regex`` over all fields.

        INPUT:
        - ``regex`` -- regular expression (see regex_ module).
        OUTPUT:
        - 
        
        .. _regex: http://docs.python.org/release/2.6.7/library/re.html
        """
        exlist = self.megbook_store.search(regex)
        for row in exlist:
            self.search_print_row(row)


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
            html('<b>' + sname + ': </b><pre>' + exrow['problem_text'].encode('utf8') + '</pre><br/>')
        else:
            print sname + '\n' + exrow['problem_text'].encode('utf8') + '\n'


    def remove(self,owner_keystring,dest='.'):
        r"""
        Removing an exercise from the database.

        INPUT:

        - ``owner_keystring`` -- the class name.
        """

        #Get the exercise
        row = self.megbook_store.get_classrow(owner_keystring)
        if row:            
            fname = os.path.join(dest,owner_keystring+'.txt')
            #store it on a text file
            f = open(fname,'w')
            f.write(row['summary_text'].encode('utf-8')) #includes %summary line
            f.write(row['problem_text'].encode('utf-8')) #includes %problem line
            f.write(row['answer_text'].encode('utf-8')) #includes %answer line
            f.write(row['class_text'].encode('utf-8'))
            f.close()
            print "Exercise '%s' stored on text file %s." % (owner_keystring,fname)

            #remove it
            self.megbook_store.remove_exercise(owner_keystring)
        else:
            print "Exercise %s is not on the database." % owner_keystring



    def new(self,owner_keystring, ekey=None, edict=None):
        r"""Prints an exercise instance of a given type

        INPUT:

         - ``owner_keystring`` -- the class name.
         - ``ekey`` -- the parameteres will be generated for this random seed.
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.

        OUTPUT:
            An instance of class named ``owner_keystring``.

        """
        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(owner_keystring)
        if not row:
            print "%s cannot be accessed on database" % owner_keystring
            return None
        #Create and print the instance
        ex_instance = exerciseinstance(row, ekey, edict)
        ex_instance.print()
        #old: self.print_instance(ex_instance)
        return ex_instance



    def print_instance(self, ex_instance):
        """
        Routine used to produce an exercise output to notebook or command line mode.
        """

        summtxt =  ex_instance.summary()
        probtxt =  ex_instance.problem()
        answtxt =  ex_instance.answer()
        sname   =  ex_instance.name

        #Use jinja2 template to generate LaTeX.
        latex_string = self.template("print_instance_latex.tex",sname=sname,summtxt=summtxt,probtxt=probtxt,answtxt=answtxt,ekey=ex_instance.ekey)

        if is_notebook():

            # ---------------
            # Using notebook.
            # ---------------

            #Produce PDF file from LaTeX.
            pcompile(latex_string,'.',sname, hideoutput=True)

        else:

            # -------------------
            # Using command line.
            # -------------------
            
            #Textual output
            if self.html_output:
                print '-'*len(sname)
                print sname 
                print '-'*len(sname)
                print summtxt.encode('utf8')
                print probtxt.encode('utf8')
                print answtxt.encode('utf8')

            #Produce PDF file from LaTeX.
            pcompile(latex_string, '.', sname, hideoutput=self.html_output)




    def put_here(self,owner_keystring, ekey=None, edict=None, elabel="NoLabel"):
        r"""
        Create an instance based on a template with key=owner_keystring.
        This routine is used on templates only.

        INPUT:

        - ``owner_keystring`` -- the exercise key.
        - ``ekey`` -- random seed.
        - ``edict`` -- dictionary to be used after random initialization of ex parameters.
        - ``elabel`` -- to be used for "\label" or "\ref" in LaTeX.

        OUTPUT:
            text string.

        NOTES: to be used with `template_create`.

        """

        #Get summary, problem and answer and class_text
        #Field row['class_text'] is needed to render the template. See below.
        row = self.megbook_store.get_classrow(owner_keystring)        
        if not row:
            #TODO: passar a raise Error
            print "%s cannot be accessed on database" % owner_keystring
            return "%s cannot be accessed on database" % owner_keystring

        #Get summary, problem and answer and class_text
        ex_instance = exerciseinstance(row,ekey,edict)

        #See template_create for template_row definition.
        utxt = self.template_row.render(
                exname=owner_keystring,
                summary = to_unicode( ex_instance.summary() ), 
                problemtemplate = to_unicode( ex_instance._problem_text ), 
                answertemplate  = to_unicode( ex_instance._answer_text ), 
                codetxt =  to_unicode( row['class_text'] ), 
                problem =  to_unicode( ex_instance.problem() ), 
                answer  =  to_unicode( ex_instance.answer() ),
                elabel  =  elabel,
                ekey = ekey
            )

        return utxt


    def template_fromstring(self,templatestring, ekey=None, rowtemplate=None,filename=None):
        #Get unicode and make a jinja2 template
        utxt = unicode(templatestring,'utf-8')
        template = jinja2.Template(utxt)

        #Create a new file for output
        if not filename:
            filename = os.path.join(SAGE_TMP,'modelo_out.tex')

        self.template_create(filename, template, ekey, rowtemplate)


    def template_fromfile(self,templefilename, ekey=None, rowtemplate=None):

        #Get template file and make a jinja2 template
        #NOTE: cannot use DATA variable.
        tfile = open(templefilename,'r')
        utxt = unicode(tfile.read(),'utf-8')
        tfile.close()
        template = jinja2.Template(utxt)

        #Create a new file for output on same folder of templefilename
        bname_ext = os.path.basename(templefilename)
        bname,ext_name = os.path.splitext(bname_ext)
        head,tail = os.path.split(templefilename)
        ofilename = os.path.join(head,bname+'_out.tex')

        self.template_create(ofilename, template, ekey, rowtemplate)


    def template_create(self,ofilename, template, ekey=None, rowtemplate=None):
        #Another possibility: {{ put_here("E65D05_forwarddifference_001",ekey=10,meg.SUMMARY|meg.PROBLEM|meg.ANSWER|meg.CODE) }}
        #http://jinja.pocoo.org/docs/templates/#assignments

        #Set seed
        if ekey:
            ur.set_seed(ekey)

        #Render output using the given template for each exercise.
        if rowtemplate is None:
            try:
                self.template_row = self.env.get_template("row_template.tex")
            except jinja2.exceptions.TemplateNotFound:
                return "MegUA -- missing template %s"%filename
        else:
            #Check or convert rowtemplate to unicode
            try:
                self.rowtemplate = unicode(rowtemplate,'utf-8')
            except TypeError:
                self.rowtemplate = rowtemplate
            self.template_row = jinja2.Template(rowtemplate)


        #Create a latex string s ready to compile.
        s = template.render(put_here=self.put_here)

        #Create new file and save string s.
        fp = open(ofilename,'w')
        fp.write( s.encode('utf-8') )
        res = fp.close()


        if is_notebook():

            # ---------
            # Notebook.
            # ---------
    
            #TODO: converter ao platex !

            #Create filename for 
            (base, filename) = os.path.split(ofilename)

            filename = os.path.splitext(filename)[0]  # get rid of extension
            if len(filename.split()) > 1:
                raise ValueError, "filename must contain no spaces"
            #redirect=' 2>/dev/null 1>/dev/null '

            #Compile
            if self.latex_debug:
                lt = 'cd "%s" && sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex}' % (base, 'pdflatex', filename)
            else:
                lt = 'cd "%s"&& sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex} 2>/dev/null 1>/dev/null' % (base, 'pdflatex', filename)

            #lt = 'cd "%s"&& sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex} '%(base, 'pdflatex', filename)
            os.system(lt)

            #Show in output cell
            bname,ext_name = os.path.splitext(filename)
            shutil.move(ofilename,'.') #move tex file
            shutil.move(os.path.join(base,bname+'.pdf'),'.')

        else:

            # -------------
            # Command line.
            # -------------

            print "Compile using:   pdflatex %s" % ofilename
            os.system("pdflatex %s" % ofilename)
            shutil.copy(ofilename,'.')



    def template_class_question(self,students, questions, ofilename, file_header, student_template, includeanswer=False,ekey_start=0):
        r"""
        Create several exercises for each student.

        INPUT::
    
        - ``students`` -- number of students OR list of students in form `[ ['name1', 'number'], ['name2', 'number'] ]`.
        - ``questions`` -- list of exercises names (questions).
        - ``ofilename`` -- latex output file.
        - ``file_header`` -- global latex file header.
        - ``student_template`` -- each student latex header.
        - ``ekey_start`` -- number to add to each student number (will be the exercise key).


        IMPLEMENTATIONS NOTES:

        2. See template_create() for details about use of unicode and latin1.

        """

        #TODO: improve this function to use jinja2 templates.
        #TODO: converter ao platex, etc

        #Create new file from jinja2 template  
        fp = open(ofilename,'w')

        print "Output file: ", ofilename

        fp.write( file_header )
        fp.write( '\\begin{document}\n')


        #In case there is no list of students. Only number of them.
        if type(students)!=list:
            students = [ ['', str(nm+1)] for nm in range(students) ]

        #Write questions
        for (snum,s) in enumerate(students):

            #prepare student header with his name and number
            student_Template = jinja2.Template(student_template)
            try:
                sn = unicode(s[0],'latin1')
            except TypeError:
                sn = s[0]

            student_header = student_Template.render(sname=sn, snumber=s[1] )
            fp.write( student_header.encode('utf-8') )

            #prepare this student questions
            for (qnum, qpossible) in enumerate(questions):

                #print type(qpossible),qpossible

                if type(qpossible)==list:
                    #use snum to produce exercise choice from the list in qpossible.
                    #[i % 6 for i in range(35)]
                    l = len(qpossible)
                    qname = qpossible[snum % l]
                else:
                    qname = qpossible

                ex = self._classquestion_exercise(qname, ekey=ekey_start+snum)
                
                #aqui
                if includeanswer:
                    txt = u"\n\n\\noindent\\textbf{{ {qnumber} }}~{problem}\nResolu\c c\~ao:\n{answer}\n\\vspace{{1cm}}".format(\
                        qnumber=qnum+1, \
                        problem=ex.problem(), \
                        answer=ex.answer() \
                    )
                else:
                    txt = u"\n\n\\noindent\\textbf{{ {qnumber} }}~{problem}\n".format(qnumber=qnum+1,problem=ex.problem() )

                #fp.write(txt.encode('latin-1'))
                fp.write(txt.encode('utf-8'))

            #new page
            fp.write( '\\newpage' )



        #Write questions and answers
        fp.write( '\\end{document}\n')    
        fp.close()


        base, filename = os.path.split(ofilename)
        filename = os.path.splitext(filename)[0]  # get rid of extension
        if len(filename.split()) > 1:
            raise ValueError, "filename must contain no spaces"
        #redirect=' 2>/dev/null 1>/dev/null '
        lt =u'cd "%s"&& sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex} '%(base, 'pdflatex', filename)
        os.system(lt)
        bname,ext_name = os.path.splitext(filename)


    def _classquestion_exercise(self,owner_keystring, ekey=None):
        r"""
        Create an instance based on a template with key=owner_keystring

        """
        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(owner_keystring)
        if not row:
            return "'%s' cannot be accessed on database '%s'" % (owner_keystring,self.local_store_filename)

        return exerciseinstance(row,ekey=ekey)



    def make_index(self,where='.',debug=False):
        """
        Produce rst code files from the database and an index reading first line of the %summary field.

        Command line use: 
            The ``where`` input argument, when specified,  will contain all details of Sphinx compilation.

        LINKS:

        http://code.activestate.com/recipes/193890-using-rest-restructuredtext-to-create-html-snippet/

        """

        html_index = SphinxExporter(self,where,debug)
        print "Index is at: "+ html_index.htmlfile

        if is_notebook():
            if where == '.': 
                #To open a browser
                pos = html_index.htmlfile.find(".")
                html(r'<a href="%s" target=_blank>Press to open database index.</a>' % html_index.htmlfile[pos:])
            elif 'data' in where:
                #To open a browser
                pos = html_index.htmlfile.find("/home")
                pos2 = html_index.htmlfile.find("/home",pos+1)
                if pos2>=0:
                    pos = pos2
                html(r'<a href="%s" target=_blank>Press to open database index.</a>' % html_index.htmlfile[pos:])
            else:
                #print "Index is at: "+ html_index.htmlfile
                print "See index at Megua button at top."
        else:
            print "firefox -no-remote ", html_index.htmlfile



    def make_sws(self, dest='.',tagstr='',optvalues=0):
        sws = SWSExporter(self,dest,tagstr=tagstr,optvalues=optvalues)


#end class MegBook




def is_notebook():
    return sage.plot.plot.EMBEDDED_MODE


    r''' Remove this definition:

    def dbinstance(self, ex_class, ekey=None, edict=None):
        #Get summary, problem, answer and class_text
        row = self.megbook_store.get_classrow(ex_class.name)
        #Create instance
        return self.instance(ex_class.name,ex_class, row, ekey, edict)
    '''


