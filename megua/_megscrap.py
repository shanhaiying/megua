

from class MegBook


    def save_filename(self,exfilename):
        r"""
        Save an exercise defined on textual file using a specific sintax defined here_.
    
        This function is designed when working with Meg on Sage command-line.
    
       INPUT:
        - ``exfilename`` -- a text filename containing a summary, problem, answer and class according to meg exercise sintax for files (see here_).
        OUTPUT:
        - 
    
        .. _python string: http://docs.python.org/release/2.6.7/tutorial/introduction.html#strings
    
        """
        f = open(exfilename,'r')
        exercisestr = f.read()
        f.close()
        return self.megbook_store.save_fromstring(exercisestr)


    def template_frommeg(self,templatename,outfile,ekey,exclasslist):
        """
        References:
        
        From http://jinja.pocoo.org/docs/api/?highlight=unicode

            dump(fp, encoding=None, errors='strict')

            Dump the complete stream into a file or file-like object. Per default unicode strings are written, 
            if you want to encode before writing specifiy an encoding.

        From ~/sage/devel/sage/sage/misc/latex.py

            s: from sage.misc.latex import _run_latex_, _latex_file_
            s: file = os.path.join(SAGE_TMP, "temp.tex")
            s: O = open(file, 'w')
            s: O.write(_latex_file_([ZZ[x], RR])); O.close()
            s: _run_latex_(file) # random - depends on whether latex is installed
            'dvi'
        """
        #Create numbered exercise list
        ex_list = []
        for i,v in enumerate(exclasslist):
            e = self.instance_fromstring(v, ekey=ekey+i)
            sumtxt = unicode(e.summary(), 'utf-8')
            protxt = unicode(e.problem(), 'utf-8')
            anstxt = unicode(e.answer(),  'utf-8')
            newdict = dict({
                'number': i+1, 
                'summary': sumtxt, 
                'problem': protxt, 
                'answer': anstxt
            })
            ex_list.append(newdict)

        try:
            template = env.get_template(templatename)
        except TemplateNotFound:
            tfile = open(templatename,'r')
            utxt = unicode(tfile.read(),'utf-8')
            tfile.close()
            template = Template(utxt)

        fp = open(outfile,'w')
        s = template.render(questionlist=ex_list)
        fp.write( s.encode('utf-8') )
        fp.close()

        return s.encode('utf-8') #devolver todo o latex ja com subsituicoes.

        #Futuro: implementar o pdflatex para ter o "teste na hora"
        """
        #file = os.path.join(SAGE_TMP, outfile)
        _run_latex_(outfile,engine='pdflatex')

        base, filename = os.path.split(outfile)
        filename = os.path.splitext(filename)[0]  # get rid of extension
        if len(filename.split()) > 1:
            raise ValueError, "filename must contain no spaces"
        #if not debug:
        #    redirect=' 2>/dev/null 1>/dev/null '
        #else:
        #    redirect=''
        lt = 'cd "%s"&& sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex}'%(base, 'pdflatex', filename)
        os.system(lt)
        """
    

#Helper for class_question 
import csv
alunos = csv.reader(open(DATA+'alunos_turma_39987_0.csv'), delimiter=';')
for r in alunos:
    print r


