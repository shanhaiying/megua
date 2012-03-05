
.. _userguide:

User Guide
==========

MEGUA is originally an acronym of 'Mathematics Exercise Generator'. It is a package to use in |sagemath|_ for create and edit a personal
database of LaTeX_ exercise templates. The package is ready for command line use or notebook use. 
    
Meg operations are:

1. Open one or more databases.
2. Produce, edit and delete exercises.
3. Produce a configurable PDF from list of exercises.
4. Search for one or a group of exercises.
5. Generate exercises based on existing templates with random entries or giving some entries.


Meg uses |sagemath|_ as support for mathematics. A very introductory programming skills are needed (|sagemath|_ uses Python_ language 
with very little pre parsing). Currently Meg uses LaTeX_ and you have here_ a collection of introductory level tutorials.

One can use the command-line of |sagemath|_ (Linux environment) or the front-end, usually in a server.

.. |sagemath| replace:: *Sage math*
.. _sagemath: http://www.sagemath.org
.. _Python: http://www.python.org
.. _LaTeX: http://www.tug.org
.. _here: http://www.tug.org/begin.html

The following is an exercise template:


.. code-block:: latex

   %Summary
   Here one can write few words, keywords about the exercise.
   For example, the subject, MSC code, and so on.

   %Problem
   What is the primitive of $a x + b@()$ ?

   %Answer
   The answer is $prim+C$, for $C in \mathbb{R}$.


.. code-block:: python

   class E28E28_pdirect_001(Exercise):

       def make_random(self):

           self.a = ZZ.random_element(-4,4)
           self.b = QQ.random_element(-4,4)

       def solve(self):

           x=var('x')
           self.prim = integrate(self.a * x + self.b,x)

and that's all. This exercise has a LaTeX_ part and a Python_ (with |sagemath|_ pre parse) part.

The LaTeX part has 3 sections marked by respective tags:

Tag **%Summary**

    Here one can write few words, keywords about the exercise.
    For example, the subject, MSC code, and so on. Or inline latex $equations$.

    Text in this field can help searching for a specific exercise. 
    This part is usually hidden from a student to whom this exercise is presented.


Tag **%Problem** and tag **%Answer**

    In the problem and answer place, one poses the problem and in separate the answer. 
    The text may contain placeholders or 'Meg variables'. Meg variables 
    are a mix of letters or letters and numbers and it will be replaced by some LaTeX_ expression (formula, numbers, etc.). 
    In the above example, `a` and `b@()` are the Meg variables (the second has a decorator @()). 


How it works? 

1. Put the Meg variable where you want to appear a number, a value or math expression; The example ``$a x + b@()$`` has two variables.
2. In the *make_random* function one give a 'Sage value or expression' to the Meg variable.  In the example, ``self.a = ZZ.random_element()`` a random integer value is given to ``a``.
3. When a new exercise instance is produced the Sage value is converted to the LaTeX representation.


.. _megvariables:

Meg Variables
-------------

Variables can be **decorated** as the following examples show:

1. If v=exp(1) in |sagemath|_ then $v$ will be replaced by $e$. 
2. If v=-10, a negative number, then ``$v@()$`` will be replaced by ``$(-10)$``, i.e., with parenthesis around it.
3. A precision notation, like C *printf*, can be used on numbers:  ``$v@f{0.4g}$`` prints the number with 4 decimal places.
4. And ``$v@s{sin}$`` calls function sin on ``v: sin(v)``.
    


Use from Sage notebook
-----------------------

A first cell in the worksheet should define the database and the ``meg`` object::
   #auto
   from meg.all import *
   meg = MegBook(r'/home/user/a_meg_base.sqlite')

In the example above, the database file will be available only in the current worksheet. This is caused by a restriction 
on DATA (Sage notebook variable). This should be improved for the database to be available to every worksheet from the same user.

Another possibility is using some folder where an user as permissions to write like ``/home/paula/paula.sqlite``, for example, if one is using 
Sage notebook in the local host.

**Workflow**

If the objective is to create a database of exercises then a one possible of work flow is:

1. Create an exercise in each worksheet. In the same worksheet execute a command to save the exercise to the database.
2. After all verifications on the exercise one can store a copy on the local disk (as sws file) and archive it on the notebook. 
3. Recall the exercise by searching the database (using exercise name or by words).

If the objective is to build only few exercises then it is using the same worksheet is a good solution. 

**Create and editing a template**



In a new cell of an opened worksheet do, as in the example:

.. code-block:: python

   #START of the cell  ------------------
   
   txt = r'''

   %Summary
   Here one can write few words, keywords about the exercise.
   For example, the subject, MSC code, and so on.

   %Problem
   What is the primitive of $a x + b@()$ ?

   %Answer
   The answer is $prim+C$, for $C in \mathbb{R}$.

   class E28E28_pdirect_001(Exercise):

       def make_random(self):

           self.a = ZZ.random_element(-4,4)
           self.b = QQ.random_element(-4,4)

       def solve(self):

           x=var('x')
           self.prim = integrate(self.a * x + self.b,x)

    '''

    meg.save_string(txt)
    e = meg.new("E28E28_pdirect_001",ekey=2)

    #END of the cell ------------------


Previously we address the content of the template of the exercise.
Now we describe how to use it:

