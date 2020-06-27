#!/usr/bin/python3
#
# -*- coding: utf-8 -*- 
#
# TITULO: CRONOGRAMA DE GUARDIA DE VENCERT
#
# SUSCERTE: VENCERT
# COORDINACION DE VENCERT
# AUTOR: MIGUEL MARQUEZ 
# CARACAS, JUNIO DEL 2020
#
# cronoguardvencert.py V 1.0
#
# DESCRIPCION:
# 
# 	Automatizacion de  la  elaboracion  del  documento   en
#  PDF  del  control  de guardia  para  el personal  de vencert
#  durante el periodo y el personal especificado por el usuario

# NOTA: rango de meses, ¿ lista ? del 1..
# NOTA: algoritmo de rango de meses debe definir si es par o impar y activar un swiche ?


import calendar
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth

############################ INICIO DE LA CLASE PAPEL #####################################

class Papel(object): # CLASE ABSTRACTA 

	ancho, h = A4
	#switche= True

	def __init__(self, pPapel, pTitulo):
		self.altura= self.h - pPapel
		self.tamanioPapel= self.ancho, self.altura
		self.titulo= pTitulo #"CONTROL_DE_GUARDIA_2020.pdf"
		self.pdf= None

	def iniciarPDF(self):
		print("tamaño del papel: " + str(self.tamanioPapel))
		print(self.titulo)
		self.pdf = canvas.Canvas(self.titulo, pagesize=self.tamanioPapel)
		self.pdf.setTitle(self.titulo)

	def dibujarCintillo(self):
	
		anchoImg= 550
		self.pdf.drawImage("cintillo.jpg", (self.ancho - anchoImg)/2, self.altura - 50, width=anchoImg, height=40)

	def escribirTitulo(self):
		
		titulo= self.titulo.replace('_', ' ')
		titulo= titulo.replace('.pdf', '')
		tamanioTexto= self.pdf.stringWidth(titulo, "Helvetica-Bold", 20)

		ttl= self.pdf.beginText((self.ancho-tamanioTexto)/2, self.altura - 70)
		ttl.setFont("Helvetica-Bold", 20)
		ttl.textLine(titulo)

		self.pdf.drawText(ttl)


	def escribirPieDePagina(self, texto, alto):

		tamanioTexto= self.pdf.stringWidth(texto, "Helvetica", 10)

		
		pie= self.pdf.beginText((self.ancho-tamanioTexto)/2, self.altura - alto)
		pie.setFont("Helvetica", 10)
		pie.textLine(texto)

		self.pdf.drawText(pie)

	def guardarPDF(self):
		self.pdf.showPage()

	def finalizarPDF(self):
		self.pdf.save()

############################### FIN DE LA CLASE PAPEL #####################################

##################################### BORRAR ##############################################
'''
class PruebaRectangulo(Papel): 

	def __init__(self, pPapel, pTitulo, rAncho, rLargo): # 	  constructor clase PruebaRectangulo
		Papel.__init__(self, pPapel, pTitulo ) #  constructor clase Papel

		self.recAncho= rAncho #pasar a clase tabla
		self.recLargo= rLargo #pasar a clase tabla

	def dibujarRectangulo(self):
		self.pdf.rect((self.ancho - self.recAncho)/2, self.altura-460, self.recAncho, self.recLargo)

	def dibujarUnaLinea(self, aux):
		#self.pdf.line(0, self.altura-aux, self.ancho, self.altura-aux)
		self.pdf.line(573, 0, 573, self.altura)

	def dibujarUnrectangulo(self):
		mitadRecLargo= self.recLargo / 2 # 190
		#nuevaAltura=  self.altura-(mitadRecLargo + 80) #270 mitad superior
		#nuevaAltura= nuevaAltura + mitadRecLargo / 2 # 270 + 95 = 365

		#print("esta es la nueva altura: " + str(nuevaAltura))

		self.pdf.rect((self.ancho - self.recAncho)/2, self.altura-365, self.recAncho, mitadRecLargo) #nuevaAltura = 241.88

	def dibujarDosRectangulos(self): 

		mitadRecLargo= self.recLargo / 2 # 190
		
		self.pdf.rect((self.ancho - self.recAncho)/2, self.altura-(mitadRecLargo + 80), self.recAncho, mitadRecLargo) #nuevaAltura = 241.88
		self.pdf.rect((self.ancho - self.recAncho)/2, self.altura-460, self.recAncho, mitadRecLargo) #nuevaAltura = 241.88

	def decidirCantidadRectangulos(self, llave):#si el numero de meses es par o impar y si el numero de meses es mayor a uno o menor a uno

		if(llave > 1):

			self.dibujarDosRectangulos()

		else:
			self.dibujarUnrectangulo()
'''
##################################### BORRAR ##############################################

