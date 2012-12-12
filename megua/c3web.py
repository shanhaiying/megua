
    def c3web(self, exname, many=10, fn="3", ekey=0, edict={}, where='c3web'):
        """
        Save an exercse to aspx page.

	INPUT:
	- exname: string with exercise identification name.
	- many: how many samples (starting ekey generated key).
	- fn: "2", "3", whatever that preceeds filenames.
	- ekey: random values generation key.
	- editc: some values declared on make_random or solve functions of the exercise.

        NOTES:
          Use
            self.ofile = codecs.open( os.path.join( self.c3web_folder, "e%02d.rst" % (sec_number+1) ),encoding='utf-8', mode='w+')
          if utf8 is needed.
        """

        #If does not exist create
        if not os.path.exists(where):
            os.makedirs(where)


        #Create exercise instance
        row = self.megbook_store.get_classrow(exname) 

        for e_number in range(many):

            #Continuous numeration of exercises
            exnr = ekey + e_number

            #Create exercise instance
            ex_instance = exerciseinstance(row, ekey=exnr)


            #Print problem
            #Template fields:
            # {{ extitle }} Ex. Q.1
            # {{ exsmall }} Ex. L.1

            problem_html = self.problem_template.render(
                extitle = "Ex. L. %d" % exnr,
                exsmall = "Ex. L. %d" % exnr,
                problem = ex_instance.problem()
            )

            #ofile = open( os.path.join( self.c3web_folder, "e%02d-%02d-P%02d.aspx" % (sec_number+1,e_number+1,ekey+1) ), 'w')
            ofile = open( os.path.join( where, "P_%s_%03d.aspx" % (exname,exnr) ), 'w')
            ofile.write(problem_html.encode('latin1'))
            ofile.close()

            #Print problem and answer
            problemanswer_html = self.problemanswer_template.render(
                extitle = "Res. L. %d" % exnr,
                exsmall = "Res. L. %d" % exnr,
                problem = ex_instance.problem(),
                answer = ex_instance.answer()
            )

	    #ofile = open( os.path.join( self.c3web_folder, "e%02d-%02d-A%02d.aspx" % (sec_number+1,e_number+1,ekey+1) ), 'w')
            ofile = open( os.path.join(where, "R_%s_%03d.aspx"  % (exname,exnr) ), 'w')
            ofile.write(problemanswer_html.encode('latin1'))
            ofile.close()


        #fnull = open(os.devnull,'w')
        import subprocess
        #subprocess.check_call([ "zip", self.c3web_folder, self.c3web_folder],stdout=fnull,stderr=fnull)
        subprocess.call("zip %s %s" % (where, where+r'/*'), shell=True)
ttp://stackoverflow.com/questions/699325/suppress-output-in-python-calls-to-executables
        #fnull = open(os.devnull,'w')
        import subprocess
        #subprocess.check_call([ "zip", self.c3web_folder, self.c3web_folder],stdout=fnull,stderr=fnull)
        subprocess.call("zip %s %s" % (self.c3web_folder, self.c3web_folder+r'/*'), shell=True)
        #fnull.close()

        #fnull.close()


