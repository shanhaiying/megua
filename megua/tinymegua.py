


#Random numbers from numpy
#http://docs.scipy.org/doc/numpy/reference/routines.random.html
import numpy.random as nprandom

#Random numbers with python
import random
import time #re-start random

#Random numbers from R using RPy2
# 1. Always do casts to python rpy2 commands.
# 2. To do: study how does rpy2 works.
import rpy2.robjects as robjects



class UnifiedRandom:

    """Check every function in the module for how to use details.
    """

    #See squnif for details about this list. 
    _qlist = [Integer(1)/Integer(9), Integer(1)/Integer(8), Integer(1)/Integer(7),
Integer(1)/Integer(6), Integer(1)/Integer(5), Integer(2)/Integer(9),
Integer(1)/Integer(4), Integer(2)/Integer(7), Integer(1)/Integer(3),
Integer(3)/Integer(8), Integer(2)/Integer(5), Integer(3)/Integer(7),
Integer(4)/Integer(9), Integer(1)/Integer(2), Integer(5)/Integer(9),
Integer(4)/Integer(7), Integer(3)/Integer(5), Integer(5)/Integer(8),
Integer(2)/Integer(3), Integer(5)/Integer(7), Integer(3)/Integer(4),
Integer(7)/Integer(9), Integer(4)/Integer(5), Integer(5)/Integer(6),
Integer(6)/Integer(7), Integer(7)/Integer(8), Integer(8)/Integer(9)]

    _qlen = len(_qlist)


    def _init_(self,seed_value=None):
        self.set_seed(seed_value)

    def __repr__(self):
        return "UnifiedRandom(%d)" % self.seed_value

    def set_seed(self,seed_value=None):
        """ Set seeds from all random number libraries to the "same" value.

        INPUT:

        - ``seed_value`` -- an Integer.

        OUTPUT:

           Same integer.

        Seed commands:

        1. Sage: set_random_seed, seed.
        2. R: set.seed

        To do: 

        1. check what happens with simultaneous notebooks 
        and worksheets and also in a shared "sage" instance.

        2. Change random_seed set.

        """

        #NOTE: change this.
        random_seed = int(time.time())

        #Keep in memory, use int to convert from sage to python int
        if seed_value==None:
            self.seed_value = random_seed
        else:
            self.seed_value = int(seed_value)

        #set SAGE random seed
        set_random_seed(self.seed_value)
        #set PYTHON random seed
        random.seed(self.seed_value)
        #set R from rpy2
        self._rpy2_setseed(self.seed_value) 
        #Set NUMPY seed
        nprandom.seed(int(self.seed_value))

        return self.seed_value

    def random_element(self,somelist=[exp(1),pi,sqrt(2)]):
        """
        Returns an element from the ``somelist`` parameter.

        INPUT:

        - ``somelist`` -- a list, for example ``[exp(1),pi,sqrt(2)]``.

        OUTPUT:

        A random element from the input list.
        """

        l = len(somelist)
        i = ZZ.random_element(l)
        return somelist[i]


    def iunif(self,a,b):
        """
        Integer random number from a uniform distribution (iunif).
        Seed is from Sage random module.

        INPUT:

        - ``a`` -- minimum integer

        - ``b`` -- maximum integer

        OUTPUT:

            Integer

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.set_seed(10)
            10
            sage: ur.iunif(-10,10)
            -4
            sage: ur.iunif(-10,10)
            1

        Notes: iunif function returns ZZ.random_element(a,b+1)
        """

        return ZZ.random_element(a,b+1) #An integer in [a,b]
 

    def iunif_nonset(self,a,b,nonset):
        """
        Integer random number from a uniform distribution excluding numbers on "nonset".
        Seed is from Sage random module.

        INPUT:

        - ``a`` -- minimum integer

        - ``b`` -- maximum integer

        OUTPUT:

            Integer

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.set_seed(10)
            10
            sage: ur.iunif_nonset(-10,10,[-1,0,1]) #exclude [-1,0,1]
            -4
            sage: ur.iunif_nonset(-10,10,[-1,0,1]) #exclude [-1,0,1]
            4

        To do: improve this algorithm.
        """
        nonset = set(nonset) #remove duplicates
        n = b-a+1 #number of integers from a to b
        m = len(nonset) #number of excluded cases
        rd_yes = ZZ.random_element(n-m) #Get a random number from 0 to (n-m-1)
        #Choose the rd 'y'
        #  -3 -2 -1 0 1 2 3 (i iterator)
        #   y  n y  y n y y (yes iterator)
        i=a-1
        yes=-1
        while yes<rd_yes:
            i += 1        
            if i not in nonset:
                yes += 1
        return i


    def runif(self,a,b,prec=None):
        """
        Real random number from a uniform distribution.
        Seed is from Sage random module.

        INPUT:

        - ``a`` -- minimum integer

        - ``b`` -- maximum integer

        - ``prec`` -- number of decimal digits (default all).

        OUTPUT: 

        An ``RealDoubleField`` (or ``RDF``) number.

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.set_seed(10)
            10
            sage: ur.runif(-10,10,2) 
            -8.74
            sage: ur.runif(-10,10) 
            -7.17316398804125

        """
        res = RR.random_element(a,b)
        if prec:
            res = round(res,prec)
        return res


    def rnorm(self,mean,stdev,prec=None):
        """
        Real random number from a normal distribution.
        Seed is from Sage random module.

        INPUT:

        - ``mean`` -- mean value of the Normal distribution.

        - ``stdev`` -- standard deviation of the Normal distribution.

        - ``prec`` -- number of decimal digits (default all).

        OUTPUT:

        An ``RealDoubleField`` (or ``RDF``) number.

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.set_seed(10)
            10
            sage: ur.rnorm(0,1,2) 
            1.33
            sage: ur.rnorm(0,1) 
            -0.11351682931886863

        Another possible implemention::

            #rpy version 
            rnum = rnorm(1,RDF(mean),RDF(sigma))._sage_()
            #rpy2 version
            rnum = rpy2_rnorm(1,float(mean),float(sigma))[0]

        """
        #sage version
        rnum = normalvariate(mean,stdev) #rnum is a float
        if prec:
            rnum = round(rnum, prec)
        return rnum


    def rbernoulli(self):
        """
        Generate 0 or 1 randonly.
        Seed is from Sage random module.

        INPUT: no need.

        OUTPUT:

            0 or 1.

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.set_seed(10)
            10
            sage: ur.rbernoulli() 
            1
            sage: ur.rbernoulli() 
            1

        """
        return int(getrandbits(1))
    

    def squnif(self):
        """
        Random select pure rationals (no integers) that are suitable for easy hand calculations over a predefined list:

        1. `squnif`` means 'selected from Q using uniform distribution'.
        2. Extracts negative or positive rationals in the form `a/b` where::

            b in 1,2,3,4,5,6,7,8,9
            a in 1,2,...,b

        3. No integer numbers.
        4. No duplicates (`2/4` is not produced, only `1/2`).
        5. See implementation notes below for more details.

        Seed is from Sage random module.

        INPUT: nothing

        OUTPUT:

        A rational number from -8/9 to 8/9 usign single digits on numerator and denominator (integeres excluded).

        EXAMPLES::
 
            sage: from megua.ur import ur
            sage: ur.set_seed(10)
            10
            sage: ur.squnif() 
            -1/4
            sage: ur.squnif() 
            -4/9
 
        IMPLEMENTATION NOTES:

        1. Check class variable UnifiedRandom._qlist.
        2. This module is a pure python module so 1/3 results in 0. One must use Integer(1)/Integer(3)::
        3. Testing::

            sage: from sage.all import *
            sage: qq = [ Integer(a+1)/Integer(b+1) for b in range(9) for a in range(b)]
            sage: ql = list(set(qq)); ql
            [2/3, 1/3, 4/7, 1/5, 1/4, 3/5, 3/4, 1/9, 1/8, 8/9, 3/8, 4/9, 5/7, 7/9, 7/8, 1/2, 3/7, 2/7, 6/7, 1/7, 2/5, 4/5, 2/9, 5/9, 5/8, 1/6, 5/6]
            sage: ql.sort()
            sage: print ql
            [1/9, 1/8, 1/7, 1/6, 1/5, 2/9, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 4/9, 1/2, 5/9, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 7/9, 4/5, 5/6, 6/7, 7/8, 8/9]
            sage: len(ql)
            27
            sage: from megua.ur import ur
            sage: print ur._qlist
            [1/9, 1/8, 1/7, 1/6, 1/5, 2/9, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 4/9, 1/2, 5/9, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 7/9, 4/5, 5/6, 6/7, 7/8, 8/9]
            sage: print ur._qlen
            27

        """
        qr = ZZ.random_element(UnifiedRandom._qlen)
        if self.rbernoulli() == 0:
            return - UnifiedRandom._qlist[qr]
        else:
            return + UnifiedRandom._qlist[qr]


    """
    RPy2 wrappers
     
    Postpone::

        def rpy2_multinomial(self,....)
        rpy2_multinomial = robjects.r['rmultinom']

        def rpy2_runif(self,...)
        rpy2_runif = robjects.r["runif"]

    """ 

    def _rpy2_setseed(self,seed):
        """
        Set seed for RPy2 module.
        See set_seed on this module.
        """
        setseed = robjects.r['set.seed']
        setseed(int(seed))


    def rpy2_rnorm(self,mean,stdev,prec=None):
        """
        Random number from Normal distribution. 

        NOTES:

        - Based on RPy2 module (seed is from RPy2).

        INPUT:

        - ``mean`` -- mean value of the Normal distribution.

        - ``stdev`` -- standard deviation of the Normal distribution.

        - ``prec`` -- number of decimal digits (default all).

        OUTPUT:

            A random number from Normal distribution with given parameters.

        EXAMPLES::
 
            sage: from megua.ur import ur
            sage: ur.set_seed(10)
            10
            sage: ur.rpy2_rnorm(0,1,2) #two decimals 
            0.02
            sage: ur.rpy2_rnorm(0,1) 
            -0.18425254206906366
 
        """
        rnorm = robjects.r['rnorm']
        res = rnorm(1,float(mean),float(stdev))[0]
        if prec:
            res = round(res,prec)
        return res
    



