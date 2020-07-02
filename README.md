<h1>Automatización del Cronograma de Guardia</h1>

<h3>Requisitos:</h3>

	python 3


<h3>Instalación:</h3>

instalamos pip3

	apt-get install python3-pip

el entorno virtual virtualenv no es indispensable, pero permite aislar las librerias

	pip3 install virtualenv

crear el entorno virutal con virtualenv

	virtualenv envcrono --python=python3

entrar en la carpeta "envcrono"

	cd /ruta/envcrono

descargar el codigo fuente del programa

	git clone https://github.com/MiguelM001/cronguardvencert.git

dentro de la carpeta "envcrono" ejecutar:

	source bin/activate

instalar la libreria reportlab

	pip3 install reportlab

entrar en la carpeta cronguardvencert y ejecutar cualquiera de los siguientes comandos:

	python3 cronguardvencert.py
	python3 cronguardvencert.py -h
	python3 cronguardvencert.py --help

Se desplegará un menu de ayuda junto con un ejemplo de uso del programa.

