
class Exercise:

    def ....

    def create_instance(self, ekey, edict):

        exinstance_class = eval(self.exinstance_class)

        exinstance = exinstance_class( \
            ownerkey = self.ownerkey, \
            summtext = self.summary(), \
            ...
        )

class ExerciseInstance:

    def __init__(self), ownerkey, summtext, probtext, anstext, ekey, edict):

        self
        self.summtext = ex_model.summary()

    def summary(self, mode):
        """Return a string"""
        if mode=='utf-8':
            return 
        else:
            return

        print '-'*len(sname)
                print summtxt.encode('utf8')
                print probtxt.encode('utf8')
                print answtxt.encode('utf8')


    def print(self):
        #print like sage/python print
        # etc
        chama a função self._latex

    def _latex(self, options=[sum,prob,answe)    



class PDFLatexExercise(ExerciseInstance):


     def __init__(self), ownerkey, summtext, probtext, anstext, ekey, edict):

        self
        self.summtext = ex_model.summary()

    def print(self):
        # print like sage/python print
        # etc
        chama a função self._latex

    def _latex(self, options=[sum,prob,answe)    




class C3WebExercise(ExerciseInstance):


    def _publish_tikz(self,sname,html_str):
        """ 
        Receives a string with latex tikz begin{}...end{} environments. Extracts and produce pdf and png file for each tikz graphic.
        """

        #important \\ and \{
        #
        tikz_pattern = re.compile(r'\\begin\{tikzpicture\}(.+)\\end\{tikzpicture\}', re.DOTALL|re.UNICODE)

        #Cycle through existent tikz code and produce pdf and png files.


   def um render via template

 ex_instance = exerciseinstance(row, ekey= ekey + e_number)


            #Print problem
            #Template fields:
            # {{ extitle }} Ex. Q.1
            # {{ exsmall }} Ex. L.1

            problem_html = self.problem_template.render(
                extitle = "Ex. %s. %d" % (whatinside,exnr),
                exsmall = "Ex. %s. %d" % (whatinside,exnr),
                problem = ex_instance.problem()
            )

            #ofile = open( os.path.join( self.c3web_folder, "e%02d-%02d-P%02d.aspx" % (sec_number+1,e_number+1,ekey+1) ), 'w')
            ofile = open( os.path.join( where, "%s%d.aspx" % (ename,exnr) ), 'w')
            ofile.write(problem_html.encode('latin1'))
            ofile.close()

            #Print problem and answer
            problemanswer_html = self.problemanswer_template.render(
                extitle = "Res. %s. %d" % (whatinside,exnr),
                exsmall = "Res. %s. %d" % (whatinside,exnr),
                problem = ex_instance.problem(),
                answer = ex_instance.answer()
            )

	    #ofile = open( os.path.join( self.c3web_folder, "e%02d-%02d-A%02d.aspx" % (sec_number+1,e_number+1,ekey+1) ), 'w')
            ofile = open( os.path.join(where, "%s%d.aspx"  % (rname,exnr) ), 'w')
            ofile.write(problemanswer_html.encode('latin1'))
            ofile.close()  