############################ INICIO DE LA CLASE TABLA #####################################

class Tabla(Papel):# Hereda de la clase Papel

	def __init__(self, pPapel, pTitulo, rAncho, rLargo, tFilas, tColumnas ): # 	  constructor clase PruebaRectangulo
		Papel.__init__(self, pPapel, pTitulo ) #  constructor clase Papel

		self.recAncho= rAncho #ancho tabla
		self.recLargo= rLargo #largo tabla
		self.filasLista= list()# lista vacia del calendario
		self.columnasLista= list()# lista vacia del calendario
		self.filasListaNombres= list() # lista vacia del personal
		self.columnasListaNombres= list()# lista vacia del personal
		self.tamanioFilas= tFilas
		self.tamanioColumnas= tColumnas
		#self.inicioVertical= self.altura - 80
		#self.inicioHorizontal= (self.ancho - self.recAncho)/2
		#self.inicioVertical= 80
		#self.finalVertical= 460
		#self.inicioHorizontal= 27.635
		#self.finalHorizontal= 573.635

	def dibujarTabla(self, puntero): # crear argumento llamado puntero para definir la ubicacion de la tabla

		filasLista= list()# lista vacia del calendario
		columnasLista= list()# lista vacia del calendario
		filasListaNombres= list() # lista vacia del personal
		columnasListaNombres= list()# lista vacia del personal

		iVertical= self.altura - puntero # inicio vertical /  argumento puntero
		iHorizontal= ( self.ancho - self.recAncho ) / 2 # inicio horizontal
		fVertical=  self.recLargo/2 # 190 final vertical
		fHorizontal= self.recAncho # 550 final horizontal

#--------------------------------------------------------------------------------------------
# INICIO CICLOS QUE OBLIGAN EL CRECIMIENTO DINAMICO DE LAS GRILLAS CONSERVANDO EL TAMAÑO DE LA TABLA
		
		contFilas= self.tamanioFilas
		sumaVerticales= iVertical
		while(contFilas > 0):
			
			resto=  fVertical / contFilas
			fVertical-= resto # el resto de la division es el relleno
			#sumaVerticales-= resto
			if( contFilas < self.tamanioFilas):
				columnasListaNombres.append(sumaVerticales)#SEGUNDA TABLA  BORRAR ?
			columnasLista.append(sumaVerticales)
			sumaVerticales-= resto #comentar esta linea para redefinir la posicion
			contFilas-= 1
		columnasListaNombres.append(sumaVerticales)
		columnasLista.append(sumaVerticales)

		contColumnas= self.tamanioColumnas
		sumaHorizontales= iHorizontal
		while( contColumnas > 0 ): 

			resto = fHorizontal / contColumnas
			fHorizontal-= resto # el resto de la division es el relleno
			if( contColumnas >= (self.tamanioColumnas - 1)):# SEGUNDA TABLA  BORRAR ?
				filasListaNombres.append(sumaHorizontales) # SEGUNDA TABLA  BORRAR ?
			sumaHorizontales+= resto
			filasLista.append(sumaHorizontales) # llenar lista del calendario
			#sumaHorizontales+= resto #comentar esta linea para redefinir la posicion
			contColumnas-= 1
		filasLista.append(sumaHorizontales)

