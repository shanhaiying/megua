r"""
This module defines the base class for exercise templating.

To build a database of exercise templates read details of module ``megbook``.
 

AUTHORS:

- Pedro Cruz (2010-03-01): initial version
- Pedro Cruz (2011-05-06): redefining Exercise templating.
- Pedro Cruz (2011-08): documentation strings with tests
- Pedro Cruz (2013-01): Exercise can be derived for other types than pdflatex.


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

class Exercise:
    """Class ``Exercise`` is the base class for an exercise **template**.

    Derivations of this class will be specific Exercise Templates. A template of an exercise depends on numerical parameters. 
    The template is defined by a summary, a problem and an answer text containing question parameters and solution parameters.
    The data parameters of the sage/python class define the dictionary that contains all parameters needed for substitution.

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
    _owner_key = None
    _summary_text = None
    _problem_text = None
    _answer_text = None

    #Auxiliar
    _env

    #def __init__(self,ownerkey=None,ekey=None,edict=None,summary=None,problem=None,answer=None):
    #    self.ownerkey = ownerkey
    #    #text fields: IMPORTANT: use SELF. on class globals!!!!
    #    if summary is not None:
    #        self._summary_text = summary
    #    if problem is not None:
    #        self._problem_text = problem
    #    if summary is not None:
    #        self._answer_text = answer
    #    #Guarantee a first set of parameters
    #    self.update(ekey,edict)


    def __init__(self,ekey=None,edict=None):
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
        #Initialize all random generators.
        self.ekey = ur.set_seed(ekey)

        #Call user derived function to generate a set of random variables.
        self.make_random()

        #Change all or some parameters existing in pdict.
        if edict is not None:
            self.__dict__.update(edict) 

        #Call user derived function to solve it.
        self.solve()

        #Create textual instances
        self.owner_key = self._owner_key
        self.summary_utf8 = self._summary()
        self.problem_utf8 = self._problem()
        self.answer_utf8 = self._answer()

    def _summary(self):
        """
        Use class text self._summary_text and replace for parameters on dictionary. Nothing is saved.
        """
        return parameter_change(self._summary_text,self.__dict__)

    def _problem(self):
        """
        Use class text self._problem_text and replace for parameters on dictionary. Nothing is saved.
        """
        in_text = parameter_change(self._problem_text,self.__dict__)
        out_text = self.rewrite(in_text)
        return out_text

    def _answer(self):
        """
        Use class text self._answer_text and replace for parameters on dictionary. Nothing is saved.
        """
        #return parameter_change(self._answer_text,self.__dict__)
        in_text = parameter_change(self._answer_text,self.__dict__)
        out_text = self.rewrite(in_text)
        return out_text

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
            tmpl = self._env.get_template(filename)
        except jinja2.exceptions.TemplateNotFound:
            return "ex.py -- missing template %s"%filename
        r = tmpl.render(**user_context)
        return r


    def view(self):
        """Print the exercise in a nice format, if possible.
        OUTPUT:

        * True if view is possible. False otherwise.
        """

        if is_notebook():
            return self.view_nb()
        else:
            self.view_cl()


    # ==========================
    # Markup language services.
    # ==========================

    def markuplang_test(self):
        """In case of latex, only after sucessful compilation one knows if latex markup is ok."""
        return self.view()


    # ============================
    # Methods to print and export.
    # ============================


    def view_cl(self)
        #Use jinja2 template to generate LaTeX.
        self.latex_string = self.template("PDFLatexExercise_print.tex",self)
        #Produce PDF file from LaTeX.
        return pcompile(latex_string, '.', self.owner_key)

    def view_nb(self):
        #Use jinja2 template to generate LaTeX.
        self.latex_string = self.template("PDFLatexExercise_print.tex",self)
        #Produce PDF file from LaTeX.
        return pcompile(latex_string, '.', self.owner_key)


    # =====================================
    # Methods to build the parametrization.
    # =====================================

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

    def print(self):
        pass


    def rewrite(self,text):
        """
        Derive this function and implement rewritting rules to change latex expressions for example.
        """
        exp_pattern = re.compile(ur'e\^\{\\left\((.+?)\\right\)\}',re.U)
        out_text = re.sub(exp_pattern, r'e^{\1}', text)
        return text





# --------------
# Instantiators
# --------------

"""
ERRORS:
- during class text preparse (including class name).
- 
"""


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

    #Parse text, extract sage/python textual class definition, then
    #interpret it and put it in memory.
    sage_class_text = preparse(row['class_text'])
    exec sage_class_text #here the ExerciseTemplate class gets known by python

    #Now row['owner_key'] exists in memory as a class.
    #Get class from text name
    ex_class = eval(row['owner_key']) #String contents row['owner_key'] is now a valid identifier.

    #Create one instance of ex_class
    #class fields
    ex_class._owner_key = row['owner_key']
    ex_class._summary_text = row['summary_text']
    ex_class._problem_text = row['problem_text']
    ex_class._answer_text  = row['answer_text']

    ex_instance = ex_class(ekey, edict)

    return ex_instance





    #Create the class (not yet the instance). See exerciseclass definition above.
    #ex_class = exerciseclass(row)

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


def to_unicode(s):
    if type(s)!=unicode:
        return unicode(s,'utf-8')
    else:
        return s

def is_notebook():
    return sage.plot.plot.EMBEDDED_MODE

