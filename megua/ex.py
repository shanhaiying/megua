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
  

#MEGUA modules
from paramparse import parameter_change
from platex import pcompile
from mathcommon import *
from msc15 import * #algebra
from msc26 import *
from msc60 import * #probability
from msc62 import * #statistics
from msc65 import * #numerical


#Import the random generator object.
from ur import ur 
#, edict=" + str(edict) + ")\n")
import tikzmod
import subprocess

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

#, edict=" + str(edict) + ")\n")
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

        #Case when exercise is multiplechoice
        self.all_choices = []
        self.has_multiplechoicetag = None #Don't know yet.
        self.detailed_answer= None

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
        """#, edict=" + str(edict) + ")\n")
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
        """Called after parameter_change call. See above."""
        text2 = self.rewrite(text1)
        if text2 is None:
            raise NameError('rewrite(s,text) function is not working.')
        text3 = self.latex_images(text2)
        text4 = self.show_one(text3)
        self.multiplechoice_parser(text4)  #extract information but don't change text
        return text4 



    def name(self):
        return self.name


    def show_one(self,input_text):
        """Find all <showone value>...</showone> tags and select proper <thisone>...</thisone>
        Change it in the original text leaving only the selected ... in <thisone>...</thisone>
        """

        showone_pattern = re.compile(r'<\s*showone\s+(\d+)\s*>(.+?)<\s*/showone\s*>', re.DOTALL|re.UNICODE)

        #Cycle through all <showone> tags
        match_iter = re.finditer(showone_pattern,input_text)#create an iterator
        new_text = ''
        last_pos = 0
        for match in match_iter:

            #Get list of possibilities
            #print "===>",match.group(2)
            possibilities = self._showone_possibilities(match.group(2))

            #Get selected possibility
            #TODO: check range and if group(1) is a number.
            pnum = int(match.group(1))
            #print "===>",pnum

            #Text to be written on the place of all options
            possibility_text = possibilities[pnum]

            #new_text = new_text[:match.start()] + possibility_text + new_text[match.end():] 
            new_text += input_text[last_pos:match.start()] + possibility_text
            last_pos = match.end()

        new_text += input_text[last_pos:]

        return new_text


    def _showone_possibilities(self,text_with_options):
        """Find all tags <thisone>...</thisone> and make a list with all `...`
        """

        thisone_pattern = re.compile(r'<\s*thisone.*?>(.+?)<\s*/thisone\s*>', re.DOTALL|re.UNICODE)

        #Cycle through all <showone> tags
        match_iter = re.finditer(thisone_pattern,text_with_options)#create an iterator
        options = []
        for match in match_iter:
            options.append( match.group(1) )

        return options

        

    def sage_graphic(self,graphobj,varname,dimx=5,dimy=5, arrows=False):
        """This function is to be called by the author in the make_random or solve part.
        INPUT:

        - `graphobj`: some graphic object.

        - `varname`: user supplied string that will be part of the filename.

        - `dimx` and `dimy`: size in centimeters.

        - `arrows`: if ``arrows=True`` **try** to put arrows in the axis extremes.
        """ 
        #Arrows #TODO: this is not working
        if arrows:
            xmin = graphobj.xmin()
            xmax = graphobj.xmax()
            ymin = graphobj.ymin()
            ymax = graphobj.ymax()
            xdelta= (xmax-xmin)/10.0
            ydelta= (ymax-ymin)/10.0
            graphobj += arrow2d((xmin,0), (xmax+xdelta, 0), width=0.1, arrowsize=3, color='black') 
            graphobj += arrow2d((0,ymin), (0, ymax+ydelta), width=0.1, arrowsize=3, color='black') 

        gfilename = '%s-%s-%d'%(self.name,varname,self.ekey)
        #create if does not exist the "image" directory
        os.system("mkdir -p images") #The "-p" ommits errors if it exists.
        if arrows:
            #TODO: clip figure for avoid -->---  extra ---
            graphobj.save("images/"+gfilename+'.png',figsize=(dimx/2.54,dimy/2.54),dpi=100)
        else:
            graphobj.save("images/"+gfilename+'.png',figsize=(dimx/2.54,dimy/2.54),dpi=100)
        self.image_list.append(gfilename) 
        return r"<img src='images/%s.png'></img>" % gfilename



    def sage_staticgraphic(self,fullfilename,dimx=150,dimy=150):
        """This function is to be called by the author in the make_random or solve part.

        INPUT:

        - `fullfilename`: full filename for the graphic or picture.
        - `dimx` and `dimy`: display image in (dimx,dimy) pixels.

        NOTES:
            - see also ``s.sage_graphic``.
        """ 
        #create if does not exist the "image" directory
        os.system("mkdir -p images") #The "-p" ommits errors if it exists.
        os.system("cp %s images" % fullfilename)
        gfilename = os.path.split(fullfilename)[1]
        #print "gfilename=",gfilename
        self.image_list.append(gfilename) 
        return r"<img src='images/%s' alt='%s' height='%d' width='%d'></img>" % (gfilename,self.name+' graphic',dimx,dimy)

    def latex_images(self,input_text):
        """When <latex percent%> ... </latex> is present, then 
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
        latex_error_pattern = re.compile(r"!.*?l\.\d+(.*?)$",re.DOTALL|re.M)

        #create if does not exist the "image" directory
        os.system("mkdir -p images") #The "-p" ommits errors if it exists.

        #Cycle through existent tikz code and produce pdf and png files.
        graphic_number = 0
        match_iter = re.finditer(latex_pattern,input_text)#create an iterator
        for match in match_iter:
            #Graphic filename
            gfilename = '%s-%d-%02d'%(self.name,self.ekey,graphic_number)
            #print "=========="
            #print gfilename
            #print "=========="
            #Compile what is inside <latex>...</latex> to a image
            tikz_picture = match.group(2) 
            #TODO: mudar tikz_graphics para latex_image.tex
            #Note: compile only in a images/*.tex folder
            try:
                tikz_tex = Exercise.megbook.template("tikz_graphics.tex", 
                                pgfrealjobname=r"\pgfrealjobname{%s}"%self.name, 
                                beginname=r"\beginpgfgraphicnamed{%s}"%gfilename, 
                                tikz_picture=tikz_picture)
                pcompile(tikz_tex,'images','%s-%d-%02d'%(self.name,self.ekey, graphic_number))
                #convert -density 600x600 pic.pdf -quality 90 -resize 800x600 pic.png
                cmd = "cd images;convert -density 100x100 '{0}.pdf' -quality 95 -resize {1} '{0}.png' 2>/dev/null".format(
                    gfilename,match.group(1),gfilename)
                #print "============== CMD: ",cmd
                os.system(cmd)
                os.system("cp images/%s.tex ." % gfilename)
                graphic_number += 1
                self.image_list.append(gfilename) 
            except subprocess.CalledProcessError as err:
                #Try to show the message to user
                #print "Error:",err
                #print "returncode:",err.returncode
                #print "output:",err.output
                print "================"
                match = latex_error_pattern.search(err.output) #create an iterator
                if match:
                    print match.group(0)
                else:
                    print "There was a problem with an latex image file."
                print "You can download %s.tex and use your windows LaTeX editor to help find the error." % gfilename
                print "================"
                os.system("cp images/%s.tex ." % gfilename)
                raise Exception


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


    def multiplechoice_parser(self,input_text):
        """When <multiplechoice>...</multiplecoice> is present it parses them
        and puts each option in exercise fields: 

        * self.all_choices: list of all choices.
        * self.detailed_answer: full detailed answer.
        * self.has_multiplechoicetag: tell that choices came from this syntax

        This routine only extracts information
        Does not change the "answer" or "problem" part like the latex_images that
        needs to put <img ... fig filename>

        """

        if "CDATA" in input_text:
            #TODO: should issue warning when CDATA and multiplechoice are both present.
            return 


        #Find and extract text inside <multiplechoice>...</multiplechoice>
        choices_match = re.search(r'<\s*multiplechoice\s*>(.+?)<\s*/multiplechoice\s*>', input_text, re.DOTALL|re.UNICODE)
        
        if choices_match is None:
            return 
        #print "group 0=",choices_match.group(0)
        #print "group 1=",choices_match.group(1)

        #Text inside tags <multiplechoice> ... </multiplechoice>
        choice_text = choices_match.group(1)

        #Get all <choice>...</choice>
        choice_pattern = re.compile(r'<\s*choice\s*>(.+?)<\s*/choice\s*>', re.DOTALL|re.UNICODE)

        #Collects all <choice>...</choice> pairs
        match_iter = re.finditer(choice_pattern,choice_text) #create an iterator
        self.all_choices = [ "<center>"+match.group(1)+"</center>" for match in match_iter]
        #print "=========================="
        #print self.all_choices
        #print "=========================="
        

        #Find detailed answer and save it
        self.detailed_answer = input_text[choices_match.end():].strip("\t\n ")
        #print "=========================="
        #print self.detailed_answer
        #print "=========================="

        #For sending it's important to know where options are stored.
        self.has_multiplechoicetag = True





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
    Interpret the `exercise class` (not an object) from text fields.
    """

    #Create the class (not yet the instance)

    #TODO:
    #   put class in globals(). 
    #   Now ex_name is on global space ?? 
    #   or is in this module space?

    try:
        #exec compile(sage_class,row["owner_key"],'eval')
        #TODO: http://www.sagemath.org/doc/reference/misc/sage/misc/sage_eval.html
        # and spread this for more points in code.
        sage_class = preparse(row['class_text'])
        exec sage_class
    except: 
        tmp = tempfile.mkdtemp()
        pfilename = tmp+"/"+row["owner_key"]+".sage"
        pcode = open(pfilename,"w")
        pcode.write("# -*- coding: utf-8 -*\nfrom megua.all import *\n" + row['class_text'].encode("utf-8") )
        pcode.close()
        errfilename = "%s/err.log" % tmp
        os.system("sage -python %s 2> %s" % (pfilename,errfilename) )
        errfile = open(errfilename,"r")
        err_log = errfile.read()
        errfile.close()
        #TODO: adjust error line number by -2 lines HERE.
        #....
        #remove temp directory
        #print "=====> tmp = ",tmp
        os.system("rm -r %s" % tmp)
        print err_log #user will see errors on syntax.
        raise SyntaxError  #to warn user #TODO: not always SyntaxError


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
    try:
        ex_instance = ex_class(row['owner_key'],ekey,edict)
    except: 
        tmp = tempfile.mkdtemp()
        pfilename = tmp+"/"+row["owner_key"]+".sage"
        pcode = open(pfilename,"w")
        pcode.write("# -*- coding: utf-8 -*\nfrom megua.all import *\n" + row['class_text'].encode("utf-8")+"\n")
        pcode.write(row['owner_key'] + "(ekey=" + str(ekey) + ", edict=" + str(edict) + ")\n")
        pcode.close()
        errfilename = "%s/err.log" % tmp
        os.system("sage %s 2> %s" % (pfilename,errfilename) )
        errfile = open(errfilename,"r")
        err_log = errfile.read()
        errfile.close()
        #TODO: adjust error line number by -2 lines HERE.
        #....
        #remove temp directory
        #print "=====> tmp = ",tmp
        os.system("rm -r %s" % tmp)
        print err_log
        raise Exception  #to warn user #TODO: not always SyntaxError


    return ex_instance


def to_unicode(s):
    if type(s)!=unicode:
        return unicode(s,'utf-8')
    else:
        return s