# FIN CICLOS QUE OBLIGAN EL CRECIMIENTO DINAMICO DE LAS GRILLAS CONSERVANDO EL TAMAÑO DE LA TABLA		
#--------------------------------------------------------------------------------------------
		
		self.pdf.grid(filasListaNombres, columnasListaNombres)# construye tabla vacia para el personal #SEGUNDA TABLA  BORRAR ?
		self.pdf.grid(filasLista, columnasLista)# construye tabla vacia para el calendario
		
		#debugear
		#print("FILA LISTA: "+str(self.filasLista))
		#print("FILA LISTA NOMBRES: "+str(self.filasListaNombres))
		#print("COLUMNAS LISTA: "+str(self.columnasLista))
		#print("COLUMNAS LISTA NOMBRES: "+str(self.columnasListaNombres))
		#debugear

		self.filasLista= filasLista
		self.columnasLista= columnasLista
		self.filasListaNombres= filasListaNombres
		self.columnasListaNombres= columnasListaNombres

		#self.limpiarListas() #subrutina que limpia las listas

	
	def dibujarUnaTabla(self):
		self.dibujarTabla(175) # (380 / 4) = (95 + 80) = 172 un cuarto superior

	def dibujarDosTabla(self):
		self.dibujarTabla(80-0) #  80 desde el inicio
		self.dibujarTabla(270+0) # (380 / 2)  =  190 + 80 mitad
	'''
	def limpiarListas(self):
		del self.filasLista[:]	        # borrar lista 
		del self.columnasLista[:]	# borrar lista
		del self.filasListaNombres[:]	# borrar lista
		del self.columnasListaNombres[:]# borrar lista
	'''
############################### FIN DE LA CLASE TABLA #####################################

'''
class DibujarTabla(Papel):

	def __init__(self, pPapel, pTitulo): # constructor clase dibujar tabla
	
	Papel.__init__(self, pPapel, pTitulo): # constructor clase papel
'''	

	#ojo las tablas deben ser polimorficas adaptarse a cualquier tamaño siguiendo una regla especifica

		
class Calendario:
	
	# nota:
	# meses por rango de numeros del mes
	# ¿ meses por rango de nombre del mes ?

	def __init__(self, cAnio, cMes): # constructor 

		if(cMes >= 1 and cMes <= 12):

			self.anio= cAnio
	
			if(cMes > 1):
				self.mesAnterior= cMes - 1
			else:
				self.mesAnterior= 12

			self.mesActual= cMes
		
			if(cMes < 12 ):
				self.mesSiguiente= cMes + 1
			else:
				self.mesSiguiente= 1
			
		
			self.meses=['ENERO',
				   'FEBRERO',
				   'MARZO',
				   'ABRIL',
				   'MAYO',
				   'JUNIO',
				   'JULIO',
				   'AGOSTO',
				   'SEPTIEMBRE',
				   'OCTUBRE',
				   'NOVIEMBRE',
				   'DICIEMBRE']

			self.dias= ['Lunes', 
				    'Martes', 
				    'Miercoles', 
				    'Jueves', 
				    'Viernes', 
				    'Sabado', 
				    'Domingo']
		else:
			print("ERROR!!! MES FUERA DE RANGO!")

	def obtenerDias():
		return self.dias

	def obtenerNombreMesAnterior(self):
		return self.meses[self.mesAnterior-1]

	def obtenerNombreMesActual(self):
		return self.meses[self.mesActual-1]

	def obternerNombreMesSiguiente(self):
		return self.meses[self.mesSiguiente-1]
	
	def obtenerCalendarioMesAnterior(self):

		if( self.mesAnterior ==  12 ):

			anioAnterior= self.anio - 1
		else:
			anioAnterior= self.anio

		calendario = calendar.LocaleTextCalendar(locale='es_ES')
		mesAnterior = calendario.monthdayscalendar(anioAnterior, self.mesAnterior) 
	
		return mesAnterior

	def obtenerCalendarioMesActual(self):

		calendario = calendar.LocaleTextCalendar(locale='es_ES')
		mesActual = calendario.monthdayscalendar(self.anio, self.mesActual)
	
		return mesActual

	def obtenerCalendarioMesSiguiente(self):
	
		if(self.mesSiguiente == 1):

			anioSiguiente= self.anio + 1
		else:
			anioSiguiente= self.anio

		calendario = calendar.LocaleTextCalendar(locale='es_ES')
		mesSiguiente = calendario.monthdayscalendar(anioSiguiente, self.mesSiguiente) 
	
		return mesSiguiente

