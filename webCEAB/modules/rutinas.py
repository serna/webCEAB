import random
def evaluate(nPreguntas,claveExamen,claveAlumno,listaRespuestasAlumno,materia,parametro):
	
	invalidas = []
	noContestadas = []
	correctas = []
	incorrectas = []
	cnt = 1
	respuestas = {0:"a",1:"b",2:"c",3:"d",-1:"No res",-2:"Inval"}
	#scrambleOnlyAnswer = 0
	if claveExamen[0]==0:
		print("Evaluando examen que solo tiene las opciones desordenadas aleatoriamente")
	#	scrambleOnlyAnswer = 1
	else:
		print("Evaluando examen que tiene desordenadas las preguntas y respuestas")
	if parametro == "1":
		semilla = int(claveAlumno[0])*1000+int(claveAlumno[1])*100+int(claveAlumno[2])*10+int(claveAlumno[3])
	else:
		print("La clave del examen en la segunda funcion es: ", claveExamen)
		print(claveExamen[2],claveExamen[3])
		semilla = int(claveExamen[2])*10+int(claveExamen[3])
	#semilla=10
	print("semilla para numeros aleatorios",semilla)
	print(claveAlumno)
	###################################################################
	random.seed(semilla) #generating the answers from test seed
	lista = list(range(nPreguntas))
	listaRespuestasCorrectas = []
	#lista = range(len(lista))
	#if scrambleOnlyAnswer==0:
	random.shuffle(lista) # this change the order of the questions randomly
	#random.seed(semilla)
	for i in range(nPreguntas):
		listaRespuestasCorrectas.append(random.randint(0,3))
	print("Las respuestas correctas son: ",listaRespuestasCorrectas)
	#print listaRespuestas[0],listaRespuestas[1],listaRespuestas[2],listaRespuestas[3],listaRespuestas[4]
	print("n\t","corret\t","Alumno\t","Calificacion")
	for item in listaRespuestasAlumno:
		if cnt>nPreguntas:
			break
		print(cnt,"\t",respuestas[listaRespuestasCorrectas[cnt-1]],"\t",respuestas[item],"\t",)
		if item==listaRespuestasCorrectas[cnt-1]:
			print("Correcta")
			correctas.append(str(cnt)+" ("+respuestas[item]+"), ")
		elif item==-1:
			
			print( "No contestada")
			noContestadas.append(cnt)
		elif item==-2:
			invalidas.append(cnt)
			print( "Invalida")
		else:
			incorrectas.append(str(cnt)+" ("+respuestas[item]+"), ")
			print("Incorrecta")
		cnt+=1
	
	print("Preguntas correctas:", correctas)
	print("Preguntas incorrectas:",incorrectas)
	print("Preguntas invalidas: ",invalidas)
	print("Preguntas no contestadas:",noContestadas)
	calificacion = round(float(len(correctas))/float(nPreguntas)*10.0,2)
	print("Calificacion:", calificacion)
	print("Clave alumno", claveAlumno)
	print("Clave examen",claveExamen)
	print("Total de preguntas", nPreguntas)
	return calificacion,incorrectas

		
	
	

def evaluacionDigital(nombreAlumno,claveAlumno,claveExamen,nPreguntas,materia,listaPreguntas,versionExamen):
	print( "El total de preguntas es: ",nPreguntas)

	while len(claveExamen)<4:
	  claveExamen = "0" + claveExamen
	print( "La clave del examen: ", claveExamen)

	while len(claveAlumno)<4:
	  claveAlumno = "0" + claveAlumno
	print( "La clave del alumno: ", claveAlumno)
	
	print( "Las respuestas del alumno son: ",listaPreguntas	)
	
	if versionExamen==2016:
		parametro = '0'
	else:
		parametro = '1'
        
	print( 'version del examen', versionExamen,parametro)
	return evaluate(int(nPreguntas),claveExamen,claveAlumno,listaPreguntas,materia,parametro)