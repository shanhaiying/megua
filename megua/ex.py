r"""
This module defines the base class for exercise templating.

To build a database of exercise templates read details of module ``megbook``.
 

AUTHORS:

- Pedro Cruz (2010-03-01): initial version
- Pedro Cruz (2011-05-06): redefining Exercise templating.
- Pedro Cruz (2011-08): documentation strings with tests


EXAMPLES:

This examples can be tested using ``sage -python -m doctest ex.py`` or ``sage -t ex.py``.

Defining a new exercise template::

   >>> from ur import * 
   >>> from ex import Exercise
   >>> class AddingTwoIntegers(Exercise):
   ...     def make_random(self):
   ...         self.a = ZZ.random_element(-10,11)
   ...         self.b = ZZ.random_element(-10,11)
   ...     def solve(self):
   ...         self.c = self.a + self.b 

Create an instance::

   >>> adding_template = AddingTwoIntegers(name="adding_integers",ekey=10,edict=None,summary="Adding Integers",problem="Calculate $ a + b = res?$",answer="Result is: $res=c$")
   >>> print adding_template
   {'a': -4, 'c': -3, 'b': 1, '_summary_text': 'Adding Integers', 'name': 'adding_integers', 'ekey': 10, '_answer_text': 'Result is: $res=c$', '_problem_text': 'Calculate $ a + b = res?$'}
   >>> print adding_template.summary()
   Adding Integers
   >>> print adding_template.problem()
   Calculate $ -4 + 1 = res?$
   >>> print adding_template.answer()
   Result is: $res=-3$

Changing randomly the set of parameters::

   >>> adding_template.update(ekey=15) #another set of random parameters
   >>> print adding_template.problem()
   Calculate $ 2 + 10 = res?$
   >>> print adding_template.answer()
   Result is: $res=12$

Changing randomly but setting one of them::
    
   >>> adding_template.update(ekey=15,edict={'a':99}) #another set of random parameters
   >>> print adding_template.problem()
   Calculate $ 99 + 10 = res?$
   >>> print adding_template.answer()
   Result is: $res=109$

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

#Function that transforms input text in an exercise instance.
from paramparse import parameter_change
from platex import pcompile

#Import the random generator object.
from ur import ur 

from msc15 import *
import tikzmod

#Sage
from sage.all import *

#Warnings
# http://www.doughellmann.com/PyMOTW/warnings/
import warnings

import re
import tempfile

class Exercise:
    """Class ``Exercise`` is the base class for an exercise.

    In fact, this is an hybrid: is an Exercise Template and a concret Exercise.

    Derivations of this class will be specific Exercise Templates. A template of an exercise depends on numerical parameters. 
    The template is defined by a summary, a question and an answer text containing question parameters and solution parameters.
    The data paramters of the class define the dictionary that contains all parameters needed for substitution.

    The Exercise Template allows the following operations:
    * Return the dictionary of a specific exercise
    * Generate an exercise dictionary from a key
    * Generate an exercise dictionary from a given set of parameters
    * Give a textual (semi-latex) representation of the dictionary (question and full, non pedagogical, answer).
    * Give a textual description of the template.
    """


    """Class variables:
    - a derivation of class ``Exercise`` will inherit the values below.
    - a derivation of class ``Exercise`` should change this class parameters to new ones.
    """
    _summary_text = "A summary (from empty template)."
    _problem_text = "A problem (from empty template)."
    _answer_text = "An answer (from empty template)."



    def __init__(self,name="exercise",ekey=None,edict=None,summary=None,problem=None,answer=None):
        self.name = name
        #text fields: IMPORTANT: use SELF. on class globals!!!!
        if summary is not None:
            self._summary_text = summary
        if problem is not None:
            self._problem_text = problem
        if summary is not None:
            self._answer_text = answer
        #Guarantee a first set of parameters
        self.update(ekey,edict)


    def __str__(self):
        return str(self.__dict__)

    def __repr__(self): #python _ _ repr _ _
        return str(self.__class__) + r"(" + repr(self.__dict__) + ")"

    def _repr_(self): #sage _ repr _
        return str(self.__class__) + r"(" + repr(self.__dict__) + ")"

    def _latex_(self): #sage _ repr _
        return "To be done"

    def update(self,ekey=None,edict=None):
        #reset image list for the new parameters
        #TODO: this can generate inconsistency if make_random or solve are called alone.
        self.image_list = []

        #Initialize all random generators.
        self.ekey = ur.set_seed(ekey)

        #Call user derived function to generate a set of random variables.
        self.make_random()

        #Change all or some parameters existing in pdict.
        if edict is not None:
            self.__dict__.update(edict) 

        #Call user derived function to solve it.
        self.solve()


    def make_random(self):
        """
        Derive this function.
        """    
        pass


    def solve(self):
        """
        Derive this function.
        """    
        pass

    def rewrite(self,text):
        """
        Derive this function and implement rewritting rules to change latex expressions for example.
        """
        exp_pattern = re.compile(ur'e\^\{\\left\((.+?)\\right\)\}',re.U)
        out_text = re.sub(exp_pattern, r'e^{\1}', text)
        return text

    def summary(self):
        """
        Use class text self._summary_text and replace for parameters on dictionary. Nothing is saved.
        """
        return parameter_change(self._summary_text,self.__dict__)

    def problem(self):
        """
        Use class text self._problem_text and replace for parameters on dictionary. Nothing is saved.
        """
        text1 = parameter_change(self._problem_text,self.__dict__)
        return self._change_text(text1)

    def answer(self):
        """
        Use class text self._answer_text and replace for parameters on dictionary. Nothing is saved.
        """
        text1 = parameter_change(self._answer_text,self.__dict__)
        return self._change_text(text1)


    def _change_text(self,text1):
        text2 = self.rewrite(text1)
        text3 = self.latex_images(text2)
        return text3



    def name(self):
        return self.name


    def sage_graphic(self,graphobj,varname,dimx=5,dimy=5):
        gfilename = '%s-%s-%d'%(self.name,varname,self.ekey)
        #create if does not exist the "image" directory
        os.system("mkdir -p images") #The "-p" ommits errors if it exists.
        graphobj.save("images/"+gfilename+'.png',figsize=(dimx/2.54,dimy/2.54),dpi=100)
        self.image_list.append(gfilename) 
        return r"<img src='images/%s.png'></img>" % gfilename


    def latex_images(self,input_text):
        """When <latex dimx dimy> ... </latex> is present, then 
        it is necessary to produce them.
        """

        #VER LATEXIMG.PY


        #important \\ and \{

        #old pattern:
        #tikz_pattern = re.compile(r'\\begin\{tikzpicture\}(.+?)\\end\{tikzpicture\}', re.DOTALL|re.UNICODE)

        #print "Group 0:",match.group(0) #all
        #print "Group 1:",match.group(1) #scale (see http://www.imagemagick.org/script/command-line-processing.php#geometry)
        #print "Group 2:",match.group(2) #what is to compile

        latex_pattern = re.compile(r'<\s*latex\s+(\d+%)\s*>(.+?)<\s*/latex\s*>', re.DOTALL|re.UNICODE)

        #create if does not exist the "image" directory
        os.system("mkdir -p images") #The "-p" ommits errors if it exists.

        #Cycle through existent tikz code and produce pdf and png files.
        graphic_number = 0
        match_iter = re.finditer(latex_pattern,input_text)#create an iterator
        for match in match_iter:
            #Graphic filename
            gfilename = '%s-%d-%02d'%(self.name,self.ekey,graphic_number)
            print "=========="
            print gfilename
            print "=========="
            #Compile what is inside <latex>...</latex> to a image
            tikz_picture = match.group(2) 
            #TODO: mudar tikz_graphics para latex_image.tex
            #Note: compile only in a images/*.tex folder
            tikz_tex = Exercise.megbook.template("tikz_graphics.tex", pgfrealjobname=r"\pgfrealjobname{%s}"%self.name, beginname=r"\beginpgfgraphicnamed{%s}"%gfilename, tikz_picture=tikz_picture)
            pcompile(tikz_tex,'images','%s-%d-%02d'%(self.name,self.ekey, graphic_number),hideoutput=True)
            #convert -density 600x600 pic.pdf -quality 90 -resize 800x600 pic.png
            cmd = "cd images;convert -density 100x100 '{0}.pdf' -quality 95 -resize {1} '{0}.png'".format(
                gfilename,match.group(1),gfilename)
            print "============== CMD: ",cmd
            os.system(cmd)
            graphic_number += 1
            self.image_list.append(gfilename) 

        #Cycle through existent tikz code and produce a new html string .
        graphic_number = 0
        gfilename = '%s-%d-%02d'%(self.name,self.ekey,graphic_number)
        (new_text,number) = latex_pattern.subn(r"<img src='images/%s.png'></img>" % gfilename, input_text, count=1)
        while number>0:
            graphic_number += 1
            gfilename = '%s-%d-%02d'%(self.name,self.ekey,graphic_number)
            (new_text,number) = latex_pattern.subn(r"<img src='images/%s.png'></img>" % gfilename, new_text, count=1)
        
        #TODO: falta gravar as imagens na lista deste exercicio.

        return new_text







# --------------
# Instantiators
# --------------

"""
ERRORS:
- during class text preparse (including class name).
- 
"""

def exerciseclass(row):
    r"""
    Instantiates the `exercise class` (not an object) from text fields.
    """

    #Create the class (not yet the instance)

    #TODO:
    #   put class in globals(). 
    #   Now ex_name is on global space ?? 
    #   or is in this module space?

    #TODO: what if preparse fails with errors?
    sage_class = preparse(row['class_text'])
    try:
        print "====> Antes do exec"
        exec compile(sage_class,row["owner_key"],'eval')
        print "====> Depois do exec"
    except SyntaxError as se:
        tmp = tempfile.mkdtemp()
        pfilename = tmp+"/"+row["owner_key"]+".py"
        pcode = open(pfilename,"w")
        pcode.write("# -*- coding: utf-8 -*\n" + sage_class.encode("utf-8") )
        pcode.close()
        errfilename = "%s/err.log" % tmp
        os.system("sage -python %s 2> %s" % (pfilename,errfilename) )
        print "=====> tmp = ",tmp
        errfile = open(errfilename,"r")
        err_log = errfile.read()
        errfile.close()
        #remove temp directory
        os.system("rm -r %s" % tmp)
        print err_log
        raise SyntaxError  #to warn user


    #Get class name
    ex_class = eval(row['owner_key']) #String contents row['owner_key'] is now a valid identifier.

    #class fields
    ex_class._summary_text = row['summary_text']
    ex_class._problem_text = row['problem_text']
    ex_class._answer_text  = row['answer_text']

    return ex_class



def exerciseinstance(row, ekey=None, edict=None):
    r"""
    Instantiates the `exercise class` (not an object) from text fields.
    Then, creates an instance using  `exercise_instance` routine.

    This function creates an instance of a class named in parameter owner_keystring. That class must be already defined in memory.

    INPUT:

     - ``owner_keystring`` -- the class name (python string).
     - ``ex_class`` -- a class definition in memory.
     - ``row``-- the sqlite row containing fields: 'summary_text', 'problem_text',  'answer_text'.
     - ``ekey`` -- the parameteres will be generated for this random seed.
     - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.

    OUTPUT:
        An instance of class named ``owner_keystring``.

    NOTES:

        http://docs.python.org/library/exceptions.html#exceptions.Exception

    """


    #Create the class (not yet the instance). See exerciseclass definition above.
    ex_class = exerciseclass(row)

    #Create one instance of ex_class
    #With exception control:
    #try:
    #    print "ekey ", ekey, " start."
    #    ex_instance = ex_class(row['owner_key'],ekey,edict)
    #    print "ekey ", ekey, " end."
    #TODO: not working
    #except DeprecationWarning as dw:
    #    print "Warning on exercise '{0}' with parameters edict={1} and ekey={2}".format(row['owner_key'],edict,ekey)
    #    raise dw
    #except Exception as ee: # Exception will be in memory.
    #    print "Error on exercise '{0}' with parameters edict={1} and ekey={2}".format(row['owner_key'],edict,ekey)
    #    raise ee

    #Create one instance of ex_class
    #without exception control.
    ex_instance = ex_class(row['owner_key'],ekey,edict)

    return ex_instance


def to_unicode(s):
    if type(s)!=unicode:
        return unicode(s,'utf-8')
    else:
        return s


