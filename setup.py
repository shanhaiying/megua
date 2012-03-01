"""Distutils based setup script for Biopython.

This uses Distutils (http://python.org/sigs/distutils-sig/) the standard
python mechanism for installing packages. For the easiest installation
just type the command:

python setup.py install

"""

from distutils.core import setup



setup(name='meg',
      version='0.2.2',
      description='Meg Learning Objects',
      author='Pedro Cruz',
      author_email='pedrocruz@ua.pt',
      url='https://code.google.com/p/meg/',
      packages=['meg','pdfminer'],
      package_dir={'meg': 'meg', 'pdfminer': 'meg/src/pdfminer'},
      package_data={'meg': ['template/pt_pt/*']},
)


