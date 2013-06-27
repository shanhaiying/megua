r"""
MegBookWeb -- Build your own database of exercises to the web.

AUTHORS:

- Pedro Cruz (2012-06): initial version.


"""


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

#Python Modules
import re
import codecs
import random
import json
import httplib, urllib


#Megua modules:
from megbookbase import *
from xc3web import C3WebExporter
from platex import pcompile
from xmoodle import MoodleExporter
from xsphinx import SphinxExporter


#TODO Is it necessary to import other libs?



class MegBookWeb(MegBookBase):
    r"""
    Set of routines for exercise templating to the web.

    INPUT::

    - ``filename`` -- filename where the database is stored.

    This module provides means to use a database of exercises that can be seen as a book of some author or authors.
    """

    def __init__(self,filename=None,natlang='pt_pt'):
        r"""

        INPUT::
        - ``filename`` -- filename where the database is stored.        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.exercise_template = self.megbook.env.get_template("moodle-cloze.xml")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template moodle_cloze.xml"
            raise e

        - ``natlang`` -- natural language ('pt_pt', etc).

        """
        MegBookBase.__init__(self,filename=filename,natlang=natlang,markuplang='web')

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.problem_template = self.env.get_template("xc3web_problem.html")
            self.problemanswer_template = self.env.get_template("xc3web_problemanswer.html")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing templates 'xc3web_problem.html' or 'xc3web_problemanswer.html'."
            raise e

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


    def __str__(self):
        return "MegBookWeb('%s') for %s and markup language %s" % (self.local_store_filename,self.megbook_store.natural_language,self.megbook_store.markup_language)


    def __repr__(self):
        return "MegBookWeb('%s')" % (self.local_store_filename)


    def is_exercise_ok(self,row,dest,silent=True):
        r"""
        Check if exercise is ready for compilation and for python/sage errors.
        """

        # --------------------------------
        # Testing the new python class for 
        # programming errors:
        #     syntax and few instances execution. 
        # -------------------------------
        if not self.exercise_pythontest(row,silent=silent):
            return False


        # --------------------------
        # Testing html compilation. TODO: how to do this?
        # --------------------------
        #if not self.exercise_htmltest(row,dest,silent=silent):
        #    return False

        # Exercise Ok
        return True



    def search_print_row(self,exrow):
        r"""
        This is an helper function of ``Meg.search`` function to print the contents of a search.
        Not to be called by meg user.

        INPUT:

        - ``exrow`` -- an sqlite row structure_ where fields are accessible by name.

        OUTPUT:

        - html or text.

        NOTES:
            unicode is in utf-8 -> string
            http://en.wikipedia.org/wiki/ISO/IEC_8859-1
            Sage html() requires string.
        """
    
        sname = 'Exercise name %s' % exrow['owner_key'].encode('utf8')
        if is_notebook():
            html('<b>' + sname + ': </b><br/>' + exrow['problem_text'].encode('utf8') + '<br/>')
        else:
            print sname + '\n' + exrow['problem_text'].encode('utf8') + '\n'

        

    def print_instance(self, ex_instance):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """

        summtxt =  ex_instance.summary()
        probtxt =  ex_instance.problem()
        answtxt =  ex_instance.answer()
        sname   =  ex_instance.name

        #Use jinja2 template to generate LaTeX.
        answtxt_woCDATA = re.subn(
            '<!\[CDATA\[(.*?)\]\]>', r'\1', 
            answtxt, 
            count=0,
            flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]

        html_string = self.template("print_instance_html.html",
                sname=sname,
                summtxt=summtxt,
                probtxt=probtxt,
                answtxt=answtxt_woCDATA,
                ekey=ex_instance.ekey)

        #Produce files for pdf and png graphics if any tikz code embed on exercise
        html_string = self.publish_tikz(sname,html_string)


        if is_notebook():
            # ---------------
            # Using notebook.
            # ---------------



            #show in notebook
            #html(html_string.encode('utf-8'))

            #file with html to export (extension txt prevents html display).

            #To be viewed on browser
            #f = open(sname+'.html','w')
            #f.write(html_string.encode('latin1'))
            #f.close()
            f = codecs.open(sname+'.html', mode='w', encoding='utf-8')
            f.write(html_string)
            f.close()

            #To be used on sphinx
            f = codecs.open(sname+'.rst', mode='w', encoding='utf-8')
            f.write(html_string)
            f.close()

            #file with html to export.
            #f = open(sname+'.html','w')
            #f.write(html_string.encode('latin1'))
            #f.close()

        else:
            # -------------------
            # Using command line.
            # -------------------
            print html_string



    def publish_tikz(self,sname,html_str):
        """ 
        Receives a string with latex tikz begin{}...end{} environments. Extracts and produce pdf and png file for each tikz graphic.
        """

        #important \\ and \{
        tikz_pattern = re.compile(r'\\begin\{tikzpicture\}(.+)\\end\{tikzpicture\}', re.DOTALL|re.UNICODE)

        #Cycle through existent tikz code and produce pdf and png files.
        graphic_number = 0
        match_iter = re.finditer(tikz_pattern,html_str)#create an iterator
        for match in match_iter:
            #Graphic filename
            gfilename = '%s-%02d'%(sname,graphic_number)
            #Compile tikz picture
            tikz_picture = match.group() 
            tikz_tex = self.template("tikz_graphics.tex", pgfrealjobname=r"\pgfrealjobname{%s}"%sname, beginname=r"\beginpgfgraphicnamed{%s}"%gfilename, tikz_picture=tikz_picture)
            pcompile(tikz_tex,'.','%s-%02d'%(sname,graphic_number),hideoutput=True)
            #convert -density 600x600 pic.pdf -quality 90 -resize 800x600 pic.png
            os.system("convert -density 300x300 '%s.pdf' -quality 90 -resize 400x300 '%s.png'"  % (gfilename,gfilename))
            graphic_number += 1

        #Cycle through existent tikz code and produce a new html string .
        graphic_number = 0
        gfilename = '%s-%02d'%(sname,graphic_number)
        (new_html,number) = tikz_pattern.subn(r"<img src='%s.png'></img>" % gfilename, html_str, count=1)
        while number>0:
            graphic_number += 1
            gfilename = '%s-%02d'%(sname,graphic_number)
            (new_html,number) = tikz_pattern.subn(r"<img src='%s.png'></img>" % gfilename, new_html, count=1)
        
        return new_html

    def make_index(self,where='.',debug=False):
        """
        Produce rst code files from the database and an index reading first line of the %summary field.

        Command line use: 
            The ``where`` input argument, when specified,  will contain all details of Sphinx compilation.

        LINKS:

        http://code.activestate.com/recipes/193890-using-rest-restructuredtext-to-create-html-snippet/

        """

        html_index = SphinxExporter(self,where,debug)
        print "Index is at: "+ html_index.htmlfile

        if is_notebook():
            if where == '.': 
                #To open a browser
                pos = html_index.htmlfile.find(".")
                html(r'<a href="%s" target=_blank>Press to open database index.</a>' % html_index.htmlfile[pos:])
            elif 'data' in where:
                #To open a browser
                pos = html_index.htmlfile.find("/home")
                pos2 = html_index.htmlfile.find("/home",pos+1)
                if pos2>=0:
                    pos = pos2
                html(r'<a href="%s" target=_blank>Press to open database index.</a>' % html_index.htmlfile[pos:])
            else:
                #print "Index is at: "+ html_index.htmlfile
                print "See index at Megua button at top."
        else:
            print "firefox -no-remote ", html_index.htmlfile



    def make_c3web(self,where='.',debug=False):
        """
        Produce html files from the database based on the %summary field.

        Command line use: 
            The ``where`` input argument, when specified.

        LINKS:

        """
        html_index = C3WebExporter(self,where,debug)


    def make_moodlexml(self,where='.',debug=False):
        MoodleExporter(self, where, debug)  


    def siacua(self,exname,ekeys=[],many=2,sendpost=False):
        r"""
        LINKS:
            http://docs.python.org/2/library/json.html
            http://stackoverflow.com/questions/7122015/sending-post-request-to-a-webservice-from-python

        Algorithm:
            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.

        TESTS:
            ~/Dropbox/all/megua/archive$ sage jsontest.sage

        """


        #Create exercise instance
        row = self.megbook_store.get_classrow(exname)
        if not row:
            print "Exercise %s not found." % exname
            return

        ekeys2 = self._build_ekeys(ekeys,many)



        (concept_dict,concept_list) = self._siacua_extract(row['summary_text'])

        #For _siacua_sqlprint
        f = codecs.open(exname+'.html', mode='w', encoding='utf-8')
        f.write(u"<html><body><h2>Copy/paste do conte\xFAdo e enviar ao Sr. Si\xE1cua por email. Obrigado.</h2>")
        
        for e_number in ekeys2:

            #Create exercise instance
            ex_instance = exerciseinstance(row, ekey=e_number)

            problem = ex_instance.problem()
            answer = ex_instance.answer()
            answer_list = self._siacua_answer_extract(answer)


            #build json string
            send_dict =  self._siacua_json(exname, e_number, problem, answer_list, concept_list)
            send_dict.update(concept_dict)

            #Call siacua for store.
            #call in future
            #print send_dict

            if sendpost:
                self._siacua_send(send_dict)

            self._siacua_sqlprint(send_dict,concept_list,f)



        #Ending _siacua_sqlprint
        f.write(r"</body></html>")
        f.close()
 
        print r"Copy/paste of contents and send to Sr. Siacua using email. Merci."


    def _siacua_send(self, send_dict):
        params = urllib.urlencode(send_dict)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("localhost")
        conn.request("POST", "/ajax/post_work.php", params, headers)
        response = conn.getresponse()
        #TODO: improve message to user.
        print response.status, response.reason
        #data = response.read()
        #print "============"
        #print data
        #print "============"
        conn.close()


    def _build_ekeys(self,ekeys,many=2):
        r"""From ekeys or many build a range of ekeys."""

        if ekeys is None or len(ekeys)==0:
            
            #generate incresing sequence of keys
            #start = random.randint(1,100000)
            start = ZZ.random_element(1,100000)
            return [start + i for i in range(many)]
        else:
            return ekeys

    def _siacua_answer_extract(self,answer_text):
        r"""
        Does the parsing of answer to extract options and complete answer.
        """
        l = re.findall('<!\[CDATA\[(.*?)\]\]>', answer_text, re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)
        return l


    def _siacua_json(self,exname, e_number, problem, answer_list,concepts_list):
        r"""
        LINKS:
            http://docs.python.org/2/library/json.html
        """

        #Dictionary with fields
        d = {}

        #Wrong answers
        d.update( self._siacua_wronganswerdict(answer_list) )

        #Other fields
        d.update( {
            "exname": exname, 
            "ekey": str(e_number), 
            "problem":  json.dumps(problem.strip(), encoding="utf-8"), 
            "answer":   json.dumps(answer_list[-1].strip(), encoding="utf-8"),
            "rv":       json.dumps(answer_list[0].strip(), encoding="utf-8"),
            "nre": len(answer_list) - 2
            } )

        #TODO: colocar concepts_list no dict

        #return json.dumps(d,
        #    ensure_ascii=True, 
        #    encoding="utf-8")
        return d


    def _siacua_wronganswerdict(self,alist):
        r"""Wrong answer extraction"""

        nre = len(alist) - 2 # 2 = "correct option" + "detailed answer"
        #TODO: warn user from this maximum
        #assume(0<=nre<=6)

        d = dict()

        d["re1"] =  json.dumps(alist[1].strip(), encoding="utf-8") if nre>=1 else ""
        d["re2"] =  json.dumps(alist[2].strip(), encoding="utf-8") if nre>=2 else ""
        d["re3"] =  json.dumps(alist[3].strip(), encoding="utf-8") if nre>=3 else ""
        d["re4"] =  json.dumps(alist[4].strip(), encoding="utf-8") if nre>=4 else ""
        d["re5"] =  json.dumps(alist[5].strip(), encoding="utf-8") if nre>=5 else ""
        d["re6"] =  json.dumps(alist[6].strip(), encoding="utf-8") if nre>=6 else ""

        return d

    def _siacua_sqlprint(self,send_dict, concept_list,f):
        """Print SQL INSERT instruction"""

        html_string = self.template("print_instance_sql.html",
                exname  = send_dict["exname"],
                ekey    = send_dict["ekey"],
                probtxt = json.loads(send_dict["problem"]),
                answtxt = json.loads(send_dict["answer"]),
                correct = send_dict["rv"], #"resposta verdadeira" (true answer)
                nwrong  = send_dict["nre"],
                wa1     = json.loads(send_dict["re1"]) if send_dict["re1"]!="" else "",
                wa2     = json.loads(send_dict["re2"]) if send_dict["re2"]!="" else "",
                wa3     = json.loads(send_dict["re3"]) if send_dict["re3"]!="" else "",
                wa4     = json.loads(send_dict["re4"]) if send_dict["re4"]!="" else "",
                wa5     = json.loads(send_dict["re5"]) if send_dict["re5"]!="" else "",
                wa6     = json.loads(send_dict["re6"]) if send_dict["re6"]!="" else "",
                level   = send_dict["level"],
                slip    = send_dict["slip"],
                guess   = send_dict["guess"],
                discr   = 0.3,
        )

        f.write(html_string)

        for c in concept_list:

            html_string = self.template("print_instance_sql2.html",
                conceptid  = c[0],
                weight     = c[1],
            )

            f.write(html_string)



    def _siacua_extract(self,summary_text):
        """
        Extract from summary:
            SIACUAstart
            guess=2;  slip= 0.2; guess=0.25
            concepts = [(1221, 1)]
            SIACUAend
        export to:
                level   = send_dict["level"],
                slip    = send_dict["slip"],
                guess   = send_dict["guess"],
        """

        #TODO: TERMINAR esta FUNcao

        concepts_match = re.search(
            r'SIACUAstart(.*?)SIACUAend', 
            summary_text, 
            flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)

        if concepts_match is not None:
            #print "GROUP 1=", concepts_match.group(1)
            exec concepts_match.group(1)
        else:
            print "The summary needs the following lines:\nSIACUAstart\nguess=2;  slip= 0.2; guess=0.25\nconcepts = [(1221, 1)]\nSIACUAend\n"
            raise ValueError

        return (dict(level=level, slip=slip, guess=guess), concepts)




    def c3web(self, exname, ename="e", rname="r", startnumber=1, many=10,  whatinside="E", ekey=0, edict={}, where='c3web'):
        """
        Save an exercse to aspx page.

	INPUT:

	- exname: string with exercise identification name.
	- many: how many samples (starting ekey generated key).
        - ename: filename prefix for file with exercise text.
        - rname: filename prefix for file with resolution text.
        - startnumber: number for filename.
        - whatinside: "E" for extrema, "L" for limits, whatever...
	- ekey: random values generation key.
	- edict: some values declared on make_random or solve functions of the exercise.

        EXAMPLES:

        Full use of parameters::

            sage: meg.c3web("E12A34_Aplic_DerivadasE1_002", many=10, ekey=100, edict={'a': 10})

        Less parameters::

            sage: meg.c3web("E12A34_Aplic_DerivadasE1_002", many=10 )

        NOTES:
          See C3WebExporter for saving full database.
        """

        #If does not exist create
        if not os.path.exists(where):
            os.makedirs(where)


        #Create exercise instance
        row = self.megbook_store.get_classrow(exname)
        if not row:
            print "Exercise %s not found." % exname
            return

        for e_number in range(many):

            #Continuous numeration of exercises
            exnr = startnumber + e_number

            #Create exercise instance
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


        import subprocess
        subprocess.call("zip %s %s" % (where, where+r'/*'), shell=True)


    def moodle(self, exname, questiontype="mchoice", many=10,  ekey=0, where='.'):
        """
        Save an exercse to moodle xml file format.

	INPUT:

	- exname: string with exercise identification name.
	- questiontype: "mchoice" or "cloze"
	- many: how many samples (starting ekey generated key).
	- ekeys: random values generation key.
        - where: local folder to store data.

        EXAMPLES:

        Full use of parameters::

            sage: meg.moodle("E12A34_Aplic_DerivadasE1_002", "mchoice", many=10, ekey=100)

        Less parameters::

            sage: meg.moodle("E12A34_Aplic_DerivadasE1_002", many=10 )

        """

        #If does not exist create
        if not os.path.exists(where):
            os.makedirs(where)


        #Create exercise instance
        row = self.megbook_store.get_classrow(exname)
        if not row:
            print "Exercise %s not found." % exname
            return

        questions_xml = unicode('')

        for e_number in range(many):

            #Create exercise instance
            ex_instance = exerciseinstance(row, ekey= ekey + e_number)

            if questiontype=='mchoice':
                questions_xml += self.mchoice_template.render(
                    sections= m_get_sections(row['sections_text']),
		    exercisename = exname,
		    ekey = e_number,
                    problemname=row['suggestive_name'],
                    answertext = ex_instance.answer(),
                    problemtext = ex_instance.problem()
                )
            else:
                questions_xml += self.cloze_template.render(
                    sections= m_get_sections(row['sections_text']),
		    exercisename = exname,
		    ekey = e_number,
                    problemname=row['suggestive_name'],
                    answertext = ex_instance.answer(),
                    problemtext = ex_instance.problem()
                )


        # -----------------
        # output file
        # -----------------
        xmlfilename = "quiz-%s.xml" % exname
        xmlfile = codecs.open(xmlfilename, encoding='utf-8', mode='w')
        xmlfile.write('<?xml version="1.0" encoding="utf-8"?>\n<quiz>\n')
        xmlfile.write(questions_xml)
        xmlfile.write("\n</quiz>")
        xmlfile.close()


def m_get_sections(sectionstxt):
    """

    LINKS::

       http://stackoverflow.com/questions/2054746/how-to-search-and-replace-utf-8-special-characters-in-python?rq=1
    """   
    s = "megua/"+sectionstxt.replace("; ","/") #case "; " by "/"
    return s.replace(";","/") #possible case without space: ";" by "/"



#end class MegBookWeb

