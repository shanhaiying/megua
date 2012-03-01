
.. Global status of Meg:
.. * local archive is in use and improvement.
.. * global archive has some experiments but is not the primary goal now.
.. TARGET ? http://www.sagemath.org/packages/experimental/



.. _developerguide:


Developer Guide
===============

This section is for developers who want to contribute to Meg code. 
Section :ref:`userguide` contains an initial description of Meg and on 
Sage tutorial `Writing Code for Sage`_ one can find the standards of programing for Sage.


.. _Writing Code for Sage: http://www.sagemath.org/doc/developer/writing_code.html

You can improve Meg by solving issues (improvements and defects) listed here_.

.. _here: http://code.google.com/p/meg/issues/list


Workflow
--------

Meg uses Mercurial_ versioning system. To get Meg you can create a clone of it some folder (ex. /home/user1/)::
  
   $ hg clone https://meg.googlecode.com/hg/ meg  

.. _Mercurial: http://mercurial.selenic.com/

A possible procedure to get Meg knowable by Sage is doing the following. 
Consider that Sage packages are instaled at::

   /opt/sage/local/lib/python2.6/site-packages/

inside of it do (0.2 is current version)::

   $ ln -s /home/user1/meg-0.2/meg/

that produces a symbolic link::

 /opt/sage/local/lib/python2.6/site-packages/meg/

and to confirm do::

   sage: from meg import all

Now you can edit ``meg/*.py`` files and check changes using Sage.


Packages on SAGE
----------------

Put lines like these on .bashrc::

   export PATH=/home/user1/sage/bin/:$PATH:/home/jpedro/all/ubuntu/bin/
   export SAGE_ROOT=/home/user1/sage
   export SAGE_LOCAL=/home/user1/sage/local
   export LD_LIBRARY_PATH=/home/user1/sage/local/lib
   export DYLD_LIBRARY_PATH=/home/user1/sage/local/lib

To create a package do, above directory  ``meg-0.2``::

   $ sage -pkg meg-0.2
   $ sudo sage -f meg-0.2.spkg 

To download and install a package
    sage -i package_name

To look inside a package:
    tar -jxvf mypackage-version.spkg

Managing packages inside Sage:

* http://www.sagemath.org/doc/reference/sage/misc/package.html

Sources:

* http://www.sagemath.org/doc/developer/producing_spkgs.html
* http://www.sagemath.org/download-packages.html



Mercurial versioning system
----------------------------

Versioning server: https://code.google.com/p/meg/

Clone:

   hg clone https://meg.googlecode.com/hg/ meg  


Push changes:

   hg push https://meg.googlecode.com/hg/ 



Produce documentation for Meg
-----------------------------

Guided markup here: `restructuredtext`_ and `sphinx`_.

.. _restructuredtext:   http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _sphinx: http://sphinx.pocoo.org/index.html

See the `Python home page`_ for info.

.. _Python home page: http://www.python.org

Using automodule for building reference manuals: 

http://www.sagemath.org/doc/developer/sage_manuals.html#building-the-manuals

http://sphinx.pocoo.org/tutorial.html#running-the-build

In documentation folder there exists ``conf.py``

1. Add this lines::

   \# If extensions (or modules to document with autodoc) are in another directory,
   \# add these directories to sys.path here. If the directory is relative to the
   \# documentation root, use os.path.abspath to make it absolute, like shown here.
   sys.path.append(os.path.abspath('/home/jpedro/all/meg/meg-0.2/meg/'))

2. and this::

   \# Add any Sphinx extension module names here, as strings. They can be extensions
   \# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
   extensions = ['sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.pngmath', 'sphinx.ext.graphviz']



Testing
-------

The following commands can be used for testing examples in documentation strings::

   sage -t -verbose exerparse.py
   sage -t exerparse.py

If modules are pure python using ">>>" for examples:

python -m doctest -v example.py


Unicode utf8
------------

To use portuguese one must use this on a vim file::

   # vim:fileencoding=iso-8859-15
   # -*- coding: iso-8859-15 -*-

where the first line informs vim about the character set and second line informs python.
 More details here_.

.. _here: http://www.python.org/peps/pep-0263.ht

#ISO-8859-1 (also called “latin-1”),
#http://diveintopython.org/xml_processing/unicode.html
# http://docs.python.org/howto/unicode.html

VIM
http://vim.wikia.com/wiki/Working_with_Unicode









