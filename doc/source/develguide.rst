
.. Global status of Meg:
.. * local archive is in use and improvement.
.. * global archive has some experiments but is not the primary goal now.
.. TARGET ? http://www.sagemath.org/packages/experimental/



.. _developerguide:


Developer Guide
===============

This section contains memory notes for the MEGUA authors and also for new developers who want to contribute to or change MEGUA code. 

Section :ref:`userguide` contains an initial description of MEGUA and on 
Sage tutorial `Writing Code for Sage`_ one can find the standards of programing for Sage.

.. _Writing Code for Sage: http://www.sagemath.org/doc/developer/writing_code.html

.. You can improve Meg by solving issues (improvements and defects) listed here_.

.. here http://code.google.com/p/meg/issues/list


Workflow
--------

MEGUA uses Mercurial_ versioning system. To get MEGUA you can create a clone of it some folder (ex. /home/user1/)::
  
   $ hg clone https://megua.googlecode.com/hg/ megua  

.. _Mercurial: http://mercurial.selenic.com/

A possible procedure to get MEGUA knowable by Sage Math is doing the following. 
Consider that Sage packages are instaled at::

   /opt/sage/local/lib/python2.6/site-packages/

inside of it do (0.2 is current version)::

   $ ln -s /home/user1/megua-0.1/megua/

that produces a symbolic link::

 /opt/sage/local/lib/python2.6/site-packages/megua/

and to confirm do::

   sage: from megua.all import *


Packages on SAGE
----------------

Put lines like these on .bashrc::

   export PATH=/home/user1/sage/bin/:$PATH:/home/jpedro/all/ubuntu/bin/
   export SAGE_ROOT=/home/user1/sage
   export SAGE_LOCAL=/home/user1/sage/local
   export LD_LIBRARY_PATH=/home/user1/sage/local/lib
   export DYLD_LIBRARY_PATH=/home/user1/sage/local/lib

To create a package do, above directory  ``megua-0.1``::

   $ sage -pkg megua-0.1 #create
   $ sudo sage -f megua-0.1.spkg  #install

To download and install a package::

    sage -i package_name

To look inside a package::

    tar -jxvf mypackage-version.spkg

Managing packages inside Sage:

* http://www.sagemath.org/doc/reference/sage/misc/package.html

Sources:

* http://www.sagemath.org/doc/developer/producing_spkgs.html
* http://www.sagemath.org/download-packages.html



Mercurial versioning system
----------------------------

Versioning server: https://code.google.com/p/meg/

Clone::

   hg clone https://meg.googlecode.com/hg/ meg  

Commit::

   hg ci -m"Some description of changes"


Push changes:

   hg push https://meg.googlecode.com/hg/ 




Documenting
-----------

MEGUA is documented using `Sphinx`_ system based on markup syntax `Restructuredtext`_.

.. _Restructuredtext:   http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _Sphinx: http://sphinx.pocoo.org/index.html

The following steps have been done to be able to use `automodules`_:

 - Start a new documentation tree using this `tutorial`_.

 - For automodules to work with Sage (it seems that) is needed to change variable ``SPHINXBUILD`` in Makefile to::

      SPHINXBUILD   = /home/jpedro/sage/sage -python /usr/bin/sphinx-build

 - In documentation folder there exists ``conf.py``. Then

   * add this lines::
 
      \# If extensions (or modules to document with autodoc) are in another directory,
      \# add these directories to sys.path here. If the directory is relative to the
      \# documentation root, use os.path.abspath to make it absolute, like shown here.
      sys.path.append(os.path.abspath('/home/user1/megua/megua-0.1/megua/'))

   * and this::

      \# Add any Sphinx extension module names here, as strings. They can be extensions
      \# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
      extensions = ['sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.pngmath', 'sphinx.ext.graphviz']

 - Command ``make html`` will produce ``_build`` tree with html.


.. _tutorial: http://sphinx.pocoo.org/tutorial.html
.. _automodules: http://sphinx.pocoo.org/tutorial.html#autodoc



Just for reference (but not used in MEGUA) there is a page about Sage manuals_.

.. _manuals: http://www.sagemath.org/doc/developer/sage_manuals.html#building-the-manuals

To publish documentation in `Read The Docs`_ create an hook on ``.hg/hgrc`` file like explained in here_.

.. _`Read The Docs`: http://megua.ReadTheDocs.org
.. _hook: http://mercurial.selenic.com/wiki/Hook
..http://stackoverflow.com/questions/3120503/how-to-make-mercurial-run-script-on-push



Testing
-------

The following commands can be used for testing Sage examples in documentation strings::

   sage -t -verbose exerparse.py
   sage -t exerparse.py

Modules in 'pure' python, ie. using ">>>" for examples, are tested with::

   python -m doctest -v example.py



Unicode utf8
------------

MEGUA is intended to be used with several languages.

For exameplo, to use portuguese one must use this on a vim file::

   # vim:fileencoding=iso-8859-15
   # -*- coding: iso-8859-15 -*-

where the first line informs vim about the character set and second line informs python.
More details here_.

.. _here: http://www.python.org/peps/pep-0263.ht

.. #ISO-8859-1 (also called “latin-1”),
.. #http://diveintopython.org/xml_processing/unicode.html
.. # http://docs.python.org/howto/unicode.html
.. VIM
.. http://vim.wikia.com/wiki/Working_with_Unicode


