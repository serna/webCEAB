# esta version genera el archivo para el examen del alumno con una semilla de numeros aleatorios igual a l numero de alumno
carpeta1 = "~/Desktop/impresionExamen"
import sys
import os
def toLatexQuestion(question,order,linea):
	""" Return a latex valid sintaxis of a question
		
		linea [int]: The number of the corresponding line in the data bank
		question [string]: question that comes from bancoDatos, it is written in a valid latex sintaxis, 
		format: Question | optCorrect | opt2 | opt3 | opt3
		order [int]: this parameter defines the where the correct option will be positioned
	"""
	# Added tabs at the start of each latex line, just to make it easier to read the latex output.
	ans = ""
	if question[0:2]=="{s": # The user is defining a new section
		print( "SE IMPRIMIO UNA SECCION")
		section = question.split("}")[0][2:]
		
		ans ="\n\\section{" + section+ "}\n"
		pos = question.find("}")
		question = question[pos+1:]
	elif question[0:2]=="{p": # User is defining a paragraph
		print( "SE IMPRIMIO UN PARRAFO")
		paragraph = question.split("}")[0][2:]
		if len(paragraph.split(']'))>1: # If the paragraph does have a title
			title = paragraph.split(']')[0][1:]
			ans+= "\n{\\bf " + str(title) + "}"
			print( "SE IMPRIMIO EL TITULO", str(title))
			paragraph = paragraph.split(']')[1]
			ans += paragraph  
		else:
			ans = paragraph + "\n"
		pos = question.find("}")
		question = question[pos+1:]
	elif question[0:2]=="{b": # if it is a section and a paragraph
		print ("SE IMPRIMIERON AMBOS")
		commands = question.split("}")[0][2:]
		section = commands.split("|")[0]
		ans = "\\section{" + section+ "}\n"
		paragraph = commands.split("|")[1]
		#print "VVVVVVVVVVVVVVV",section,"PARRAFO ",paragraph
		if len(paragraph.split(']'))>1: # If the paragraph does have a title
			title = paragraph.split(']')[0][1:]
			ans+= "\n{\\bf " + str(title) + "}"
			paragraph = paragraph.split(']')[1]
			print( "TITULO DEL PARRAFO ", title,"A PARTIR DEL ]",paragraph)
			ans += paragraph 
		else:
			ans += paragraph + "\n"
		pos = question.find("}")
		question = question[pos+1:]
	else:
		print( "NO SE ELIGIO NADA")
	ans += "\n\t\\begin{enumerate}[resume]"
	ans += "		\n\t\\item " + question.split("|")[0]+ "\n"
	ans += "		\\begin{tasks}[counter-format = {tsk[a])},label-offset = {0.1em},label-format = {\\bfseries}](2) "+ "\n"
	
	cnt = 0
	if len(question.split("|")) < 5:
		print( "La sintaxis de captura del banco de datos esta mal en la linea:",  linea,len(question.split("|")))
		print (question)
		print ("Falta el caracter especial '|'")
		quit()
	#print len(question.split("|")),order,order+1
	for i in range(len(question.split("|"))-1):
		
		#print i, len(question.split("|")),question.split("|")
		if order!=0:
			if i==0:
				ans += "\t\t\t\\task " + question.split("|")[order+1]+ "\n"
			elif i==order:
				ans += "\t\t\t\\task " + question.split("|")[1]+ "\n"
			else:
				ans += "\t\t\t\\task " + question.split("|")[i+1]+ "\n"
		else:
			ans += "\t\t\t\\task " + question.split("|")[i+1]+ "\n"
		cnt += 1
	#print order
	ans += "	\t\\end{tasks}"
	ans += "\n\t\\end{enumerate}"
	return ans
def latexPreamble(testName,clave,version,nPreguntas,claveAlumno2):
	"""Define the common preamble for test template
	"""
	ans = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Large Colored Title Article
