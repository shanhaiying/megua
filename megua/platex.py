r"""
platex -- routines to compile MegUA generated tex files with pdflatex.

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  
import os
import subprocess

from sage.misc.latex import have_pdflatex


def pcompile(latexstr, workdir, filename, runs=1, hideoutput=True,silent=True):
    r"""

    NOTES:

    1. Don't show output messages directly when using notebook because:
        * it too noisy in the screen.
        * many times users are not latex professionals.

    2. utf-8 ou latin1:
        * use latin1 files because they can be exported to windows. 

    3. subprocess.call instead of os.system
       file:///D:/Transfer/python-2.6.4-docs-html/library/subprocess.html

    4. clean latex output files?

    5. TODO: call latex many times only when requested
        * for a single problem this is not neeeded. But for booklets it could be.

    6. Use 1>&  2>, etc etc
       ver http://www.linuxsa.org.au/tips/io-redirection.html

    7. pdflatex -halt-on-error
       pdflatex -interaction nonstopmode
       Check man pdflatex

    8. Remove, from megbook.py:
        self.latex_debug = latex_debug
        if not self.latex_debug:
            print "Use: megook.latex_debug=True, if you want to see LaTex error messages."

    """

    #See /home/jpedro/sage/devel/sage/sage/misc/latex.tex
    assert have_pdflatex()


    #filename must contain no spaces
    filename = os.path.splitext(filename)[0]  # get rid of extension
    if len(filename.split()) > 1:
        raise ValueError, "filename must contain no spaces"


    #Unicode or latin1
    if type(latexstr)==unicode:
        import codecs
        #Store latexstr in filename
        fullpath = os.path.join(workdir, 'utf8-'+filename+'.tex')
        f = codecs.open(fullpath,encoding='utf-8', mode='w+')
        f.write(latexstr)
        f.close()
        
        #Conversion for ISO-8859-1 http://pt.wikipedia.org/wiki/ISO_8859-1
        latexstr = latexstr.encode('latin1')


    #Store latexstr in filename
    fullpath = os.path.join(workdir, filename+'.tex')
    f = open(fullpath,'w')
    f.write(latexstr)
    f.close()

    #compile
    lt = r'cd ' + workdir + '; /usr/bin/pdflatex -interaction=nonstopmode ' + filename
    output = subprocess.check_output(lt,shell=True)

    #TODO: analyse if it need one more run.
    if runs>1:
        output = subprocess.check_output(lt,shell=True)

    return output



"""

    #compile
    #lt = ['sage-native-execute', 'pdflatex', r'\nonstopmode', r'\input{' + filename + '.tex}']
    ###lt = ['/usr/bin/pdflatex', r'\nonstopmode', r'\input{' + filename + '.tex}']
    #Note: to clear ideas: keep inputs and outputs in same directory
    lt = r'cd ' + workdir + '; /usr/bin/pdflatex -interaction=nonstopmode ' + filename + ' 1> /dev/null'

    #TODO: study efect of this in notebook

    if hideoutput:
        #read http://docs.python.org/library/subprocess.html about PIPE. The stdout will get full.
        #redirect = fout #None#subprocess.PIPE#With this "PIPE" argument no text is outputed neither to the commandline or notebook.
        ifout = open('/dev/null','w')
        error = subprocess.check_call(lt, stdout=fout, stderr=fout, cwd=workdir)
        fout.close()
    else:
        error = subprocess.check_call(lt, cwd=workdir) #Output is given in both command line and notebook.

More notes:

Notebook:

            #Create a new file for output
            #TODO: use a different filename because of multiuser environment. Check all "modelo_out.tex".
            #ofilename = os.path.join(SAGE_TMP,'modelo_out.tex')

            ofilename = 'modelo_out.tex'

            f = open(ofilename,'w')
            f.write( air.fulltext.encode('utf-8') )
            f.close()

            print "Compile using:   pdflatex %s" % ofilename

            try:
                os.remove("modelo_out.aux")
            except OSError:
                pass
            try:
                os.remove("modelo_out.out")
            except OSError:
                pass

            #redirect=' 2>/dev/null 1>/dev/null '

            #Compile
            if self.latex_debug:
                lt = 'sage-native-execute %s \\\\nonstopmode \\\\input{%s}' % ('pdflatex', ofilename)
            else:
                lt = 'sage-native-execute %s \\\\nonstopmode \\\\input{%s} 2>/dev/null 1>/dev/null' % ('pdflatex', ofilename)

            os.system(lt)
            os.system(lt)

