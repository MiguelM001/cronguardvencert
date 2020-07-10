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
import os
import sys
import time
import calendar
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

############################ INICIO DE LA CLASE PAPEL #####################################

class Papel(object): # CLASE ABSTRACTA 

	ancho, h = A4

	def __init__(self, pPapel, pTitulo):
		self.altura= self.h - pPapel
		self.tamanioPapel= self.ancho, self.altura
		self.titulo= pTitulo #"CONTROL_DE_GUARDIA_2020.pdf"
		self.pdf= None

	def iniciarPDF(self):
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
		pie.setFillColor(HexColor(0x000000))
		pie.setFont("Helvetica", 10)
		pie.textLine(texto)

		self.pdf.drawText(pie)

	def selloDelPrograma(self):

		sello= self.pdf.beginText(22.635, self.altura - 495)
		sello.setFillColor(HexColor(0xcccccc))
		sello.setFont("Helvetica-Bold", 12)
		sello.textLine("cronoguardvencert.py")

		self.pdf.drawText(sello)

	def guardarPDF(self):
		self.pdf.showPage()

	def finalizarPDF(self):
		self.pdf.save()

############################### FIN DE LA CLASE PAPEL #####################################
############################ INICIO DE LA CLASE TABLA #####################################

class Tabla(Papel):# Hereda de la clase Papel

	def __init__(self, pPapel, pTitulo, rAncho, rLargo ): # 	  constructor clase PruebaRectangulo
		Papel.__init__(self, pPapel, pTitulo ) #  constructor clase Papel

		self.recAncho= rAncho #ancho tabla
		self.recLargo= rLargo #largo tabla
		self.filasLista= list()# lista vacia del calendario
		self.columnasLista= list()# lista vacia del calendario
		self.filasListaNombres= list() # lista vacia del personal
		self.columnasListaNombres= list()# lista vacia del personal

		self.tamanioFilas= 0 
		self.tamanioColumnas= 0 

	def enviarNumeroDeFilas(self, tFilas):
		self.tamanioFilas= tFilas

		
	def enviarNumeroDeColumnas(self, tColumnas):
		self.tamanioColumnas= tColumnas

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

			contColumnas-= 1


# FIN CICLOS QUE OBLIGAN EL CRECIMIENTO DINAMICO DE LAS GRILLAS CONSERVANDO EL TAMAÑO DE LA TABLA		
#--------------------------------------------------------------------------------------------
		
		self.pdf.grid(filasListaNombres, columnasListaNombres)# construye tabla vacia para el personal #SEGUNDA TABLA  BORRAR ?
		self.pdf.grid(filasLista, columnasLista)# construye tabla vacia para el calendario
		self.filasLista= filasLista
		self.columnasLista= columnasLista
		self.filasListaNombres= filasListaNombres
		self.columnasListaNombres= columnasListaNombres
	
	def dibujarUnaTabla(self):
		self.dibujarTabla(175) # (380 / 4) = (95 + 80) = 172 un cuarto superior
	
	def limpiarListas(self):
		del self.filasLista[:]	        # borrar lista 
		del self.columnasLista[:]	# borrar lista
		del self.filasListaNombres[:]	# borrar lista
		del self.columnasListaNombres[:]# borrar lista
	
