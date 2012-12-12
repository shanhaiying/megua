"""Distutils based setup script for Biopython.

This uses Distutils (http://python.org/sigs/distutils-sig/) the standard
python mechanism for installing packages. For the easiest installation
just type the command:

python setup.py install

"""

from distutils.core import setup



setup(name='megua',
      version='0.2',
      description='MEGUA: build your database of parameterized exercises.',
      author='Pedro Cruz',
      author_email='pedrocruz@ua.pt',
      url='https://code.google.com/p/megua/',
      packages=['megua'],
      #package_dir={'megua': 'megua', 'pdfminer': 'src/pdfminer'},
      package_data={'megua': ['template/pt_pt/*']},
      requires=[ #it seems this does nothing!!
        'pdfminer'
      ]
)