#==========
# Instance
#==========
"""
The global instance ``ur=UnifiedRandom()``::

   sage: from megua.ur import ur
   sage: ur 
   UnifiedRandom(10)
"""
ur = UnifiedRandom()






#===========================================================




# -*- coding: iso-8859-15 -*-
# vim:fileencoding=iso-8859-15

r"""
Substitution on a given input text with named placeholders ('variables') by their respective values provided a dictionary.


AUTHORS:

- Pedro Cruz (2010-06): initial version
- Pedro Cruz (2011-08): documentation strings


Types of variables are:

1. ``name``: the ``name`` is directly substituted by the result of ``latex(value)`` where value is the value on the dict.
2. ``name@()``: substitution for ``\left( latex(value) \right)`` if value for name is negative (w.o. () otherwise).
3. ``name@f{2.3g}``: formatted substitution. In the example: substitution for ``"%2.3g" % value`` (this is a python expression).
4. ``name2@s{R15}``: function call substitution. In the example: substitution for ``R15(value)`` (R15 is a user function).
5. ``name3@{"text0","text1",...}``: In the example, if name3 is 0 then "text0" will appear, if name3 is 1 then text1" will appear, and so on.


EXAMPLES:

.. test as a python module with:    sage -python -m doctest paramparse.py

An example of each kind::

The text "1) name  2) name2@() 3) name@f{2.3g} 4) name2@s{sin}" has 4 placeholders that will be changed.

   >>> from paramparse import parameter_change
   >>> txt = r'''Examples: 1) name  2) name2@() 3) name@f{2.3g} 4) name@s{sin} 5) name3@c{"text0", "tex-t1"}'''
   >>> newdict = {'name': -12.123456, 'name2': -34.32, 'name3': 1, '__init__': 'the init', 'self': 'the self' }
   >>> parameter_change(txt,newdict)
   u'Examples: 1) -12.123456  2) \\left(-34.32\\right) 3) -12.1 4) 0.42857465435 5) tex-t1'
   >>> newdict = {'name3': 1 }
   >>> txt = u'''1) name3@c{"text0", "c\xc3o"} 2) name3@c{"n\xc3o", "name1"} 3) name3@c{"nop", "text2"} '''
   >>> parameter_change(txt,newdict)
   u'1) c\xc3o 2) name1 3) text2 '

.. sage output   Examples: 1) -12.1234560000000  2) \left(-34.3200000000000\right) 3) -12.1 4) -34.32
.. python output Examples: 1) -12.123456  2) \left(-34.32\right) 3) -12.1 4) -34.32



IMPLEMENTATION NOTES:

1. If this module is modified to a pure Python module then:
   a. sage -python -m doctest paramparse.py
   b. In Python the example could return "Examples: 1) -12.123456  2) (-34.32) 3) -12.1 4) R15(-34.32)"


LINKS:

1. See Python MatchObject
2. http://docs.python.org/library/string.html#formatexamples(

FUTURE. Evaluate if any of this forms is really useful::

    name
    @R15(name)
    @round(name,2)
    @(name)
    @["2.3g".format(name)]
    @[t=name1+name2;round(name,2)] ->
    @integrate(f,x) -> (1/2)x^2
    @(name[0],name[1])-> (10.2,23.3)
    @(integrate(f,x),f.diff(x)) -> ((1/2)x^2,1)


"""