############################ INICIO DE LA CLASE CONTROL #####################################
class ControlDeGuardia(Tabla): # Hereda de la clase Tabla

	def __init__(self, pPapel, pTitulo, rAncho, rLargo, tFilas, tColumnas, cPersonal): # 	  constructor clase PruebaRectangulo
		Tabla.__init__(self, pPapel, pTitulo, rAncho, rLargo, tFilas, tColumnas ) #  constructor clase Papel
	
		self.personal= cPersonal # lista del personal


	#def redefinirTamanioTexto

	def hubicarHorizontalLetras(self, posicionX1, posicionX2, tamanioDelTexto):

		
		anchoDeLaGrilla= posicionX1 - posicionX2

		if(anchoDeLaGrilla < 0):
			anchoDeLaGrilla*= -1

		posMenor= posicionX2
		if(posicionX1 < posMenor):
			posMenor= posicionX1

		return (posMenor + (anchoDeLaGrilla - tamanioDelTexto)/2)

	
	def hubicarVerticalLetras(self, posicionY1, posicionY2, tamanioDelTexto):

		altoDeLaGrilla= posicionY1 - posicionY2

		if(altoDeLaGrilla < 0):
			altoDeLaGrilla *= -1

		posMayor= posicionY1
		if(posicionY2 > posMayor):
			posMayor= posicionY2

		return (posMayor - (altoDeLaGrilla + (tamanioDelTexto-(tamanioDelTexto/3)))/2) #la longitud de la fuente menos un tercio de su longitud ejemp: 12-12/3= 12-4= 8

		
		'''

		if(posicionX > posicionY):

			posMayor= posicionX 
			posMenor= posicionY
		else:
			posMayor= posicionY
			posMeNor= posicionX 


		anchoDeLaGrilla= posMayor - posMenor
		'''

	def escribirElPersonalEnLaTabla(self):

		cont= 0
		tamanioFuente= 12

		for i in range(0, self.tamanioFilas):

			if(i+1 != self.tamanioFilas):
				
				tamanioDelTexto= self.pdf.stringWidth(personal[cont].upper(), "Helvetica-Bold", tamanioFuente)

				print(tamanioDelTexto)
				'''
				DEBUGGEAR
				print("TEXTO")
				print(tamanioDelTexto)
				print("FILAS")
				print(self.filasListaNombres[0])
				print(self.filasListaNombres[1])
				print("COLUMNAS")
				print(self.columnasListaNombres[i])
				print(self.columnasListaNombres[i+1])
				DEBUGGEAR
				'''
				xlista= self.hubicarHorizontalLetras(self.filasListaNombres[0], self.filasListaNombres[1], tamanioDelTexto)
				ylista= self.hubicarVerticalLetras(self.columnasListaNombres[i], self.columnasListaNombres[i+1], tamanioFuente)
				texto= self.pdf.beginText(xlista , ylista)
				texto.setFont("Helvetica-Bold", tamanioFuente)
				texto.textLine(str(personal[cont].upper()))
				self.pdf.drawText(texto)
			else:
				break

			#c.drawString( , yLista2[i]-16 , str(personal[cont]))#borrar

			if( cont == len(personal)-1):
				cont=0
			else:
				cont+=1

	#def escribirElCalendarioEnLaTabla(self):

	#def esCribirElCalendario(self):


	# atributos:

	# operaciones:

	#def __init__(self): # constructor
		#self.
		#self.
		#self.
		#self.

	#def dibujarTablas(self ):
	
	#def escribirCalendario(self):

	#def obtenerCalendario(self):
	
	#def enviarCalendario(self):



############################ FIN DE LA CLASE CONTROL ########################################

