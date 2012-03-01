# vim:fileencoding=iso-8859-15
# -*- coding: iso-8859-15 -*-

r"""
Base class and functions for exercise constructions.

Database sqlite

Edition with sqlitebrowser


AUTHORS:

- Pedro Cruz (2010-03-01): initial version


Lots and lots of examples.

Usage:

import meg.all as m
m.new( m.primitive_001, key=10)
m.skins.set('pt_pt','tex','latex')
m.skins.search('primitiva')


Developing a new exercise:
1. Go to the proper directory (algebra, calculus1v, numerics, etc)
2. Create some <name>.tex file and write the QUESTION and ANSWER.
3. Create <exercise>.py like others.
3. Call sage at that directory. Then
    import meg  #this will import from standard sage  instalation of meg
    attach <exercise>.py
    <exercise>.solve_sample_file('<name>.tex')
5. Make corrections in both files.


Using meg on notebook:
1. import meg
2.  

I usually use:

   html("$%s$"%latex(object)) 

http://docs.python.org/tutorial/modules.html

"""


#*****************************************************************************
#       Copyright (C) 2008 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  


#from string import Template
#import tempfile
#import os

# Coding http://www.sagemath.org/doc/developer/conventions.html

# http://docs.python.org/reference/simple_stmts.html#import

import os

import json

"""
Importing everything from sage.all

Avoid this is very difficult or even impossible.

For example:
  from sage.rings.real_double import RDF 
does not work.
"""
from sage.all import *


import re

from string import Template    
class TemplateI(Template):
    delimiter='«'



x=var('x')
R15=RealField(15)



def showmul(x):
    if x < 0 :
        return '(' + str(x) + ')'
    else:
        return str(x)




class SageJSONEncoder(json.JSONEncoder):

    """
    sage: sage.rings.all.is_RealNumber(2.3)
    True
    sage: sage.rings.all.is_RealNumber(float(2.3))
    False
    sage: sage.rings.all.is_Integer(2)
    True
    sage: sage.rings.all.is_Integer(int(2))
    False
    
    http://docs.python.org/library/json.html#encoders-and-decoders

    File:
        sage/devel/sage-main/sage/server/simple/twist.py

    try:
        print json.JSONEncoder().encode({"a": "bb"}) #replace "bb" by 1.8, sqrt(2).n(), or 123
    except TypeError:
        print "Doesn't work."
        pass

    print SageJSONEncoder().encode({"a": 1.8})
    print SageJSONEncoder().encode({"a": sqrt(2).n()})
    print SageJSONEncoder().encode({"a": 123})

    """
    def default(self,o):
        #print "----------\n\n"
        #print "Type of " + str(o) + " is " + str(type(o))
        #print "----------\n\n"
        try:
            res = str(o)
            #if sage.rings.all.is_RealNumber(o) or sage.rings.all.is_RealDoubleElement(o):
            #if isinstance(o,sage.rings.real_mpfr.RealLiteral) or \
            #   isinstance(o,sage.rings.real_mpfr.RealNumber) or \
            #   isinstance(o,sage.rings.real_double.RealDoubleElement):
            #    res = str(o)
            #elif sage.rings.all.is_Integer(o):
            #    res = str(o)
            #elif o in QQ:
            #    res = str(o)
            #else:
            #    raise TypeError
        except TypeError:
            pass
        else:
            return res
        return json.JSONEncoder.default(self,o)



megencoder = SageJSONEncoder()
megdecoder = json.JSONDecoder(parse_float=RDF)

    

#from sage.structure.sage_object import SageObject

class Exercise:
    """Base Class.  An Exercise Template is a template of an exercise that depends on numerical parameters. The template 
       is defined by a question and an answer dictionary containing question parameters and solution parameters, also, with details of
       the resolution. The question numerical parameters can be generated or given.  The data structure is on dictionary containing 
       all parameters involved.
       The Exercise Template allows the following operations:
        * Return the dictionary of a specific exercise
        * Generate an exercise dictionary from a seed
        * Generate an exercise dictionary from a given set of parameters
        * Give a textual (semi-latex) representation of the dictionary (question and full, non pedagogical, answer).
        * Give a textual description of the template.
    """

    def __init__(self,name=None,key=None):
        """
        If name==None try to get a name.
        If key not equal zero try set it
        """

         
        self.seed = None #seed is an instance of Seed or None
        self.name = name

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self): #python _ _ repr _ _
        return str(self.__class__) + r"(" + repr(self.__dict__) + ")"

    def _repr_(self): #sage _ repr _
        return str(self.__class__) + r"(" + repr(self.__dict__) + ")"

    def _latex_(self): #sage _ repr _
        return "To be done"

    def json_decode(self,jsonstr):
        #http://docs.python.org/library/stdtypes.html#context-manager-types
        self.__dict__.update(megdecoder.decode(jsonstr))
        #self.ex_dict = megdecoder.decode(jsonstr)

    def json_encode(self):
        #print self.ex_dict
        return megencoder.encode(self.__dict__)

    def make_random(self,seed):
        r.set_seed(seed)
        self.seed = seed
        #self.__dict = dict()

    def solve(self):
        None

    def solvejson(self,jsonstr):
        self.json_decode(jsonstr) #derivative class should supply this?
        self.solve()
        return self.json_encode()

    def solvejson_random(self,seed):
        self.make_random(seed)
        self.solve()
        return self.json_encode()

    def get_random(self,seed):
        self.make_random(seed)
        return self.json_encode()

#    def get_vars(self):
#        re.findall(r'[^a-zA-Z]([io][nt][a-zA-Z]+[a-zA-Z0-9]*)',r'$inVar$ etc etc $inVar / otVar$')
#        list(set(solution))


    def subs(self,text):
        #Improve representation of negative numbers:
        #  Case:  5 + -2x --> 5 + (-2)x
        #  Case:  5 + -1x --> 5 + (-x)
        #  Should the object be inside sage ?
        q = re.sub(r'([io][nt])', '«\g<1>', text)
        #print "After insertion of «"
        #print q

        res = TemplateI(q).safe_substitute(self.__dict__)
        #print "\n\nAfter replacing og ina11"
        #print res

        q2 = re.sub(r'«([io][nt])', '\g<1>', res)
        #print "\n\nAfter removing «"
        #print q2

        return q2


    def new_exercisefromfile(self,filename,key):
        self.make_random(key)
        self.solve()
        return self.subs_file(filename)

    def new_exercisefromtext(self,txt,key):
        self.make_random(key)
        self.solve()
        return self.subs(txt)


    def subs_file(self,filename):
        f = open(filename,'r')
        text = f.read()
        otext = self.subs(text)
        f.close()
        return otext

    def subs_file_file(self,filen_in,filen_out):
        f = open(filen_in,'r')
        text = f.read()
        otext = self.subs(text)
        f.close()
        f = open(filen_out,'w')
        f.write(otext)
        f.close()
        return otext

    def solve_sample_file(self,filename):
        self.make_random(0)
        self.solve()
        self.subs_file(filename)


"""
if __name__ == "__main__":

    e = Exercise()
    print e
    
"""
    




