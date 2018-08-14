import random
def evaluate(nPreguntas,claveExamen,claveAlumno,listaRespuestasAlumno,materia,parametro):
	
	invalidas = []
	noContestadas = []
	correctas = []
	incorrectas = []
	cnt = 1
	respuestas = {0:"a",1:"b",2:"c",3:"d",-1:"No res",-2:"Inval"}
	#scrambleOnlyAnswer = 0
	#if claveExamen[0]==0:
		#print("Evaluando examen que solo tiene las opciones desordenadas aleatoriamente")
	#	scrambleOnlyAnswer = 1
	#else:
		#print("Evaluando examen que tiene desordenadas las preguntas y respuestas")
	if parametro == "1":
		semilla = int(claveAlumno[0])*1000+int(claveAlumno[1])*100+int(claveAlumno[2])*10+int(claveAlumno[3])
	else:
		#print("La clave del examen en la segunda funcion es: ", claveExamen)
		#print(claveExamen[2],claveExamen[3])
		semilla = int(claveExamen[2])*10+int(claveExamen[3])
	#semilla=10
	#print("semilla para numeros aleatorios",semilla)
	#print(claveAlumno)
	###################################################################
	random.seed(semilla) #generating the answers from test seed
	lista = list(range(nPreguntas))
	listaRespuestasCorrectas = []
	#lista = range(len(lista))
	#if scrambleOnlyAnswer==0:
	#print('Antes de desordenar', lista)
	random.shuffle(lista) # this change the order of the questions randomly
	#print('despues de desordenar',lista)
	#random.seed(semilla)
	for i in range(nPreguntas):
		listaRespuestasCorrectas.append(random.randint(0,3))
	#print ("Las respuestas correctas son: ",listaRespuestasCorrectas)
	##print listaRespuestas[0],listaRespuestas[1],listaRespuestas[2],listaRespuestas[3],listaRespuestas[4]
	#print( "n\t","corret\t","Alumno\t","Calificacion")
	for item in listaRespuestasAlumno:
		if cnt>nPreguntas:
			break
		if item == '':
			#print( "No contestada")
			noContestadas.append(cnt)
			cnt+=1
			continue
		if cnt>nPreguntas:
			break
		#print(cnt,"\t",respuestas[listaRespuestasCorrectas[cnt-1]],"\t",respuestas[item],"\t",)
		if item==listaRespuestasCorrectas[cnt-1]:
			#print("Correcta")
			correctas.append(str(cnt)+" ("+respuestas[item]+"), ")
		elif item==-2:
			invalidas.append(cnt)
			#print( "Invalida")
		else:
			incorrectas.append(str(cnt)+" ("+respuestas[item]+"), ")
			#print("Incorrecta")
		cnt+=1
	
	#print("Preguntas correctas:", correctas)
	#print("Preguntas incorrectas:",incorrectas)
	#print("Preguntas invalidas: ",invalidas)
	#print("Preguntas no contestadas:",noContestadas)
	calificacion = round(float(len(correctas))/float(nPreguntas)*10.0,2)
	#print("Calificacion:", calificacion)
	#print("Clave alumno", claveAlumno)
	#print("Clave examen",claveExamen)
	#print("Total de preguntas", nPreguntas)
	return calificacion,incorrectas,correctas,noContestadas

		
	
	

def evaluacionDigital(nombreAlumno,claveAlumno,claveExamen,nPreguntas,materia,listaPreguntas,versionExamen):
	#print( "El total de preguntas es: ",nPreguntas)

	while len(claveExamen)<4:
	  claveExamen = "0" + claveExamen
	#print( "La clave del examen: ", claveExamen)

	while len(claveAlumno)<4:
	  claveAlumno = "0" + claveAlumno
	#print( "La clave del alumno: ", claveAlumno)
	
	##print( "Las respuestas del alumno son: ",listaPreguntas	)
	
	if versionExamen==2016:
		parametro = '0'
	else:
		parametro = '1'
        
	#print( 'version del examen', versionExamen,parametro)
	return evaluate(int(nPreguntas),claveExamen,claveAlumno,listaPreguntas,materia,parametro)