############################### FIN DE LA CLASE TABLA #####################################
########################## INICIO DE LA CLASE CALENDARIO ##################################
class Calendario:

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

	def obtenerDias(self):
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
############################ FIN DE LA CLASE CALENDARIO #####################################
############################ INICIO DE LA CLASE CONTROL #####################################
class ControlDeGuardia(Tabla): # Hereda de la clase Tabla

	def __init__(self, pPapel, pTitulo, rAncho, rLargo, cPersonal): # 	  constructor clase PruebaRectangulo
		Tabla.__init__(self, pPapel, pTitulo, rAncho, rLargo ) #  constructor clase Papel
	
		self.personal= cPersonal # lista del personal
		self.contPersonal= 0


	def redefinirTamanioHorizontalTexto(self, posicionX1, posicionX2, tamanioDelTexto):

		valor= False

		anchoDeLaGrilla= posicionX1 - posicionX2 #ancho de la grilla

		if(anchoDeLaGrilla < 0):
			anchoDeLaGrilla*= -1

		if(anchoDeLaGrilla <= tamanioDelTexto + 6 ): # 6 es el espacio entre el texto y la grilla
			valor= True

		return valor
			#tamanio del texto disminuye

	#NOTA: ES IMPORTANTE LA FUNCION DE REDEFINIR TAMAÑO POR LA PROPIEDAD POLIMORFICA DE LA TABLA

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

	def escribirElPersonalEnLaTabla(self):

		for i in range(0, self.tamanioFilas):

			if(i+1 != self.tamanioFilas):

				tamanioFuente= 12
				tamanioDelTexto= self.pdf.stringWidth(self.personal[self.contPersonal].upper(), "Helvetica-Bold", tamanioFuente)
				# BUCLE REDEFINE EL TAMAÑO DEL TEXTO HORIZONTALMENTE
				while( self.redefinirTamanioHorizontalTexto( self.filasListaNombres[0], self.filasListaNombres[1], tamanioDelTexto ) ):
					tamanioFuente-= 1
					tamanioDelTexto= self.pdf.stringWidth(self.personal[self.contPersonal].upper(), "Helvetica-Bold", tamanioFuente)
				
				xlista= self.hubicarHorizontalLetras(self.filasListaNombres[0], self.filasListaNombres[1], tamanioDelTexto)
				ylista= self.hubicarVerticalLetras(self.columnasListaNombres[i], self.columnasListaNombres[i+1], tamanioFuente)
				texto= self.pdf.beginText(xlista , ylista)
				texto.setFillColor(HexColor(0xcc0000))
				texto.setFont("Helvetica-Bold", tamanioFuente)
				texto.textLine(str(self.personal[self.contPersonal].upper()))
				self.pdf.drawText(texto)
			else:
				break


			if( self.contPersonal == len(self.personal)-1):
				self.contPersonal=0
			else:
				self.contPersonal+=1

	def escribirNombreMesEnLaTabla(self, nombreMesActual): 

		resta= self.columnasListaNombres[2] - self.columnasListaNombres[3]

		if(resta < 0 ):
			resta *= -1

		suma= self.columnasListaNombres[0] + resta 

		tamanioFuente= 50
		tamanioDelTexto= self.pdf.stringWidth(nombreMesActual, "Helvetica-Bold", tamanioFuente)
		
		while( self.redefinirTamanioHorizontalTexto( self.filasListaNombres[0], self.filasListaNombres[1], tamanioDelTexto ) ):
					tamanioFuente-= 1
					tamanioDelTexto= self.pdf.stringWidth(nombreMesActual.upper(), "Helvetica-Bold", tamanioFuente)
		

		xlista= self.hubicarHorizontalLetras(self.filasListaNombres[0], self.filasListaNombres[1], tamanioDelTexto)
		ylista= self.hubicarVerticalLetras(suma, self.columnasListaNombres[0], tamanioFuente)
		texto= self.pdf.beginText(xlista , ylista)
		texto.setFillColor(HexColor(0x9faec8))
		texto.setFont("Helvetica-Bold", tamanioFuente)
		texto.textLine(str(nombreMesActual.upper()))
		self.pdf.drawText(texto)

	def escribirDiasEnlaTabla(self, dias):

		cont= 0
		for i in range(0, len(dias)):

			tamanioFuente= 12
			tamanioDelTexto= self.pdf.stringWidth(dias[cont], "Helvetica-Bold", tamanioFuente)
			while( self.redefinirTamanioHorizontalTexto( self.filasLista[i], self.filasLista[i+1], tamanioDelTexto ) ):
				tamanioFuente-= 1
				tamanioDelTexto= self.pdf.stringWidth(dias[cont], "Helvetica-Bold", tamanioFuente)

			xlista= self.hubicarHorizontalLetras(self.filasLista[i], self.filasLista[i+1], tamanioDelTexto)#columas
			ylista= self.hubicarVerticalLetras(self.columnasLista[0], self.columnasLista[1], tamanioFuente) #filas
			texto= self.pdf.beginText(xlista , ylista)
			texto.setFillColor(HexColor(0x000000))
			texto.setFont("Helvetica-Bold", tamanioFuente)
			texto.textLine(str(dias[cont]))
			self.pdf.drawText(texto)

			cont+=1
		
		self.columnasLista.pop(0)# se elimina la primera fila

	def escribirElCalendarioEnLaTabla(self, mesActual,  mesAnterior, mesSiguiente, dias):

		cont1=0
		for i in range(0, len(dias)):
			cont2=0
			for j in range(0, len(self.columnasLista)-1):

				if(mesActual[cont2][cont1] != 0):# condicion impide escritura de ceros
					cadena= mesActual[cont2][cont1]
					fuente= "Helvetica"
					tamanio= 16
					hexaColor= 0x272727

				if(j == 0):#  sustituye los ceros de las primeras filas del mes , por el nombre del mes anterior
					if(mesActual[cont2][cont1] == 0):
						cadena=  mesAnterior[len(mesAnterior)-1][cont1]
						fuente= "Helvetica-Bold"
						tamanio= 16
						hexaColor= 0x9faec8

				if(j == len(self.columnasLista)-2):#  sustituye los ceros de las ultimas filas del mes , por el nombre del siguiente mes
					if(mesActual[cont2][cont1] == 0):
						cadena= mesSiguiente[0][cont1]
						fuente= "Helvetica-Bold"
						tamanio= 16
						hexaColor= 0x9faec8

						if(cont1 == len(mesActual[len(mesActual)-1])-1):
							if(mesActual[len(mesActual)-1][len(mesActual[len(mesActual)-1])-1] == 0):
								self.contPersonal -= 1
						
				
				
				tamanioFuente= tamanio
				tamanioDelTexto= self.pdf.stringWidth(str(cadena), fuente, tamanioFuente)
				
				while( self.redefinirTamanioHorizontalTexto( self.filasLista[i], self.filasLista[i+1], tamanioDelTexto ) ):
					tamanioFuente-= 1
					tamanioDelTexto= self.pdf.stringWidth(str(cadena), fuente, tamanioFuente)
				

				xlista= self.hubicarHorizontalLetras(self.filasLista[i], self.filasLista[i+1], tamanioDelTexto)#columas
				ylista= self.hubicarVerticalLetras(self.columnasLista[j], self.columnasLista[j+1], tamanioFuente) #filas
				texto= self.pdf.beginText(xlista , ylista)
				texto.setFillColor(HexColor(hexaColor))
				texto.setFont(fuente, tamanioFuente)
				texto.textLine(str(cadena))
				self.pdf.drawText(texto)

				cont2+=1

			cont1+=1
			
