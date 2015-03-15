

*MEGUA* is a package for [http://www.sagemath.org Sage Math].
 
It allows an author to create databases of parameterized exercises characterized by a *summary*, a *problem* and a detailed *answer* of the exercise, all fields in latex typeset. Exercises are parameterized with variables names that are replaced by values using the Python language in the framework of Sage Mathematics.

After choosing a set of questions from a database one can print them to create a small textual study book or a paper exam (with or without resolution).



== Current state ==

MEGUA is being developed by a team at University of Aveiro (Portugal) and project home page is (only) a *Portuguese homepage*: [http://cms.ua.pt/megua MEGUA]. 

We appreciate colaboration in the project so feel free to contact [http://www.mat.ua.pt/PagePerson.aspx?id=1183&b=1 Pedro Cruz] meguaquestion@gmail.com

Tutorial is only in portuguese in 
[https://dl.dropboxusercontent.com/u/10518224/megua/index.html here].

===Install===

Current version is in the "running" branch so this set of instructions should set it up:

{{{
$ hg clone https://code.google.com/p/megua/
$ cd megua
$ hg update running
$ pwd
<some directory>/megua
$ cd ~/sage-6.1.1/local/lib/python2.7/site-packages
$ ln -s <some directory>/megua/megua      #--- twice "megua".
}}}

and it should run.



===Install (old)===

First, install pdfminer:

1. download from here http://pypi.python.org/pypi/pdfminer/;
2. unzip it;
3. enter pdfminer directory;
4. sage -python setup.py install

Then, download megua-0.2.spkg and, at linux console, do:

$ sage -i megua-0.2.spkg 

Consult MEGUA user guide [http://megua.readthedocs.org here].

===License===

MEGUA is an "GPL v2" package for Sage Math. 

Name "[http://cms.ua.pt/megua MEGUA]" is registered to [http://www.ua.pt University of Aveiro] (Portugal) in 2012.
