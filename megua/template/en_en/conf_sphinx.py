# -*- coding: utf-8 -*-

#See more details at http://sphinx.pocoo.org/config.html

language = '{{ language }}'

import sys, os
extensions = ['sphinx.ext.pngmath']
#templates_path = ['build/_templates']
#html_static_path = ['build/html/_static']
source_suffix = '.rst'

#source_encoding = 'utf-8-sig'
master_doc = 'index'

# General information about the project.
project = u'MEGUA'
copyright = u'MEGUA is a registered mark of University of Aveiro (2012)'
version = '0'
release = '0'
today_fmt = '%Y-%B-%d'

exclude_patterns = []
pygments_style = 'sphinx'

# HTML builder
html_theme_path = ['/usr/share/sphinx/themes', '{{ megua_theme_dir }}' ]
html_theme = 'default2'
#html_theme_options = {
#    "rightsidebar": True
#    "sidebarwidth": 330
#}

html_title = '{{ local_store_filename }}'
html_short_title = '{{ local_store_filename }}'

html_use_index = True


