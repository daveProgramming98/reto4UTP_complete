def promedio_facultades(info: dict, contando_externos: bool = True) -> tuple:
	# Armamos el correo de un estudiante
	def armarCorreo(nombres: str, apellidos: str, documento: int):
		nom = nombres.split()
		ap = apellidos.split()
		documento = str(documento)
		correo = ""
		# Si el estudiante tiene 2 nombres
		if len(nom) == 2:
			# Primera letra del primer nombre
			correo = correo + nom[0][0]
			# Primera letra del segundo nombre
			correo = correo + nom[1][0]
			# (".") un punto
			correo = correo + "."
			# Primer Apellido
			correo = correo + ap[1]
			# Dos ultimos numeros del documento
			correo = correo + documento[-2] + documento[-1]
		else:
			# Si el estudiante tiene 1 nombre
			if len(nom) == 1:
				# Primera letra del primer nombre
				correo = correo + nom[0][0]
				# Primera letra del primer apellido
				correo = correo + ap[1][0]
				# (".") un punto
				correo = correo + "."
				# Segundo Apellido
				correo = correo + ap[0][:-1]
				# Dos ultimos numeros del documento
				correo = correo + documento[-2] + documento[-1]

		# Convertir todas los caracteres del correo a letras minusculas (funcion lower)
		correo = correo.lower()

		# Convertir los caracteres del alfabeto con tilde (á, é, í, ó, ú) a sin tilde
		# y Convertir el caracter (ñ) a (n)
		# (funcion replace)

		letrasChange = [("á", "a"),
						("é", "e"),
						("í", "i"),
						("ó", "o"),
						("ú", "u"),
						("ñ", "n")]

		for valorReemp, valorCam in letrasChange:
			correo = correo.replace(valorReemp, valorCam)

		return correo
	def laRetiro(materia: dict) -> bool:
		claveRet = materia["retirada"]
		if claveRet == "No":
			return True
		else:
			return False
	def CeroCreditos(materia: dict) -> bool:
		creditos = materia["creditos"]
		if creditos != 0:
			return True
		else:
			return False
	def cursoVerano(codEst: int) -> bool:
		# Convertir a str
		codEst = str(codEst)
		# Rescatar las posiciones {pos4:pos5} del String
		perIngEst = codEst[4:6]
		if perIngEst != "05":
			return True
		else:
			return False
	def valMatProg(programa: str, materia: dict) -> bool:
		# Obtnemos el codigo de la materia
		codigoMat = materia["codigo"]
		# Obtner la longitud del Str programa
		longProg = len(programa)
		# Redefinir la variable codigoMat, tomando desde la posicion 0 hasta la longitud de la variable programa
		codigoMat = codigoMat[0:longProg]
		if programa == codigoMat:
			return True
		else:
			return False
	def facultadesIni(info: dict) -> dict:
		# Inicializamos un conjunto vacio para guardar las facultades
		facult = set()
		for codigoEst in info:
			# Obteniendo la informacion de cada materia -> Dict
			for materia in info[codigoEst]["materias"]:
				nomFac = materia["facultad"]
				facult.add(nomFac)
		facult = list(facult)
		facult.sort()

		# Obtener long de la lista facultades
		lenFac = len(facult)
		# Inicializamos un diccionario vacio
		valoresFac = {}
		for fac in facult:
			# Iterar y agregar cada facultad como una clave para el diccionario
			# Iterar y agregar un arreglo [0, 0] para cada clave del diccionario
			valoresFac[fac] = [0, 0]
		return valoresFac
	try:
		# Inicializamos un conjunto vacio para guardar los correos de los estudiantes
		correos = set()
		# COnsideracion inicial de Facultades
		facultades = facultadesIni(info)
		# SI contando_externos es True
		if contando_externos == True:
			# Accedemos a la informacion de cada estudiante -> Segun su codigo
			for codigoEst in info:
				# Obteniendo la informacion de cada materia -> Dict
				for materia in info[codigoEst]["materias"]:
					# NO consideramos materias retiradas
					noLaRetiro = laRetiro(materia) # True - False
					# NO consideramos materias con un valor de 0 creditos
					tieneCeroCred = CeroCreditos(materia) # True - False
					# Evaluamos las subcondiciones
					if noLaRetiro and tieneCeroCred:
						# AÑADIR LOS DATOS DE LA MATERIA AL PROMEDIO DE DETERMINADA FACULTAD
						facultad = materia["facultad"]
						for fac in facultades:
							if fac == facultad:
								# Obtenemos la nota y los creditos de cada materia
								nota = materia["nota"]
								creditos = materia["creditos"]
								# Agregamos un dato a la sumatoria del valor1
								facultades[fac][0] = facultades[fac][0] + (nota * creditos)
								# Agregamos un dato a la sumatoria del valor2
								facultades[fac][1] = facultades[fac][1] + creditos
						# ARMAR EL CORREO
						nombres = info[codigoEst]["nombres"]
						apellidos = info[codigoEst]["apellidos"]
						documento = info[codigoEst]["documento"]
						# Armamos el correo
						correo = armarCorreo(nombres, apellidos, documento)
						# Añadimos el correo al conjunto
						correos.add(correo)
		# SI contando_externos es False
		else:
			# Accedemos a la informacion de cada estudiante -> Segun su codigo
			for codigoEst in info:
				# Obteniendo la informacion de cada materia -> Dict
				for materia in info[codigoEst]["materias"]:
					# NO consideramos materias electivas y vacacionales
					matVacacional = cursoVerano(codigoEst) # True - False
					# NO consideramos materias retiradas
					noLaRetiro = laRetiro(materia) # True - False
					# NO consideramos materias con un valor de 0 creditos
					tieneCeroCred = CeroCreditos(materia)  # True - False
					# NO consideramos materias en donde la materia no pertenezca al programa
					# en el que el estudiante esta inscrito.
					programa = info[codigoEst]["programa"]
					pertProg = valMatProg(programa, materia) # True - False
					# Evaluamos las subcondiciones
					if matVacacional and noLaRetiro and tieneCeroCred and pertProg:
						# AÑADIR LOS DATOS DE LA MATERIA AL PROMEDIO DE DETERMINADA FACULTAD
						facultad = materia["facultad"]
						for fac in facultades:
							if fac == facultad:
								# Obtenemos la nota y los creditos de cada materia
								nota = materia["nota"]
								creditos = materia["creditos"]
								# Agregamos un dato a la sumatoria del valor1
								facultades[fac][0] = facultades[fac][0] + (nota * creditos)
								# Agregamos un dato a la sumatoria del valor2
								facultades[fac][1] = facultades[fac][1] + creditos
						# ARMAR EL CORREO
						nombres = info[codigoEst]["nombres"]
						apellidos = info[codigoEst]["apellidos"]
						documento = info[codigoEst]["documento"]
						# Armamos el correo
						correo = armarCorreo(nombres, apellidos, documento)
						# Añadimos el correo al conjunto
						correos.add(correo)
		# Inicializo el diccionario con los promedios de las facultades
		prom = {}
		# Llenamos el diccionario con los promedios para cada facultad
		for i in facultades:
			# Obtnemos el valor de la sumatoria de las notas * los creditos de las materias
			sumatoriaNotasCred = facultades[i][0]
			# Obtenemos el valor de la sumatoria de los creditos de las materias
			sumatoriaCred = facultades[i][1]
			# Asignamos como clave cada facultad
			# Y el valor para cada clave es el promedio de la facultad redondeado a 2 decimales
			prom[i] = round((sumatoriaNotasCred / sumatoriaCred), 2)
		# Convertimos el conjunto a una lista
		correos = list(correos)
		# Ordenamos la lista alfabeticamente
		correos.sort()
		# SALIDA
		# Creamos la tupla (diccionario con facultes y promedios, lista con correos)
		salida = (prom, correos)
		return salida
	except:
		return "Error numérico."

