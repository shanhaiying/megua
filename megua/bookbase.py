r"""
BookBase -- Base class for build your own database of exercises on some markup language. 

BookBase is ready for textual form exercises. See derivatives of this class for
other markup languages.


AUTHORS:

- Pedro Cruz (2012-06): initial version (based on megbook.py)

"""

# Abstract function
# raise NotImplementedError( "Should have implemented this" )


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

#Megua modules:
from localstore import LocalStore,ExIter
from ex import *
from exerparse import exerc_parse
from xsphinx import SphinxExporter


#Because sage.plot.plot.EMBEDDED_MODE
#This variable indicates if notebook is present.
#Trying no include now the EMBEDDED_MODE and wait for some place else:
from sage.all import *

#Python modules:
import sqlite3 #for row objects as result from localstore.py
import shutil
import os
#import codecs


# Jinja2 package
import jinja2
#from jinja2 import Environment, PackageLoader,FileSystemLoader,Template, TemplateNotFound
#Note on Jinja2:
# di = { 'ex_10_0_4': 10 }
# template.stream(di).dump('new.tex')
# print "Template folders are: " + str(env.loader.searchpath)


class BookBase:
    r"""
    Base routines for exercise templating. Abstract class.

    INPUT::

    - ``filename`` -- filename where the database is stored.

    This module provides means to produce a database of exercises that can be seen as a book of some author or authors.

    Using exercices:

    - create, edit and delete exercises from a database.
    - search for an exercise or set of exercises.
    - create a random instance from a set or single exercise
    - create an instance based on specific parameters
    - create latex (and PDF) from a single or a set of exercises.


    Examples of use:

    .. test with: sage -python -m doctest bookbase.py

    Create or edit a database::

       >>> from all import *
       >>> meg = BookBase(r'.testoutput/megbasedb.sqlite')
       Opened BookBase(.testoutput/megbasedb.sqlite) for natural language pt_pt and markup language  text.
       Templates for 'pt_pt' language at template/pt_pt


    Save a new or changed exercise::

       >>> meg.save(r'''
       ... %Summary Primitives
       ... Here one can write few words, keywords about the exercise.
       ... For example, the subject, MSC code, and so on.
       ...   
       ... %Problem
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
       ... ''')
       Each problem can have a suggestive name. 
       Write in the '%problem' line a name, for ex., '%problem The Fish Problem'.
       <BLANKLINE>
       Exercise name E28E28_pdirect_001 inserted or changed.


    Search an exercise:

      >>> meg.search("primitive")
      Exercise name E28E28_pdirect_001
      <BLANKLINE>
      What is the primitive of ap x + bp@() ?
      <BLANKLINE>
      <BLANKLINE>
      <BLANKLINE>


    Remove an exercise:

       >>> meg.remove('E28E28_pdirect_001',dest=r'.testoutput')
       Exercise 'E28E28_pdirect_001' stored on text file .testoutput/E28E28_pdirect_001.txt.
       >>> meg.remove('E28E28_nonexistant',dest=r'.testoutput')
       Exercise E28E28_nonexistant is not on the database.
    """

    def __init__(self,filename=None,natlang='pt_pt',markuplang='text'): #TODO: utf-8 instead of asciitext?
        r"""

        INPUT::
        - ``filename`` -- filename where the database is stored.
        - ``natlang`` -- For example, 'pt_pt', for portuguese of Portugal.
        - ``markuplang`` -- 'latex' or 'web'. Derivative class could pass this argument.

        """
    
        #Sage and sagenotebook DATA variable is only defined after 
        #worksheet is opened so it cannot be imported to here.

        #Create or open the database
        try:
            self.book_store = LocalStore(filename=filename,natlang=natlang,markuplang=markuplang)
            self.local_store_filename = self.book_store.local_store_filename #keep record.
            print "Opened " + str(self)
        except sqlite3.Error as e:
            print "BookBase couldn't be opened: " , e.args[0]
            return

        #Templating (with Jinja2)
        if os.environ.has_key('MEGUA_TEMPLATE_PATH'):
            TEMPLATE_PATH = os.environ['MEGUA_TEMPLATE_PATH']
        else:
            from pkg_resources import resource_filename
            TEMPLATE_PATH = os.path.join(resource_filename(__name__,''),'template',natlang)
        print "Templates for '%s' language at %s" % (natlang,TEMPLATE_PATH)
        #print "Templates in: " + TEMPLATE_PATH
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH))

        #For template. See template_create function.
        self.template_row = None


    def __str__(self):
        return "BookBase(%s) for natural language %s and markup language  %s." % \
            (self.local_store_filename, \
             self.book_store.natural_language, \
             self.book_store.markup_language)

    def __repr__(self):
        return "BookBase(%s)" % (self.local_store_filename)

    def template(self, filename, **user_context):
        """
        Returns HTML, CSS, LaTeX, etc., for a template file rendered in the given
        context.

        INPUT:

        - ``filename`` - a string; the filename of the template relative
          to ``sagenb/data/templates``

        - ``user_context`` - a dictionary; the context in which to evaluate
          the file's template variables

        OUTPUT:

        - a string - the rendered HTML, CSS, etc.

        BASED ON:

           /home/.../sage/devel/sagenb/sagenb/notebook/tempate.py

        """

        try:
            tmpl = self.env.get_template(filename)
        except jinja2.exceptions.TemplateNotFound:
            return "MegUA -- missing template %s"%filename
        r = tmpl.render(**user_context)
        return r


    def save(self,exercisestr,dest='.'):
        r"""
        Save an exercise defined on a `python string`_ using a specific sintax defined here_.

        INPUT::

        - ``exercisestr`` -- a `python string`_ text containing a summary, problem, answer and class according to meg exercise sintax.
        - ``dest`` -- directory where possible compilation will be done.

        OUTPUT::

            Textual messages with errors.
            Check ``dest`` directory (default is current) for compilation results.

        .. _python string: http://docs.python.org/release/2.6.7/tutorial/introduction.html#strings

        """

        #print "TYPE OF INPUT ", str(type(exercisestr))

        if type(exercisestr)==str:
            exercisestr = unicode(exercisestr,'utf-8')


        # ---------------------------------------
        # Check exercise syntax: 
        #    summary, problem, answer and class.
        # ---------------------------------------
        row = exerc_parse(exercisestr)

        if not row:
            print self.template('exercise_syntax.txt')
            print "==================================="
            print "Exercise was not saved on database."
            print "==================================="
            return

        # (0 owner_key, 1 txt_sections, 2 txt_summary, 3 txt_problem, 4 txt_answer, 5 txt_class)
        #row = {'owner_key': p[0], 'summary_text': p[2], 'problem_text': p[3], 'answer_text': p[4], 'class_text': p[5]}


        # -------------
        # Exercise ok?
        # -------------
        if not self.is_exercise_ok(row,dest,silent=False):
            print "==================================="
            print "Exercise was not saved on database."
            print "==================================="
            return


        # ----------------------------
        # Exercise seems ok: store it.
        # ----------------------------
        inserted_row = self.book_store.insertchange(row)
        if inserted_row: 
            print 'Exercise name %s inserted or changed.' % inserted_row['owner_key']
        else:
            print 'Problem in access to the database. Could not save the exercise on the database.'


    def is_exercise_ok(self,row,dest,silent=True):
        r"""
        Check if exercise is ready for compilation and for python/sage errors.

        Developer note: derive this for other markups.
        """
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

        success = True

        #Testing        
        try:
            #Do the test for other keys
            if not silent:
                print "Testing python/sage class '%s' with %d different keys." % (row['owner_key'],many)

            #Create a class and a first instance for ekey=start.
            ekey = start #for exceptions
            print "    Testing for ekey =",start
            ex_instance = exerciseinstance(row,ekey=start,edict=edict)

            for ekey in range(start+1,start+many):
                print "    Testing for ekey =",ekey
                ex_instance.update(ekey=ekey)
        except SyntaxError as se:
            print "   Exercise class '%s' contains a syntax error on line %d." % (row['owner_key'],se.lineno)
            cl = row['class_text'].split()
            if len(cl)>se.lineno:
                print "      check line: %s" % cl[se.lineno-1]
            success = False
        except Exception as ee: # Exception will be in memory.
            print "    Error on exercise '{0}' with parameters edict={1} and ekey={2}".format(row['owner_key'],edict,ekey)
            print "    error description: ", ee
            if is_notebook():
                print "    Copy exercise code, only the class part, to a new cell. Then add the following command"
                print "%s().update(ekey=%d)" % (row['owner_key'],ekey)
                print "and execute with shift+enter. This may help finding the error line."
            else:
                print "    Test the exercise code, only the class part using the following command"
                print "%s().update(ekey=%d)" % (row['owner_key'],ekey)
                print "This may help finding the error line."
            success = False
        
        #Conclusion
        if not silent:
            if success:
                print "    No problems found in this test."
            else:
                print "    Review exercise '%s' based on the reported cases." % row['owner_key']

        return success


    def check_all(self,dest='.'):
        r""" 
        Check all exercises of this book for errrors.

        INPUT:

        OUTPUT:

            Printed message and True/False value.
        """

        all_ex = []
        for row in ExIter(self.book_store):
            if not self.is_exercise_ok(row,dest,silent=True):
                print "   Exercise '%s' have python/sage or compilation errors." % row['owner_key']
                all_ex.append(row['owner_key'])
        if all_ex:
            print "Review the following exercises:"
            for r in all_ex:
                print r
        else:
            print "No problem found."


    def search(self,regex):
        r"""
        Search all fields for a regular expression ``regex``.

        INPUT:
        - ``regex`` -- regular expression (see regex_ module).

        OUTPUT:
        - 
        
        .. _regex: http://docs.python.org/release/2.6.7/library/re.html
        """
        exlist = self.book_store.search(regex)
        for row in exlist:
            self._search_print_row(row)


    def _search_print_row(self,exrow):
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
        #Modify this
        sname = 'Exercise name %s' % exrow['owner_key'].encode('utf8')
        print sname + '\n' + exrow['problem_text'].encode('utf8') + '\n'


    def remove(self,owner_keystring,dest='.'):
        r"""
        Removing an exercise from the database.

        INPUT:

        - ``owner_keystring`` -- the class name.
        """

        #Get the exercise
        row = self.book_store.get_classrow(owner_keystring)
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
            self.book_store.remove_exercise(owner_keystring)
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
        row = self.book_store.get_classrow(owner_keystring)
        if not row:
            print "%s cannot be accessed on database" % owner_keystring
            return None
        #Create and print the instance
        ex_instance = exerciseinstance(row, ekey, edict)
        self.print_instance(ex_instance)
        return ex_instance



    def print_instance(self, ex_instance):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """
        #Derive this for other markups.

        summtxt =  ex_instance.summary()
        probtxt =  ex_instance.problem()
        answtxt =  ex_instance.answer()
        sname   =  ex_instance.name

        print '-'*len(sname)
        print sname 
        print '-'*len(sname)
        print summtxt.encode('utf8')
        print probtxt.encode('utf8')
        print answtxt.encode('utf8')



    def make_sws(self, dest='.'):
        sws = SWSExporter(self,dest)



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

#end class BookBase



def is_notebook():
    return sage.plot.plot.EMBEDDED_MODE


    r''' Remove this definition:

    def dbinstance(self, ex_class, ekey=None, edict=None):
        #Get summary, problem, answer and class_text
        row = self.book_store.get_classrow(ex_class.name)
        #Create instance
        return self.instance(ex_class.name,ex_class, row, ekey, edict)
    '''


