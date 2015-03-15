**MEGUA** is a package for [Sage Math](http://www.sagemath.org).

It allows an author to create databases of parameterized exercises characterized by a **summary**, a **problem** and a detailed **answer** of the exercise, all fields in latex typeset. Exercises are parameterized with variables names that are replaced by values using the Python language in the framework of Sage Mathematics.

After choosing a set of questions from a database one can print them to create a small textual study book or a paper exam (with or without resolution).



## Current state ##

MEGUA is being developed by a team at University of Aveiro (Portugal) and project home page is (only) a **Portuguese homepage**: [MEGUA](http://cms.ua.pt/megua).

We appreciate colaboration in the project so feel free to contact [Pedro Cruz](http://www.mat.ua.pt/PagePerson.aspx?id=1183&b=1) meguaquestion@gmail.com

Tutorial is only in portuguese in
[here](https://dl.dropboxusercontent.com/u/10518224/megua/index.html).

### Install ###

Current version is in the "running" branch so this set of instructions should set it up:

```
$ hg clone https://code.google.com/p/megua/
$ cd megua
$ hg update running
$ pwd
<some directory>/megua
$ cd ~/sage-6.1.1/local/lib/python2.7/site-packages
$ ln -s <some directory>/megua/megua      #--- twice "megua".
```

and it should run.



### Install (old) ###

First, install pdfminer:

1. download from here http://pypi.python.org/pypi/pdfminer/;
2. unzip it;
3. enter pdfminer directory;
4. sage -python setup.py install

Then, download megua-0.2.spkg and, at linux console, do:

$ sage -i megua-0.2.spkg

Consult MEGUA user guide [here](http://megua.readthedocs.org).

### License ###

MEGUA is an "GPL v2" package for Sage Math.

Name "[MEGUA](http://cms.ua.pt/megua)" is registered to [University of Aveiro](http://www.ua.pt) (Portugal) in 2012.