# RETO 4
""" RETO #4
	1. Validar condiciones iniciales
	2. Hallar promedios por facultad -> Segun las condiciones iniciales
	3. Armar correos -> Segun las condiciones iniciales y solo si se tomo algun dato del estudiante
	4. Retornar una salida
"""
# CONDICIONES INICIALES 1
""" Reto 4 -> CONDICIONES INICIALES
	-> Variable de entrada a la funcion -> contando_externos (Tipo Booleano)

	SEGUN LA VARIABLE contando_externos -> Tendremos 2 caminos (2 condiciones)

	--> SI (contando_externos es True / Verdadero):

		CONDICIONES PARA TOMAR LA NOTA EN EL PROMEDIO Y ARMAR EL CORREO
		-> NO consideramos materias retiradas
		-> NO consideramos materias con un valor de 0 creditos

	--> SI (contando_externos es False / Falso):
		CONDICIONES PARA TOMAR LA NOTA EN EL PROMEDIO Y ARMAR EL CORREO
		-> NO consideramos materias electivas y vacacionales
		-> NO consideramos materias retiradas
		-> NO consideramos materias con un valor de 0 creditos
		-> NO consideramos materias en donde la materia no pertenezca al programa
			en el que el estudiante esta inscrito.	
"""
# CONDICIONES INICIALES 2
""" Reto 4 -> CONDICIONES INICIALES ¿Que necesitamos?
	1. NO consideramos materias retiradas:
		clave "retirada" (tipo String) -> Puede ser -> "Si" o "No"
	2. NO consideramos materias con un valor de 0 creditos
		clave "creditos" (tipo Int)
	3. NO consideramos materias electivas y vacacionales
		Codigo del estudiante {periodo de ingreso} (tipo Int)
		{año de ingreso}{periodo de ingreso}{5 numeros adicionales}
		-> Convertir a str
		2017 01 36837
		{pos0:pos3}{pos4:pos5}{pos6:pos11}
		-> {periodo de ingreso} = 05
	4. NO consideramos materias en donde la materia no pertenezca al programa
		en el que el estudiante esta inscrito.	
		clave "programa" (tipo String)
		clave "codigo" (tipo String) -> Solo los primeros caracteres == clave "programa"
		
"""
# PROMEDIOS FACULTAD
""" ¿Como calculamos el promedio para cada facultad?
	
	1. ¿FORMULA?
		( Sumatoria [ NotaMateria * CreditosMateria ] ) / ( Sumatoria (CreditosMateria))
		Ejemplo :
		Mat1 -> Nota: 5.0 -> Creditos: 3
		Mat2 -> Nota: 4.0 -> Creditos: 1
		Mat3 -> Nota: 3.0 -> Creditos: 2
		Mat4 -> Nota: 2.0 -> Creditos: 4
		SUMATORIA [ NotaMateria * CreditosMateria ]
		-> (5.0 * 3) + (4.0 * 1) + (3.0 * 2) + (2.0 * 4) = 33
		SUMATORIA [ CreditosMateria ]
		-> 3 + 1 + 2 + 4 = 10
		PROMEDIO
		-> 33 / 10 = 3.3 
		
	1. CONSIDERACIONES INICIALES ¿QUE NECESITAMOS?
		-> ¿Cuantas facultades hay? ¿Nombre de las faculdades? (Tipo String)
		-> Nota de determinada materia para determinado estudiante (Tipo Float)
		-> Numero de creditos para determinada materia para determinado estudiante (Tipo Int)
		
	2. ¿DONDE GUARDO?
		{'nombreFacultad': [valor1, valor2]}
		valor1 -> Sumatoria [ NotaMateria * CreditosMateria ]
		valor2 -> Sumatoria (CreditosMateria)
		-----------------------------------------
		-> Inicializar el diccionario con las facultades
		-> Obtenemos todas las facultades
		Diccionario vacio {}
		-> Iterar y agregar cada facultad como una clave para el diccionario
		-> Iterar y agregar un arreglo [0, 0] para cada clave del diccionario 
		
	3. ¿COMO ACCEDO A DETERMINADA MATERIA Y CAPTURO SUS DATOS?
		-> Accedemos a la lista de materias de cada estudiante
		-> Obtenemos la nota y los creditos de cada materia
		-> Agregamos un dato a la sumatoria del valor1
		-> Agregamos un dato a la sumatoria del valor2	
			
	4. ¿QUE DEBEMOS ENTREGAR?
		-> Un diccionario: {} dict
			* Clave -> Nombres de las facultades (tipo String)
			* Valor -> Promedio de la favultad (tipo Float) 
				-> Debe estar redondeado a 2 decimales (round (valor, 2))
		-> Debe estar ordenado alfabeticamente 
"""		
# CORREOS
""" ¿Como Armar los correos electronicos de los estudiantes?

	-> Obtener los nombres del estudiante (tipo str)
	-> Obtener los apellidos del estudiante (tipo str)
	-> Obtener el documento del estudiante (tipo int)

	-> Separar los dos nombres (Funcion split)
	-> Separar los dos apellidos (Funcion split)
	SPLIT -> ['', '', .....]
	nombres = "Carlos"
	nombres.split -> ['Carlos']
	[pos0, pos1, pos2, .....]
	a = "abdc"
	valora = a[-2] 

	-> Convertir el documento del estudiante a String

	CONDICIONALES
	-> Si el estudiante tiene dos nombres
		-----------------------------------
		Estructura
		-----------------------------------
		* Primera letra del primer nombre
		* Primera letra del segundo nombre
		* (".") un punto
		* Primer Apellido
		* Dos ultimos numeros del documento
		-----------------------------------
	-> Si el estudiante tiene un nombre
		-----------------------------------
		Estructura
		-----------------------------------
		* Primera letra del primer nombre
		* Primera letra del primer apellido
		* (".") un punto
		* Segundo Apellido
		* Dos ultimos numeros del documento
		-----------------------------------

	-> Convertir todas los caracteres del correo a letras minusculas (funcion lower)
	-> Convertir los caracteres del alfabeto con tilde (á, é, í, ó, ú) a sin tilde 
	   y Convertir el caracter (ñ) a (n)
	   (funcion replace)

"""
# EXTRA CORREOS
""" Lista de salida de correos
	-> Debe ser una lista
	-> No deben existir correos repetidos (conjunto -> set())
	-> Deben estar ordenados alfabeticamente (funcion sort)
"""

