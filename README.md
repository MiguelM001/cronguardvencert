<h1>Automatización del Cronograma de Guardia</h1>

<h3>Requisitos:</h3>

	python 3


<h3>Instalación:</h3>

instalamos pip3

	<code>apt-get install python3-pip</code>

el entorno virtual virtualenv no es indispensable, pero permite aislar las librerias

	<code>pip3 install virtualenv</code>

crear el entorno virutal con virtualenv

	<code>virtualenv envcrono --python=python3</code>

entrar en la carpeta "envcrono"

	<code>cd /ruta/envcrono</code>

descargar el codigo fuente del programa

	<code>git clone https://github.com/MiguelM001/cronguardvencert.git</code>

dentro de la carpeta "envcrono" ejecutar:

	<code>source bin/activate</code>

instalar la libreria reportlab

	<code>pip3 install reportlab</code>

entrar en la carpeta cronguardvencert y ejecutar cualquiera de los siguientes comandos:

	<code>python3 cronguardvencert.py</code>
	<code>python3 cronguardvencert.py -h</code>
	<code>python3 cronguardvencert.py --help</code>

Se desplegará un menu de ayuda junto con un ejemplo de uso del programa.