#Python package
import re



def parameter_change(inputtext,datadict):match: " + match.groups())

        try:
            if match.group(1) is not None:
                #Case name@()
                #Get data from dict for this match
                keyname = match.group(1)
                data_value = datadict[keyname]
                if data_value<0:
                    outputtext += inputtext[text_last:match.start()+1] + ur'\left(' + ulatex(data_value) + ur'\right)'
                else:
                    outputtext += inputtext[text_last:matparameter_change(inputtext,datadict):
    """
    Substitution on a given input text with names acting as placeholders by their values on a provided dict.

    INPUT:
    - ``inputtext``-- text containing an exercise template with named placeholders.
    - ``datadict`` -- a dictionary with the names that will be changed by values.

    OUTPUT:
        Text where names where replaced by values.

    See examples at top of the file.
    Implementation details below.
    """

    #Create regex using datadict names
    keys_no_keyword = [ v for v in datadict.keys() if v[0]!='_' and v!='self'] 
      #this revered sort guarantees that 'onb1' is first changed and only then 'onb'.
      #Otherwise, if key onb1 appear,  "onb" will be first replaced leaving '1' in the text.
    keys_no_keyword.sort(reverse=True) 
    c_dict_keys = "|".join( keys_no_keyword ) #see use below.

    """
    RegEX definition:

    Consider this examples:   ``"1) name  2) name2@() 3) name@f{2.3g} 4) name2@s{R15} 5) name3@["text0","text1"] "``. 
    Fields in the regex are for the example are separed in this way:

    * Groups in example 1): (None, None, None, None, None, None, None, 'name')
    * Groups in example 2): ('name2', None, None, None, None, None, None, None)
    * Groups in example 3): (None, 'name', '2.3g', None, None, None, None, None)
    * Groups in example 4): (None, None, None, 'name2', 'R15', None, None, None)
    * Groups in example 5): (None, None, None, 'name2', None, 'name3', '["text0","text1"]', None)

    Detailed description:
    * g0: is the full match
    * g1: name of var that needs () if negative value (otherwise None)
    * g2,g3: name using @f and args (otherwise None,None)
    * g4,g5: name using @s and args (otherwise None,None)
    * g6,g7: name and list of possibilities ["text0","text1"].
    * g8: name without format

    NOTES:
    1. dd must be on end
    2. '\W(' + dd + ')' = a key must be preceeded by a non alphanumeric character
    3. Does not work to do: \W(' + dd + ')\W' because in this case two characters are needed for each dd name. User must be warned of this.

    \W: If UNICODE is set, this will match anything other than [0-9_] and characters marked as alphanumeric in the Unicode character properties database.
    \w: If UNICODE is set, this will match the characters [0-9_] plus whatever is classified as alphanumeric in the Unicode character properties database.

    """
    #ReEX definition:
    re_str = r'\W(\w+)@\(\)|'\
             r'\W(\w+)@f\{([\.#bcdeEfFgGnosxX<>=\^+\- 0-9\%]+)\}|'\
             r'\W(\w+)@s\{(\w+)\}|'\
             r'\W(\w+)@c\{([\s",\-\w]+)\}|' + \
             r'\W(' + c_dict_keys + ')'



    #re.MULTILINE|re.DOTALL|re.IGNORECASE|re.|
    match_iter = re.finditer(re_str,inputtext,re.UNICODE)


    #TODO: maybe this should be above.
    if type(inputtext) == str:
        inputtext = unicode(inputtext,'utf-8')

    #Debug
    #import unicodedata
    #print "UNICODE DATA FOR REGEX:----------------"
    #for i, c in enumerate(inputtext):
    #    print i, '%04x' % ord(c), unicodedata.category(c),
    #    print unicodedata.name(c)

    outputtext = u""

    text_last = 0

    for match in match_iter:
        
        
        #if type(inputext) == unicode:
        #    print "Full match group(0) is: " + unicode(match.group(0))
        #    print "Groups(1..n) in this ch.start()+1] +  ulatex(data_value)
            elif match.group(2) is not None and match.group(3) is not None:
                #case name@f{0.2g}
                keyname = match.group(2)
                data_value = datadict[keyname]
                format_text = r"%" + match.group(3)
                formated_argument = format_text % data_value
                outputtext += inputtext[text_last:match.start()+1] + formated_argument
            elif match.group(4) is not None and match.group(5) is not None:
                #case name@s{RealField15}
                keyname = match.group(4)
                data_value = datadict[keyname]
                sage_command = match.group(5) + '(' + str(data_value) +')'
                ev = eval(sage_command,globals())
                outputtext += inputtext[text_last:match.start()+1] + str(ev)
            elif match.group(6) is not None and match.group(7) is not None:
                #case name@c{"text0","text1"}
                try:
                    #create list with user given strings:
                    #name@c{"text0","text1"} --> ["text0","text1"]
                    str_list = eval("["+match.group(7)+"]")
                    #get value of 'name'
                    keyname = match.group(6)
                    data_value = datadict[keyname]
                    #get string from the list
                    str_value = str_list[data_value]

                    #TODO: Check if rmeove this is ok
                    #if str_value in datadict:
                    #    data = datadict[str_value]
                    #    if type(data) == str:
                    #        str_value = unicode(datadict[str_value],'utf-8')
                    #    else:
                    #        str_value = data
                    #else:
                    #    if type(str_value) == str:
                    #        str_value = unicode(str_value,'utf-8')

                except SyntaxError as e:
                    value = keyname
                    print "Syntax problem on %s." % match.group(7)
                except NameError as e:
                    value = keyname
                    print "Use double quotes even on names (case: %s in '%s')." % (e,match.group(7))
                #print type(str_value), " ", str_value
                if type(str_value) == str:
                    str_value = unicode(str_value,'utf-8')
                outputtext += inputtext[text_last:match.start()+1] + str_value
            else: #same as if match.group(5) is not None
                #case name (wihtout formating)
                keyname = match.group(8)
                data_value = datadict[keyname]
                if type(data_value) is str:
                    outputtext += inputtext[text_last:match.start()+1] + data_value
                elif type(data_value) is unicode:
                    outputtext += inputtext[text_last:match.start()+1] + data_value
                else:
                    outputtext += inputtext[text_last:match.start()+1] + ulatex(data_value)
        except KeyError:
                #outputtext += inputtext[text_last:match.start()+1] + unicode(keyname,'utf-8')
                outputtext += inputtext[text_last:match.start()+1] + keyname

        text_last = match.end()            

    outputtext += inputtext[text_last:]


    return outputtext



def ulatex(s):
    return unicode(latex(s),'utf-8')


#==========================================



#Sometimes needed.
x=var('x')


#For 4 digit numbers.
R15=RealField(15)


#Negative numbers in (...)
def showmul(x):
    """Old way of writing parentesis on negative numbers."""
    if x<0:
        return '(' + latex(x) + ')'
    else:
        return x






#==========================================



