r"""
MegEnv module. In this module the class ``MegEnv`` and the global object ``megenv`` are defined. 

Templates are part of all megua code so this class template joins together in one place several 
needs of templates.

This templates are used to comunicate with the user (not to produce exercises).

Language: templates to comunicate with user depend on the user language. The template folder 
depends on this language.

AUTHORS:

- Pedro Cruz (2013-02-06): initial version
"""



class MegEnv:

    def __init__(self,natlang='pt_pt'):
        """Templating with Jinja2"""
        self.setlang(natlang)


    def setlang(self,natlang):

        if os.environ.has_key('MEGUA_TEMPLATE_PATH'):
            TEMPLATE_PATH = os.environ['MEGUA_TEMPLATE_PATH']
        else:
            from pkg_resources import resource_filename
            TEMPLATE_PATH = os.path.join(resource_filename(__name__,''),'template',natlang)

        print "Templates for '%s' language: %s" % (natlang,TEMPLATE_PATH)
        #print "Templates in: " + TEMPLATE_PATH

        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH))
        


    def template(self, filename, **user_context):
        """
        Returns HTML, CSS, LaTeX, etc., for a template file rendered in the given
        context.

        INPUT:

        - ``filename`` - a string; the filename of the template relative
          to ``sagenb/data/templates``

        - ``user_context`` - a dictionary; the context in which to evaluate
          the file's template variables

        OUTPUT:

        - a string - the rendered HTML, CSS, etc.

        BASED ON:

           /home/.../sage/devel/sagenb/sagenb/notebook/tempate.py

        """

        try:
            tmpl = self._env.get_template(filename)
        except jinja2.exceptions.TemplateNotFound:
            return "megenv.py -- missing template %s"%filename
        r = tmpl.render(**user_context)
        return r


megenv = MegEnv()