% LaTeX Template
% Version 1.1 (25/11/12)
%
% This template has been downloaded from:
% http://www.LaTeXTemplates.com
%
% Original author:
% Frits Wenneker (http://www.howtotex.com)
%
% License:
% CC BY-NC-SA 3.0 (http://creativecommons.org/licenses/by-nc-sa/3.0/)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------------------------------------
%   PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
%----------------------------------------------------------------------------------------

\\documentclass[DIV=calc, paper=letterpaper, fontsize=14pt]{scrartcl}   % A4 paper and 11pt font size
\\textwidth=18.5cm
\\usepackage{geometry}
\\geometry{left = 5mm,top = 18mm,bottom = 28mm,right = 5mm}
\\usepackage{lipsum} % Used for inserting dummy 'Lorem ipsum' text into the template
\\usepackage[spanish]{babel} % English language/hyphenation
\\usepackage[utf8]{inputenc}
\\usepackage[protrusion=true,expansion=true]{microtype} % Better typography
\\usepackage{amsmath,amsfonts,amsthm} % Math packages
\\usepackage[svgnames,dvipsnames]{xcolor} % Enabling colors by their 'svgnames'
\\usepackage[hang, small,labelfont=bf,up,textfont=it,up]{caption} % Custom captions under/above floats in tables or figures
\\usepackage{booktabs} % Horizontal rules in tables
\\usepackage{fix-cm}  % Custom font sizes - used for the initial letter in the document
\\usepackage{framed, color}
\\usepackage{url}
\\usepackage{enumitem} % allows to resume counting from enumerate command
%%%%%%%%%%%%%%%%% Farbige box
\\usepackage{tcolorbox}

%%%%%%%%%%%%%%%%%



\\usepackage{sectsty} % Enables custom section titles
\\allsectionsfont{\\usefont{OT1}{phv}{b}{n}} % Change the font of all section commands

\\usepackage{fancyhdr} % Needed to define custom headers/footers

\\pagestyle{fancy} % Enables the custom headers/footers
\\usepackage{lastpage} % Used to determine the number of pages in the document (for "Page X of Total")

\\usepackage{mwe}% for example-image

% Headers - all currently empty
\\lhead{"""
	ans +=str(testName)+"""\\rule{\\linewidth}{1pt}}
\\chead{}
\\rhead{}

% Footers
\\lfoot{{\\footnotesize V.2018}}
\\cfoot{}
\\rfoot{\\footnotesize P\\'agina \\thepage} % "Page 1 of 2"

\\renewcommand{\\headrulewidth}{0.0pt} % No header rule
\\renewcommand{\\footrulewidth}{0.4pt} % Thin footer rule

\\usepackage{lettrine} % Package to accentuate the first letter of the text
\\newcommand{\\initial}[1]{ % Defines the command and style for the first letter
\\lettrine[lines=3,lhang=0.3,nindent=0em]{
\\color{OliveGreen}
{\\textsf{#1}}}{}}

%----------------------------------------------------------------------------------------
%   TITLE SECTION
%----------------------------------------------------------------------------------------

\\usepackage{titling} % Allows custom title configuration

\\newcommand{\\HorRule}{\\color{OliveGreen} \\rule{\\linewidth}{1pt}} % Defines the gold horizontal rule around the title

\\pretitle{\\vspace{-30pt} \\begin{flushleft} \\HorRule \\fontsize{30}{30} \\usefont{OT1}{phv}{b}{n} \\color{RawSienna} \\selectfont} % Horizontal rule before the title


\\title{"""
	ans+= str(testName)+ """} % Your article title

\\posttitle{\\par\\end{flushleft}\\vskip 0.5em} % Whitespace under the title

\\preauthor{\\begin{flushleft}\\large \\lineskip 0.5em \\usefont{OT1}{phv}{b}{sl} \\color{Black}} % Author font configuration

\\author{"""
	#ans += "Clave del examen: " + str(clave) + str(version) + "\\\\Total de preguntas: " + str(nPreguntas)
	ans += "Clave del examen: " + str(clave) + "\\\\Total de preguntas: " + str(nPreguntas) + "\\\\Clave del Alumno: " + str(claveAlumno2)
	ans += """\\\\} % Your name

\\postauthor{\\footnotesize \\usefont{OT1}{phv}{m}{sl} \\color{Black} % Configuration for the institution name
Centro de estudios abiertos y a distancia CEAB\\\\
% Your institution

%% logo
%\\rhead{\\raisebox{-2.0\\height}{\\includegraphics[height=40mm]{images/logo2}}}

\\par\\end{flushleft}\\HorRule} % Horizontal rule after the title

\\date{} % Add a date here if you would like one to appear underneath the title block

%----------------------------------------------------------------------------------------
\\usepackage{tasks}	
\\begin{document}
\\maketitle
 \\noindent\\raisebox{29mm}[0pt][0pt]{\\rlap{\\makebox[\\textwidth][r]{\\includegraphics[height=30mm]{images/logo}}}}
 {\\bf Instrucciones: } Lee con atenci\\'on las preguntas y responde el examen en tu hoja de respuestas, recuerda registrar bien tu clave de alumno y clave de examen, as\\'i como el n\\'umero de preguntas.
 %\\section{Responde las preguntas en tu hoja de respuestas}
 
 
"""
	#ans += "\\title{Examen: " + str(testName) + "\\\\ Clave: " + str(clave)+str(version) +"\\\\N\\'umero de preguntas: " + str(nPreguntas)+ """}	

	return ans

import sys
import random
import os # for operations in the OS
def mkdir(dir_name):
    """ Creates a directory named 'dir_name' """
    try:
        os.makedirs(dir_name)
        return 1
    except OSError:
        if os.path.exists(dir_name):
            #pass
            return 0
        # let exception propagate if we just can't

def crea_archivo(nombre,contenido):
	cadena = r"""
\documentclass[a4paper,10pt,fleqn]{article}
\setlength{\mathindent}{0pt}
\usepackage[spanish]{babel}
\usepackage{fancyhdr}
\pagestyle{fancy}

\usepackage[ddmmyy]{datetime}

\usepackage{float}
\usepackage[utf8]{inputenc}
\usepackage{enumitem} 

\rhead{\today}
\chead{}
\lhead{\textbf{Aplicaci\'on de la derivada: optimizaci\'on.}}
\lfoot{Matem\'aticas}
\cfoot{}
\rfoot{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}


\title{}
\author{}
\date{}


\begin{document}

\maketitle
\thispagestyle{fancy}
Alumno: %s
Nombre de la materia: %s
Numero de preguntas: %d
Resuelve correctamente los siguientes ejercicios.
  \begin{enumerate}[resume]
    \item ¿Cu\'al es el \'area m\'axima posible de un rect\'angulo, cuya base 
	coincide con el eje $x$ y sus v\'ertices superiores est\'an en la curva $- 10 x^{2} + 2$?
	
    \item ¿Cu\'al es el \'area m\'axima de un rect\'angulo que se puede 
	inscribir en un semicirculo de radio 6 cm?. 
	
    \item La resistencia de una viga rectangular var\'ia según sus 
	dimensiones. Si la resistencia es proporcional al cuadrado del ancho de la 
	viga por la altura, ¿cu\'al es el \'area' de la viga m\'as resistente 
	que podr\'a cortarse de un tronco cil\'ndrico con radio de 4 pies?
	
    \item ¿Cu\'al es la distancia m\'inima que existe entre el punto 
	(-2, -1) y la par\'abola $y=4*x**2 + 9*x + 1$ ?
    \item ¿Cu\'al es el per\'imetro del rect\'angulo de mayor per\'imetro 
	que se puede inscribir en un semic\'irculo con radio de 10 unidades?
	
    \item Se inscribe un rect\'angulo en un tri\'angulo is\'osceles, cuyos 
	lados tienen longitudes 8, 8 y 9. Uno de los lados del rect\'angulo est\'a sobre
	la base del tri\'angulo (lado desigual), ¿cu\'al es el \'area mayor que puede
	abarcar el rect\'angulo?
	
    \item Calcula el \'area' de un tri\'angulo is\'osceles con un per\'imetro
	de 8 unidades que tenga \'area m\'axima.
	
    \item Obt\'en la distancia m\'as corta entre la recta $y=- 2 x - 1$ y el origen.
	
    \item ¿Cu\'al es el\'area del rect\'angulo mayor que se puede 
	inscribir en un tri\'angulo rect\'angulo de lados 42, 56 y 70 cm?.
	
    \item Una persona tiene una pared de piedra en el costado de un terreno.
	Dispone de 3600 m de material para cercar y desea hacer un corral rectangular 
	utilizando el muro como uno de sus lados, ¿qu\'e dimensiones debe tener el
	corral para tener la mayor \'area posible?.
	\begin{verbatim}
	%s
	\end{verbatim}
  \end{enumerate}


\end{document}

	"""%(contenido["alumno"],contenido["materia"],contenido["n_preguntas"],contenido["lineas"])
	#print(cadena)
	en_orden = contenido["en_orden"]
	folio = contenido["folio"]
	preguntas = contenido["lineas"]
	materia = contenido["materia"]
	preguntas_validas = []
	for pregunta in preguntas:
		# revisamos que tenga al menos 5 elementos separados por un simbolo |
		print("### Lo que contiene la linea", pregunta,type(pregunta))
		if len(pregunta.split("|"))>=5:

			preguntas_validas.append(pregunta)


	cadena = genera_TEX_PDF(folio_alumno=folio,en_orden = en_orden,listaPreguntas=preguntas_validas,testName = materia)
	print(cadena)
	ff = open(nombre,"w")
	ff.write(cadena)
	ff.close()
	print("Nombra del archivo: ",nombre)
	
	os.system("pdflatex %s "%(nombre))
	#os.system("pdflatex -interaction=nonstopmode %s "%(nombre))
	print("Borrando el archivo .aux")
	try: 
		os.system("rm %s"%(nombre[:-3]+"aux"))
	except:
		print("No se pudo borrar el archivo %s"%(nombre[:-3]+"aux"))

	print("Borrando el archivo .log")
	try: 
		os.system("rm %s"%(nombre[:-3]+"log"))
	except:
		print("No se pudo borrar el archivo %s"%(nombre[:-3]+"log"))
	
	print("Borrando el archivo .tex")
	try: 
		os.system("rm %s"%(nombre[:-3]+"tex"))
	except:
		print("No se pudo borrar el archivo %s"%(nombre[:-3]+"tex"))

	print("Moviendo archivo .pdf a la carpeta pdfs")
	try:
		cadena ="mv %s pdfs/"%(nombre[:-3]+"pdf")
		print(cadena)
		os.system(cadena)
	except:
		print("No se pudo mover el archivo %s"%(nombre[:-3]+"pdf"))

def genera_TEX_PDF(folio_alumno,listaPreguntas,testName ,en_orden = 0):
	# folio_alumno: es el numero de folio del documento que usa CEAB para inscribir alumnos
	# en_orden: Si es 1 solo se desordena el orden da las respuestas pero no la numeracion de los ejercicios
	# if the user is printing a particular version of the test
	clave = "0000"
	print( clave,str(clave))
	versionStr = str(clave)
	version = int(clave)
	if clave[0]=="0":
		print( "Only scramble options not scramble order of questions",str(int(clave)))
		# if version starts with 0, then only scramble the order of the answer but not the questions
		scrambleOnlyAnswer = 1
	scrambleOnlyAnswer = en_orden
	if version<10:
		versionStr = '0'+versionStr
	
	print( "Impresion de la version", version,int(version),versionStr)
	# check if the directory tex already exists
	#if os.path.isdir("tex/")==False: # if the directory in which texs files are goin to be compiled do not exist
	#	mkdir("tex") # create the directory
	#fileName = "tex/"
	
	#fileName = sys.argv[1][:-4] + "_" + str(versionStr) + ".tex"
	#ff1 = open(fileName,"w")
	cadena = latexPreamble(testName,clave,versionStr,len(listaPreguntas),folio_alumno) # start writing latex file
	version = int(folio_alumno)
	print("La semilla para el examen es: ",version)
	random.seed(version) #start the random generator with seed establish by the version of the test
	respuestas = [] # this array stablish in which position is the correct answer, this is done randomly
	if scrambleOnlyAnswer==0:
		print( "Se ha mezclado el orden de las preguntas\n")
		random.shuffle(listaPreguntas) # this change the order of the questions randomly
	random.seed(version) #start the random generator with seed establish by the version of the test
	lista = list(range(len(listaPreguntas)))
	random.shuffle(lista)
	#print lista
	for i in range(len(listaPreguntas)):
		pos = random.randint(0,3)
		print('POS',pos)
		respuestas.append(pos) 
	print( respuestas)
	cnt = 0
	for line in listaPreguntas:
		if len(line)>1:
			cadena += toLatexQuestion(line,respuestas[cnt],cnt+2)
		cnt += 1
	#ff1.write("\n\t\\end{enumerate}") # end of questions
	cadena += "\n\\end{document}"
	return cadena
        


	#comando = "pdflatex " + fileName
	#os.system(comando)

	#rutaCompleta = fileName
	#fileName = fileName.split("/")[-1]

	#comando = "rm " + fileName
	#os.system(comando)
	#comando = "rm " + fileName[:-4] +".log"
	#os.system(comando)
	#comando = "rm " + fileName[:-4] +".aux"
	#os.system(comando)
	#comando = "cp " + fileName[:-4] + ".pdf " + carpeta1+"/examen.pdf"
	#os.system(comando)
	#comando = "evince " + carpeta1 + "/examen.pdf&"
	#os.system(comando)
	#comando = "rm " + fileName[:-4] +".pdf"
	#os.system(comando)
	#print( fileName)
	#print( fileName[:-4])
	
	"""ff = open("script.sh","w")
	#once the document is written, call klatex to buil the pdf file
	ff.write("cd tex/\n")
	ff.write("pdflatex "+ fileName[4:]+"\n")
	ff.write("mv " + fileName[4:-4]+ ".pdf \..\n")
	ff.write("cd ..\n")
	#ff.write("rm tex/*")
	
	ff.close()
	os.chmod("script.sh", 0755) # change to execution mode all the scripts
	os.system("./script.sh" )"""