def creaNuevaLinea(linea, calificacion,respuestasEncriptadas):
	""" esta funcion agrega una calificacion a la variable linea

		linea [string]: una cadena que contiene las calificaciones de alguna materia
		calificacion [float]: una calificacion con dos cifras decimales
		return [string]: regresa una linea que tiene correctamente codificada la ultima calificacion

		El formato de la variable linea es:
		021 10 x(!_ 
		021: clave de la materia
		10: primer calificacion de esa materia
		x(!_: resouestas del cuestionario codificadas en ascii
	"""
	elementos = len(linea.split())
	lineaNueva = ""
	for i in range(elementos - 1):
		lineaNueva += linea.split()[i] + " " # usamos un espacio para separar la informacio 
	lineaNueva += str(calificacion) + ' ' # usamos un espacio para separar la informacio
	lineaNueva += respuestasEncriptadas + '\n' # la linea no termina con espacio sino con un enter
	return lineaNueva
def agrega_calificacion(boleta,idMateria,calificacion,respuestas,force = 0):
	""" Agrega una calificacion a la boleta del alumno
		
		respuestas [string]: Esta variable contiene todas las respuestas del cuestionario que acaba de responder el alumno
		Esta funcion recibe el contenido de la boleta, la materia y la calificacion
		el algoritmo permite asignar la calificacion a la materia y tiene un condi-
		cional que limita a tener maximo tres calificaciones.

		Si force = 1, entonces se agreaga una calificacion independientemente de
		que el alumno ya haya utilizado sus tres intentos, esto permite asignar una
		calificacion de manera manual si direccion direccion lo autoriza.
	"""
	boletaNueva = ""
	materiaEncontrada = 0 # variable bandera para saber si existe la materia en la boleta
	respuestasEncriptadas = encripta(respuestas)
	for linea in boleta:
		if len(linea.split())<1: # si no hay ninguna materia registrada en la boleta
			continue
		materia = linea.split()[0]
		if linea[-1]=='\r': # si la ultima linea es un enter (o formalmente un retorno de carro)
			linea = linea[:-1] # no contamos el ultimo caracter, en este caso el retorno de carro
		if int(materia)==int(idMateria): # buscamos la materia correspondiente al examen que hizo el alumno
			# si encontramos la materia en la n-esima linea de la boleta
			# verificamos el numero de intentos en esa materia. para ello consideremos que si la 
			# materia esta en la boleta es porque el alumno ha intentado al menos una vez resolver el cuestionario
			# por lo tanto, la linea de la meateria contiene la clave de la materia, una calificacion (al menos una)
			# y las respuestas codificadas en ascii, es decir tiene al menos tres elementos
			nElementos = len(linea.split())
			print('El numero de elementos en la linea de la boleta es: ',nElementos)
			if nElementos<3: # si hay menos de tres elementos en la linea de la materia
				print('SE HA CORROMPIDO LA INFORMACION EN LA BOLETA DEL ALUMNO')
			materiaEncontrada = 1 # Esta variable bandera indica que la materia esta en la boleta del curso
			nIntentos = nElementos - 2 
			if nIntentos<=3:  # si se han hecho menos de 3+1 intentos, entonces se agrega la nueva calificacion
				#boletaNueva += linea + " " + str(calificacion) +'\n'
				boletaNueva = creaNuevaLinea(linea, calificacion,respuestasEncriptadas)
			elif force==1 and nIntentos<=4: 
				# si direccion evalua con una calificacion extraordinaria
				boletaNueva = creaNuevaLinea(linea, calificacion,respuestasEncriptadas)
			else:
				# Mas intentos de los permitidos
				boletaNueva += linea +'\n'
				return -1 # regresa -1 para indicar que no despligue el resultado de la evaluacion


		else:
			# si no encontramos la materia en la n-esima linea de la boleta entonces
			# no modificamos la boleta y la dejamos como estaba
			boletaNueva += linea +'\n'
	if materiaEncontrada == 0:
		# si es la primera vez que se evalua esa materia
		boletaNueva += str(idMateria) + " " + str(calificacion)+'\n'
	return boletaNueva