############################ FIN DE LA CLASE CONTROL ########################################
#################### INICIO DE LA CLASE INTERFAZ DE USUARIO #################################

class InterfazDeUsuario:


	def __init__(self, argv):

		self.argv= argv

		self.nombres= list()
		self.numero= list()
		self.unAnio= 0


	def clasificarValores(self):

		nombres= self.nombres
		numero= self.numero
		unAnio= self.unAnio

		for i in range(0,len(sys.argv)):

	
			if(sys.argv[i] == "-p" or sys.argv[i] == "--personal"):

				palabra=''
				for letra in sys.argv[i+1]:
			
			
					if(letra != ','):

						palabra+=letra
					else:
						nombres.append(palabra)
						palabra=''
		
				nombres.append(palabra)
		
			digito=''

			if(sys.argv[i] == "-m" or sys.argv[i] == "--meses"):

				if sys.argv[i+1] != 1:
	
					for num in sys.argv[i+1]:

						if(num != '-'):

							digito+= num
						else: 
							numero.append(int(digito))
							digito=''

					numero.append(int(digito))

				else:
					numero.append(int(num))

	
			if(sys.argv[i] == "-a" or sys.argv[i] == "--anio"):
				unAnio= int(sys.argv[i+1])
	

			if sys.argv[i] == "-h" or sys.argv[i] == "--ayuda":
				self.desplegarAyuda()

		#print(nombres)
		#print(numero)
		#print(unAnio)

		self.nombres= nombres
		self.numero= numero
		self.unAnio= unAnio

	def obtenerLosNombres(self):
		return self.nombres

	
	def ObtenerRangoDeMeses(self):

		lista= list()
		
		if(len(self.numero) > 1):

			for i in range(self.numero[0], self.numero[1]):
				lista.append(i)
			lista.append(i+1)

			return lista

		else:
			return self.numero
	

	def obtnerElAnio(self):
		return self.unAnio

				
	def desplegarAyuda(self):
		print()
		print("Cronograma de Guardia Automatizado de VenCERT V1.0:")
		print()
		print("\tEjemplo de uso: python3 cronguardvencert.py -p miguel,cesar,eduardo,brian,jean -m 7-12 -a 2020")
		print("\t\t\tpython3 cronguardvencert.py --personal miguel,cesar,eduardo,brian,jean --meses 7-12 --anio 2020")
		print()
		print("Comandos:")
		print()
		print("-p --personal\tintruduzca el orden del personal en la tabla, separado solo por coma (,) ")
		print("-m --meses\tIntruduzca el rango de los meses en secuencia ascendente jemplo: 1-12,  separado por el signo (-)")
		print("-a --anio\tintroduzca el anio actual, en un entero de cuatro digitos")
		print("-h --ayuda\tComando para dezplegar la ayuda")
		print()



	# EN CONSTRUCCION
