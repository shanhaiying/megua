



class MoodleMLExercise(Exercise):

    def __init__(self,ekey=None,edict=None):
        Exercise.__init__(self,ekey,edict)

    def print_cl(self):

        #Use jinja2 template to generate LaTeX.
        self.mchoice_template = self.env.get_template("moodle-mchoice.xml")


        self.latex_string = self.template("PDFLatexExercise_print.tex",self)
        #Produce PDF file from LaTeX.
        pcompile(latex_string, '.', self.owner_key)

    def print_nb(self):
        #Use jinja2 template to generate LaTeX.
        self.latex_string = self.template("PDFLatexExercise_print.tex",self)
        #Produce PDF file from LaTeX.
        pcompile(latex_string, '.', self.owner_key)


    def export(self):
        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.mchoice_template = self.env.get_template("moodle-mchoice.xml")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template moodle_mchoice.xml"
            raise e

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.cloze_template = self.env.get_template("moodle-cloze.xml")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template moodle_cloze.xml"
            raise e