if __name__ == '__main__': # PUNTO DE ENTRADA PRINCIPAL

	
	personal= ['Miguel', 'Eduardo', 'Brian', 'Jean', 'Cesar']# variables de clase (atributos)
	meses=1 #lista de un mes simulada
	anio= 2020


	esteCalendario= Calendario(anio, meses)

	numeroFilas= len(esteCalendario.obtenerCalendarioMesActual()) + 1 # el numero de filas puede variar dependiendo de las semanas + 1 fila del nombre del mes
	numeroColumas= 8 # numero columa constante 8 = 7 columnas de dias + 1 columna del personal

	esteControlDeGuardia= ControlDeGuardia(330,"CONTROL_DE_GUARDIA_"+str(anio)+".pdf", 550, 380, numeroFilas, numeroColumas, personal)  # sacar numero Filas y numero Columnas y colocarlo en funcion ?

	esteControlDeGuardia.iniciarPDF()
	esteControlDeGuardia.dibujarCintillo()
	esteControlDeGuardia.escribirTitulo()
	esteControlDeGuardia.dibujarUnaTabla()
	esteControlDeGuardia.escribirElPersonalEnLaTabla()
	esteControlDeGuardia.escribirPieDePagina("Av. Andres Bello, Torre BFC, Piso 13,  "+ 
				  	      "Sector Guaicaipuro, Caracas - Venezuela",480)
	esteControlDeGuardia.escribirPieDePagina("Tlfs +58-212 5785674–Fax +58 212 5724932",495)
	esteControlDeGuardia.guardarPDF()
	esteControlDeGuardia.finalizarPDF()
		
		
	

#aca debo definir le bucle para el rango de meses y todas esas cosas
	
	'''

	esteCalendario= Calendario(2020, 1) # rango de meses ¿ lista ?

	
	
	print(esteCalendario.obtenerNombreMesAnterior())
	print(esteCalendario.obtenerCalendarioMesAnterior())
	print(esteCalendario.obtenerNombreMesActual())
	print(esteCalendario.obtenerCalendarioMesActual())
	print(esteCalendario.obternerNombreMesSiguiente())
	print(esteCalendario.obtenerCalendarioMesSiguiente())
	
	'''


#################################################################################################################
	'''
	estaTabla= Tabla(330,"CONTROL_DE_GUARDIA_2020.pdf", 550, 380, 7, 8)


	estaTabla.iniciarPDF()
	estaTabla.dibujarCintillo()
	estaTabla.escribirTitulo()

	
	#estaTabla.decidirCantidadRectangulos(2)
	estaTabla.dibujarUnaTabla()


	estaTabla.escribirPieDePagina("Av. Andres Bello, Torre BFC, Piso 13,  "+ 
				  	      "Sector Guaicaipuro, Caracas - Venezuela",480)
	estaTabla.escribirPieDePagina("Tlfs +58-212 5785674–Fax +58 212 5724932",495)
	estaTabla.guardarPDF()
	estaTabla.finalizarPDF()
	'''
#################################################################################################################
	'''
	esteRectangulo= PruebaRectangulo(330,"CONTROL_DE_GUARDIA_2020.pdf", 550, 380)
	esteRectangulo.iniciarPDF()

	esteRectangulo.dibujarCintillo()
	esteRectangulo.escribirTitulo()
	esteRectangulo.dibujarUnaLinea(80)
	#esteRectangulo.dibujarRectangulo()
	#esteRectangulo.dibujarUnrectangulo()
	#esteRectangulo.dibujarDosrectangulos()
	esteRectangulo.decidirCantidadRectangulos(1)
	esteRectangulo.escribirPieDePagina("Av. Andres Bello, Torre BFC, Piso 13,  "+ 
				  	      "Sector Guaicaipuro, Caracas - Venezuela",480)
	esteRectangulo.escribirPieDePagina("Tlfs +58-212 5785674–Fax +58 212 5724932",495)
	esteRectangulo.guardarPDF()

	esteRectangulo.finalizarPDF()
	'''
#################################################################################################################
	'''
	estePapel= Papel(330,"CONTROL_DE_GUARDIA_2020.pdf")
	estePapel.iniciarPDF()


	#DibujarRectangulo

	for i in range(1,5):
		estePapel.dibujarCintillo()
		estePapel.escribirTitulo()
		estePapel.escribirPieDePagina("Av. Andres Bello, Torre BFC, Piso 13,  "+ 
				  	      "Sector Guaicaipuro, Caracas - Venezuela",480)
		estePapel.escribirPieDePagina("Tlfs +58-212 5785674–Fax +58 212 5724932",495)
		estePapel.guardarPDF()
#///////////////////////////////////////////


	
	estePapel.finalizarPDF()

	'''