#SALIDA
"""SALIDA -> Tupla
( Diccionario con Facultades , Lista con correos )
"""

# Prueba 1:
print(promedio_facultades({
					20170136837:{
								"nombres" : "Jorge Juan",
								"apellidos" : "Moreno, López",
								"documento" : 88481595,
								"programa": "ARQU",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-8218",
												"nota" : 4.49,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-2113",
												"nota" : 2.97,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-5048",
												"nota" : 4.26,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20130225137:{
								"nombres" : "Sara Carolina",
								"apellidos" : "Gómez, Fernández",
								"documento" : 58770043,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-7738",
												"nota" : 3.36,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-9115",
												"nota" : 2.62,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-7698",
												"nota" : 1.59,
												"creditos" : 4,
												"retirada" : "Si",
												},
											]
								},
					20110274333:{
								"nombres" : "Carolina Paula",
								"apellidos" : "Ochoa, López",
								"documento" : 82364435,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7972",
												"nota" : 3.15,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20200116062:{
								"nombres" : "Sara Camila",
								"apellidos" : "Martínez, Gómez",
								"documento" : 40079000,
								"programa" : "DIGR",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-9331",
												"nota" : 4.0,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-3530",
												"nota" : 3.4,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-8548",
												"nota" : 3.1,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-9771",
												"nota" : 3.91,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20100379147:{
								"nombres" : "Jorge Juan",
								"apellidos" : "Romero, López",
								"documento" : 39344921,
								"programa" : "DIGR",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-9511",
												"nota" : 2.38,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-6043",
												"nota" : 3.71,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1720",
												"nota" : 2.5,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20200126220:{
								"nombres" : "Sofia",
								"apellidos" : "Cordoba, Romero",
								"documento" : 90333325,
								"programa" : "IQUI",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-4982",
												"nota" : 4.57,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-4982",
												"nota" : 2.8,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-6947",
												"nota" : 2.47,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-2248",
												"nota" : 3.43,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20130271126:{
								"nombres" : "Gabriela",
								"apellidos" : "Alvarez, García",
								"documento" : 72857337,
								"programa" : "ARQU",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-4963",
												"nota" : 3.15,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-2113",
												"nota" : 3.9,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-1221",
												"nota" : 4.37,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20160219974:{
								"nombres" : "Daniela Sara",
								"apellidos" : "Cuellar, Guitiérrez",
								"documento" : 80398132,
								"programa" : "IIND",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-3557",
												"nota" : 3.91,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-5158",
												"nota" : 3.83,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-7543",
												"nota" : 3.41,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190264705:{
								"nombres" : "Julio Nicolas",
								"apellidos" : "Fernández, Ramírez",
								"documento" : 42697671,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-7888",
												"nota" : 4.68,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20150222512:{
								"nombres" : "Mateo Gabriel",
								"apellidos" : "Niño, Romero",
								"documento" : 12964051,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-3683",
												"nota" : 3.6,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-4014",
												"nota" : 3.15,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-1670",
												"nota" : 4.75,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					}))
# Expected return:
# ({'Arquitectura': 3.81, 'Diseño': 3.58, 'Ingenieria': 3.63, 'Medicina': 3.08}, ['cp.lopez35', 'ds.guitierrez32', 'gg.alvarez37', 'jj.lopez21', 'jj.lopez95', 'jn.ramirez71', 'mg.romero51', 'sc.fernandez43', 'sc.gomez00', 'sr.cordoba25'])
# Mi salida
# ({'Arquitectura': 3.81, 'Diseño': 3.58, 'Ingenieria': 3.63, 'Medicina': 3.08}, ['cp.lopez35', 'ds.guitierrez32', 'gg.alvarez37', 'jj.lopez21', 'jj.lopez95', 'jn.ramirez71', 'mg.romero51', 'sc.fernandez43', 'sc.gomez00', 'sr.cordoba25'])

print(promedio_facultades({
					20170116008:{
								"nombres" : "Sofia Natalia",
								"apellidos" : "Martinez, Alvarez",
								"documento" : 86056697,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-3145",
												"nota" : 3.79,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1882",
												"nota" : 3.02,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-4916",
												"nota" : 3.99,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-9576",
												"nota" : 3.2,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-7401",
												"nota" : 4.08,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20180181912:{
								"nombres" : "Julian Andres",
								"apellidos" : "Fernández, Gómez",
								"documento" : 38203099,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-4822",
												"nota" : 3.99,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-6559",
												"nota" : 3.09,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20170131506:{
								"nombres" : "Laura Camila",
								"apellidos" : "Cuellar, Pérez",
								"documento" : 15755411,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-7857",
												"nota" : 3.19,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1857",
												"nota" : 2.62,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1415",
												"nota" : 2.83,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1720",
												"nota" : 2.58,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20100240601:{
								"nombres" : "Andres Julian",
								"apellidos" : "Ochoa, Romero",
								"documento" : 81959788,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-7472",
												"nota" : 3.6,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-5465",
												"nota" : 2.58,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8357",
												"nota" : 4.69,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-9511",
												"nota" : 2.51,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3379",
												"nota" : 4.31,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20160386484:{
								"nombres" : "Julio",
								"apellidos" : "Sánchez, Fernández",
								"documento" : 95423746,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3008",
												"nota" : 2.83,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3008",
												"nota" : 2.53,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2620",
												"nota" : 4.06,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20190365550:{
								"nombres" : "Catalina Valentina",
								"apellidos" : "García, López",
								"documento" : 88933669,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5278",
												"nota" : 3.45,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1857",
												"nota" : 4.56,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9835",
												"nota" : 3.93,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9442",
												"nota" : 4.46,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20150173830:{
								"nombres" : "Catalina Valentina",
								"apellidos" : "Fernández, Guitiérrez",
								"documento" : 36216549,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-3520",
												"nota" : 2.71,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5596",
												"nota" : 4.7,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6981",
												"nota" : 2.79,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5596",
												"nota" : 2.51,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5161",
												"nota" : 2.36,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20100383099:{
								"nombres" : "Juan Pablo",
								"apellidos" : "Moreno, Cordoba",
								"documento" : 17911136,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-9115",
												"nota" : 4.18,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-6074",
												"nota" : 3.73,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20090198116:{
								"nombres" : "Sofia Gabriela",
								"apellidos" : "Diaz, Moreno",
								"documento" : 62587112,
								"programa" : "ICIV",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-1157",
												"nota" : 2.45,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-7915",
												"nota" : 4.17,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-5962",
												"nota" : 4.49,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190262931:{
								"nombres" : "Paula Natalia",
								"apellidos" : "Torres, Jiménez",
								"documento" : 18534577,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2081",
												"nota" : 4.43,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-8458",
												"nota" : 4.77,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-1258",
												"nota" : 3.15,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190299456:{
								"nombres" : "Natalia Paula",
								"apellidos" : "Moreno, Alvarez",
								"documento" : 89771722,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7322",
												"nota" : 4.27,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-5808",
												"nota" : 3.19,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-4470",
												"nota" : 2.26,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7972",
												"nota" : 3.66,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20150172603:{
								"nombres" : "Catalina Paula",
								"apellidos" : "Pérez, Diaz",
								"documento" : 59641117,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8636",
												"nota" : 4.65,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-1999",
												"nota" : 2.52,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3063",
												"nota" : 2.95,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20160197253:{
								"nombres" : "Julian Mateo",
								"apellidos" : "Jiménez, Fernández",
								"documento" : 41016120,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-9348",
												"nota" : 4.55,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9306",
												"nota" : 2.77,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-1836",
												"nota" : 3.66,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20160174103:{
								"nombres" : "Mateo Julio",
								"apellidos" : "Diaz, López",
								"documento" : 88132707,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-2104",
												"nota" : 4.55,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3425",
												"nota" : 3.98,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-4686",
												"nota" : 4.97,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-9455",
												"nota" : 2.43,
												"creditos" : 0,
												"retirada" : "Si",
												},
											]
								},
					20150384070:{
								"nombres" : "Carolina Natalia",
								"apellidos" : "López, Gómez",
								"documento" : 33424549,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7322",
												"nota" : 2.49,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-4101",
												"nota" : 3.14,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-8021",
												"nota" : 2.97,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7470",
												"nota" : 4.77,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					}, False))
# Expected return:
# ({'Arquitectura': 3.84, 'Diseño': 3.37, 'Historia del Arte': 3.66, 'Ingenieria': 3.88, 'Medicina': 3.45}, ['aj.romero88', 'cn.gomez49', 'cp.diaz17', 'cv.guitierrez49', 'cv.lopez69', 'jf.sanchez46', 'jm.fernandez20', 'jp.cordoba36', 'lc.perez11', 'mj.lopez07', 'np.alvarez22', 'pn.jimenez77', 'sg.moreno12', 'sn.alvarez97'])
# Mi salida
# ({'Arquitectura': 3.84, 'Diseño': 3.37, 'Historia del Arte': 3.66, 'Ingenieria': 3.88, 'Medicina': 3.45}, ['aj.romero88', 'cn.gomez49', 'cp.diaz17', 'cv.guitierrez49', 'cv.lopez69', 'jf.sanchez46', 'jm.fernandez20', 'jp.cordoba36', 'lc.perez11', 'mj.lopez07', 'np.alvarez22', 'pn.jimenez77', 'sg.moreno12', 'sn.alvarez97'])
