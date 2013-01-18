

class PDFLatexExercise(Exercise):

    def __init__(self,ekey=None,edict=None):
        Exercise.__init__(self,ekey,edict)

    def print_cl(self)
        #Use jinja2 template to generate LaTeX.
        self.latex_string = self.template("PDFLatexExercise_print.tex",self)
        #Produce PDF file from LaTeX.
        pcompile(latex_string, '.', self.owner_key)

    def print_nb(self):
        #Use jinja2 template to generate LaTeX.
        self.latex_string = self.template("PDFLatexExercise_print.tex",self)
        #Produce PDF file from LaTeX.
        pcompile(latex_string, '.', self.owner_key)


class C3WebExercise(Exercise):