Notebook print_instance:
                #PDF creation
                pcompile(latex_string, '.', sname, hideoutput=False)

            pl = PLatex('.',ex_instance.name)
            pl.pcompile()

            #create the absolute path and save latex.
            texfilename = os.path.join(SAGE_TMP, ex_instance.name+'.tex')
            #print texfilename
            f = open(texfilename,'w') #open for latin1 for Windows use.
            f.write(latex_string.encode('latin1')) #see latex_string definition above.
            f.close()


            #LaTeX compilation.
            base, filename = os.path.split(texfilename)
            filename = os.path.splitext(filename)[0]  # get rid of extension
            if len(filename.split()) > 1:
                raise ValueError, "filename must contain no spaces"
            
            if self.latex_debug:
                #Compilation with error messages.
                lt = 'cd "%s" && sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex}' % (base, 'pdflatex', filename)
            else:
                #Silent compilation: ' 2>/dev/null 1>/dev/null '
                print "Use: meg.latex_debug = True if you want to see LaTeX error messages."
                lt = 'cd "%s"&& sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex} 2>/dev/null 1>/dev/null' % (base, 'pdflatex', filename)

            print "\nCompiling with pdfLaTeX\n %s \n" % lt

            os.system(lt)

            #Move to the cell folder. This creates a visible link on notebook output cell.
            shutil.move( os.path.join(SAGE_TMP, ex_instance.name+'.pdf'), '.')
            shutil.move( os.path.join(SAGE_TMP, ex_instance.name+'.tex'), '.')


Command line

            ofilename = "modelo_out.tex"
            f = open(ofilename,'w')
            f.write( air.fulltext.encode('utf-8') )
            f.close()

            print "Compile using:   pdflatex %s" % ofilename

            try:
                os.remove("modelo_out.aux")
            except OSError:
                pass
            try:
                os.remove("modelo_out.out")
            except OSError:
                pass

            lt =ur'pdflatex \\nonstopmode \\input{%s} ' % (ofilename)
            os.system(lt)
            os.system(lt)


            texfname = ex_instance.name + '.tex'
    
            f = open(texfname,'w')
            f.write(latex_string.encode('latin1')) #see latex_string definition above.
            f.close()

            os.system("pdflatex %s" % texfname)

        1. Files can be created in SAGE_TMP and then moved to the cell folder to be visible to the user. See `shutil.move` below.

        2. This produces latex (no use of jsmath)  but it cuts when many lines::

                html('<b>' + sname + '</b>')
                html('<b>summary:</b><pre>' + summtxt + '</pre>')
                html('<b>problem:</b><pre>' + probtxt + '</pre>')
                html('<b>answer:</b><pre>' + answtxt + '</pre>')

        3. This solution breaks long pages and shows only the last. Also, it cannot offer the PDF file to user::

                html('<br/><br/><b>Image of the exercise</b>')

                #Producing latex (it must be from a full string otherwise, latex() won't put png images by order
                fullstr = '\n\n\\textbf{Summary}\n\n'+summtxt+'\n\n\\textbf{Problem}\n\n'+probtxt+'\n\n\\textbf{Answer}\n\n'+answtxt+'\n'
                Latex().eval(fullstr,globals=globals)

        4. This does not work here: it is necessary to enter the directory. see below::

                _run_latex_(texfname,debug=False,engine='pdflatex')
                print texfname

                #NOTE: misterio: a directoria corrente e /tmp/tal e tal mas shutil.move(...,'.') move para a celula correcta.
                print os.getcwd() 

        5. It maybe necessary for Internet Explorer::

                html('<a href="%s.pdf" target="_blank">PDF here</a>' % ex_instance.name)
                html('<a href="%s.tex" target="_blank">TeX here</a>' % ex_instance.name)

        6. If output is to be utf-8 open files with this::

                import codecs
                f = codecs.open(texfilename,encoding='utf-8', mode='w+')

                #About unicode
                #print "FULLSTR TYPE = ", type(fullstr)
                #http://docs.python.org/howto/unicode.html
                #fullstr = fullstr.encode('utf-8')
                #import codecs
                #f = codecs.open(texfname,encoding='utf-8', mode='w+')


        7. It seems that '.' is the folder of the computed cell::

                #It seems that notebook prints a link to every cell content in the cell folder (that changed or all?)
                #NOTE: from help (on notebook): 
                # Working Directory:	
                #       Each block of code is run from its own directory. 
                #       If any images are created as a side effect, they will automatically be displayed.
                #http://docs.python.org/library/shutil.html

"""



 