###################### FIN DE LA CLASE INTERFAZ DE USUARIO ##################################
# INICIO DE MAIN
if __name__ == '__main__': # PUNTO DE ENTRADA PRINCIPAL

	sys.argv.pop(0)

	estaInterfazDeUsuario= InterfazDeUsuario(sys.argv)
	estaInterfazDeUsuario.clasificarValores()
	if(not sys.argv):
		estaInterfazDeUsuario.desplegarAyuda()

	personal= estaInterfazDeUsuario.obtenerLosNombres()
	meses= estaInterfazDeUsuario.ObtenerRangoDeMeses()
	anio= estaInterfazDeUsuario.obtnerElAnio()

	#INPUTS
	#personal= ['Cesar','Miguel','Eduardo', 'Brian', 'Jean']# variables de clase (atributos)
	#personal= ['Cesar','Miguel','Eduardo', 'Brian', 'Jean']# variables de clase (atributos)
	#meses= [7,8,9,10,11,12]
	#anio= 2020
	#INPUTS

	if(personal != None and meses != None and anio != 0):
	
		#INSTANCIACION DE LA CLASE ControlDeGuardia
		titulo= "CONTROL_DE_GUARDIA_"+str(anio)+".pdf"
		esteControlDeGuardia= ControlDeGuardia(330,titulo, 550, 380, personal)  # sacar numero Filas y numero Columnas y colocarlo en funcion ?
		esteControlDeGuardia.iniciarPDF()
		#INSTANCIACION DE LA CLASE ControlDeGuardia

		contPaginas= len(meses) # contador de paginas
		indexMeses= 0 # indice para la lista meses[]

		while(contPaginas >= 1):
			#INSTANCIACION DE LA CLASE ControlDeGuardia
			esteControlDeGuardia.dibujarCintillo()
			esteControlDeGuardia.escribirTitulo()
			#INSTANCIACION DE LA CLASE ControlDeGuardia
			contTablas= 2

			if(contPaginas != 1):
				switche= True

				while(contTablas >= 1):

					if(switche == True):
						posicion= (80 - 3.5 )
						switche= False
					else: 
						posicion= (270 + 5.5)
						switche= True

					#INSTANCIACION DE LA CLASE CALENDARIO
					esteCalendario= Calendario(anio, meses[indexMeses])
					mesAnterior= esteCalendario.obtenerCalendarioMesAnterior()
					mesActual= esteCalendario.obtenerCalendarioMesActual()
					mesSiguiente= esteCalendario.obtenerCalendarioMesSiguiente()
					nombreMesActual= esteCalendario.obtenerNombreMesActual()
					dias= esteCalendario.obtenerDias()
					numeroFilas= len(esteCalendario.obtenerCalendarioMesActual()) + 1 # el numero de filas puede variar dependiendo de las semanas + 1 fila del nombre del mes
					numeroColumas= 8 # numero columa constante 8 = 7 columnas de dias + 1 columna del personal
					#INSTANCIACION DE LA CLASE CALENDARIO
					#INSTANCIACION DE LA CLASE ControlDeGuardia
					esteControlDeGuardia.enviarNumeroDeFilas(numeroFilas)
					esteControlDeGuardia.enviarNumeroDeColumnas(numeroColumas)
					esteControlDeGuardia.dibujarTabla(posicion)
					esteControlDeGuardia.escribirNombreMesEnLaTabla(nombreMesActual)
					esteControlDeGuardia.escribirElPersonalEnLaTabla()
					esteControlDeGuardia.escribirDiasEnlaTabla(dias)
					esteControlDeGuardia.escribirElCalendarioEnLaTabla(mesActual, mesAnterior, mesSiguiente, dias)
					#INSTANCIACION DE LA CLASE ControlDeGuardia
					indexMeses+=1
					contTablas-= 1
			else:
			
				#INSTANCIACION DE LA CLASE Calendario
				esteCalendario= Calendario(anio, meses[indexMeses])
				mesAnterior= esteCalendario.obtenerCalendarioMesAnterior()
				mesActual= esteCalendario.obtenerCalendarioMesActual()
				mesSiguiente= esteCalendario.obtenerCalendarioMesSiguiente()
				nombreMesActual= esteCalendario.obtenerNombreMesActual()
				dias= esteCalendario.obtenerDias()
				numeroFilas= len(esteCalendario.obtenerCalendarioMesActual()) + 1 # el numero de filas puede variar dependiendo de las semanas + 1 fila del nombre del mes
				numeroColumas= 8 # numero columa constante 8 = 7 columnas de dias + 1 columna del personal
				#INSTANCIACION DE LA CLASE Calendario
				#INSTANCIACION DE LA CLASE ControlDeGuardia
				esteControlDeGuardia.enviarNumeroDeFilas(numeroFilas)
				esteControlDeGuardia.enviarNumeroDeColumnas(numeroColumas)
				esteControlDeGuardia.dibujarUnaTabla()
				esteControlDeGuardia.escribirNombreMesEnLaTabla(nombreMesActual)
				esteControlDeGuardia.escribirElPersonalEnLaTabla()
				esteControlDeGuardia.escribirDiasEnlaTabla(dias)
				esteControlDeGuardia.escribirElCalendarioEnLaTabla(mesActual, mesAnterior, mesSiguiente, dias)
				#INSTANCIACION DE LA CLASE ControlDeGuardia
				indexMeses+=1
				#contTablas-= 1
	
			# PIE DE PAGINA
			esteControlDeGuardia.escribirPieDePagina("Av. Andres Bello, Torre BFC, Piso 13,  "+ 
				  		      "Sector Guaicaipuro, Caracas - Venezuela",480)
			esteControlDeGuardia.escribirPieDePagina("Tlfs +58-212 5785674–Fax +58 212 5724932",495)
			esteControlDeGuardia.selloDelPrograma()
			esteControlDeGuardia.guardarPDF()

			contPaginas-= 2
	
		esteControlDeGuardia.finalizarPDF()

		archivo= os.getcwd()+'/'+titulo
		if(esteControlDeGuardia):
			if(os.path.isfile(archivo)):
				print()
				print("DOCUMENTO GENERADO...")
				print()
				print("Ruta:")
				print("\t\t"+os.getcwd()+'/'+titulo)
				print()
#FIN DE MAIN