def desencripta(respuestas):
	""" Convierte una cadena en ascii a su correspondiente desencriptado de respuestas

		respuestas [str]: cadena que contiene respuestas codificadas como cadena ascii. 
		return a string of integers

		recibimos una cadena, por ejemplo, cad = "'_", el primer caracter tiene un valor ascii de 39 y
		el segundo de 95, la funcion modifica el primer valor restandole 33, lo que resulta en 6, 
		convirtiendo este numero a binario obtenemos 0b110 para el segundo obtendremos bajo el mismo 
		procedimiento obtenemos 0b111110, formalmente cualquier caracter que se reciba se considera 
		que esta formado de 6 bits, por lo tanto el primer valor es 0b000110 y el segundo tiene la 
		sintaxis correcta, ahora leemos los primeros dos bits del numero 0b000110 y los convertimos a su
		equivalente decimal 0b10 = 2, los siguientes dos 0b01 = 1 y finalmente el ultimo par 0b00 = 0,
		dado que procesamos primero los dos bit menos significativos y despues seguimos con los mas 
		significativos es necesario invertir el orden en el que los procesamos, realmente no es necesario,
		si no lo hacemos entonces en la funcion de encriptacion tendriamos que tomar en cuenta esta anomalia, 
		es por ello que se invierte el orden, es decir, el caracter "'" equivale a los enteros
		012 o equivalentemenete a) b) y c) (012), haciendo lo mismo para el otro caracter tenemos que 
		la des-incriptacion equivale a: d) d) c) (332)
	"""
	ans = ''
	for car in respuestas:
		intEq = ord(car) # convierte el caracter a su correspondiente entero ascii
		intEq -= 33  # se le resta 33 porque es donde se definio el inicio de los caracteres ascii
		temp = ''
		for i in range(3):
			temp+=str(intEq&3)# se realiza la operacion binaria con los primeros dos bits de la variable intEq
			intEq=intEq>>2 # se hace un shift de dos bits para comparar los siguientes dos bits de la variable intEq
		for i in range(3):# ahora los ordenamos de manera apropiada ya que el algoritmo anterior muestra al inicio 
			ans+=temp[2-i] # la tercer respuesta y al final la primer respuesta
	return ans
def encripta(res):
	""" Convierte una cadena numerica (que en principio solo contiene 0,1,2 o 3) y la codifica en ascii
	
		res [string]: cadena de enteros
		return [string]: cadena codificada

		por ejemplo, si se recibe la cadean 012332, el programa primero verifica que sean 3 caracteres o multiplos 
		de este numero, eso es importante ya que cada caracter de la cadena ascii que quenere este codigo representa
		3 respuestas, si recibimos una cadena de respuestas en las que no se cumpla esta condicion, llenamos con cero
		los espacios vacios, en alguna otra parte, externo a este codigo, debe de estar indicado hasta donde se 
		consideran respuestas validas, luego de eso el programa convierte el caracter a su equivalente numerico
		y hace una operacion binaria  que recorre a este primer numero 4 bits a la izquierda, por ejemplo el primer 
		caracter numerico que tenemos es el 0, el cual se convierte a 0b00 que despues de correrlo 4 caracteres 
		se convierte a 0b0000, haciendo el mismo procedimiento con el siguiente caracter numerico, pero solo 
		recorriendolo 2 bits a la izquierda 1=0b01 que se convierte en 0b0100, sumando estos dos valores tenemos 
		que el resultado de lasuma es 0b0100 y finalmente el siguiente caracter numerico 2=0b10m, sumandolo al anterior
		resuta en 0b0110 que es el 6 decimal, sumandole 33 para estar en el inicio de los asciis validos para este 
		algoritmo tenemos que es el numero 39 que equivale al caracter "'", haciendolo de manera equivalente para 
		los caracteres 332 obtendriamos el caracter "_"
	"""
	cadena = ""
	ans = 0
	if len(res)%3==1:
		res += '0'
	if len(res)%3==2:
		res += '00'
	cnt=6
	for car in res:
		cnt -= 2
		num = int(car)
		ans += (num<<cnt)
		if cnt == 0:			
			cadena += chr(ans+33)
			ans=0
			cnt = 6
	return cadena