1. Notice the ``txt = '''`` in the top of the cell. We are defining a textual string containing all information. The string starts with ``'''`` and ends with the same ``'''``. The string will contain LaTeX and Python_ coding for the exercise.
2. The exercise must have a name. The recommended pattern for names is: letter ``E``, a possible MSC code, a name and a number, all joined by an ``_`` underscore.
3. Now, the command ``meg.save_string(txt)`` will save the exercise to the database.
4. After it stores the exercise in the database one can produce an example to check if everything is ok. This is command ``e = meg.new("E28E28_pdirect_001",ekey=2)``

**Notes:**

* the keyword ``self`` can be replaced by a single letter identifier ``s`` but there is no way, in a class definition, to avoid it complytely.


meg.search("E26A36")







Use from Text files
-------------------


Developing a new exercise:

1. Edit a new file, named for example, "E28E28_pdirect_001.sage" and use this sintax:

.. code-block:: python    

   txt = '''
      exercise TeX and Sage/Python definition (see above E28E28_pdirect_001)

   ''' 
   from meg.all import *
   meg = MegBook(r'/home/user/a_meg_base.sqlite')
   meg.save_string(txt)
   meg.new("E28E28_pdirect_001", ekey=10)


2. At shell prompt do::

   sage E28E28_pdirect_001.sage

3. Check E28E28_pdirect_001.tex and E28E28_pdirect_001.pdf files.

 




Creating books
--------------

The title word "books" could be a little ostentatious! Maybe booklets, book of exercises, exercise sheets, and so on.

One can join several exercises (template or instances) on a PDF. We need two templates: the 'row' template for each exercise --
what are the columns we want to appear in PDF, and the 'book' template -- what packages, LaTeX style, sections and exercise we want to
show.

In what follows, note that ``"""`` mark the beginning and end of the string in Python_. In the first example:


.. code-block:: python    

   #Full information from an exercise template

   all_details = """\\textbf{Name:}~\\verb+{{ exname }}+ \
   \n\n \\textbf{Summary} \n\n {{ summary }} \
   \n\n \\textbf{Problem template} \n\n {{ problemtemplate }} \
   \n\n \\textbf{Answer template} \n\n {{ answertemplate }} \
   \n\n \\begin{verbatim}\n{{ codetxt }}\n\\end{verbatim} \
   \n\n \\textbf{Problem Example } \n\n {{ problem }} \
   \n\n \\textbf{Answer Example } \n\n {{ answer }} \
   \n\n"""

we see the keyword names of every information that is stored about an exercise:

``exname``
   The given name to the exercise. Example ``E62L20_stochastic_001``.

``summary``
   The textual summary

``problemtemplate``
   The original problem text (template) without substitutions.

``answertemplate``
   The original answer text (template) without substitutions.

``problem``
   One sample of problem text with variables replace by proper values according to *make_random* function.

``answer``
   The related answer text with variables replace by proper values according to *solve* function.


Then we must define what the book look like using another template:

.. code-block:: latex

   #
   # Exemplo de ficheiro latex a ser usado como molde.
   #

   book_template = r"""
   \documentclass{article}
   \usepackage[utf8]{inputenc}
   \begin{document}

   {{ put_here("E26B05_DPpolinomio_001") }}

   {{ put_here("E26B05_DPexponencial_001") }}

   {{ put_here("E26B05_DPpotencia_001") }}

   {{ put_here("E26B05_DPlogaritmo_001") }}   

   {{ put_here("E26B05_DPracional_001") }}

   \end{document}
   """

Now we create the book using the string ``all_details`` that indicates what we want to show from each exercise and the string template 
``book_template``:


.. code-block:: python

   # Producing a book
   meg.template_fromstring(book_template,rowtemplate=all_details)


Another configurations
^^^^^^^^^^^^^^^^^^^^^^

Short configuration:

.. code-block:: python

   #Configuração curta: mostra apenas problem e answer

   modelo_curto = """\
   \n\n \\textbf{Problem Example } \n\n {{ problem }} \
   \n\n \\textbf{Answer Example } \n\n {{ answer }} \
   \n\n"""


With LaTeX package "exercise":


.. code-block:: latex

   # 
   # Using \usepackage{exercise}
   #

   model_exercicelist= """\
   \n\n \\Exercise \n {{ problem }} \
   \n\n \\Answer \n {{ answer }} \
   \n\n"""
   #proper for exercises at start and answers at the end.

   #
   # main latex file
   #

   file_exercicelist = r"""
   \documentclass{article}

   \usepackage[utf8]{inputenc}

   \usepackage{amsfonts}

   % ================
   % Exercise Package
   % ================
   \usepackage[lastexercise,answerdelayed]{exercise}
   \renewcommand{\AnswerListHeader}{\textbf{Resposta do ex.~\ExerciseHeaderNB\ ---\ }}
   \renewcommand{\theExercise}{\arabic{section}.\arabic{Exercise}} %texto da numeracao de cada exercicio
   \renewcounter{Exercise}[section] %permite re-iniciar Exercise=1 a cada chapter.

   \begin{document}

   %Isto é um teste.

   \section{Problemas}

   \begin{ExerciseList}

   {{ put_here("E26A36_PImediatas_001") }}

   {{ put_here("E26A36_PElementosSimples_001") }}

   {{ put_here("E26A36_PRacionais_001") }}

   \end{ExerciseList}


   \section{Soluções}

   \shipoutAnswer


   \end{document}
   """

   #
   #comando que gera o pdf e tex usando os moldes acima.
   #

   meg.template_fromstring(ficha_exercicelist,rowtemplate=modelo_exercicelist)



