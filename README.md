# Wii Balance Board. Grafiando el centro de gravedad (CG).

![Wii Balance Board](https://github.com/mecanoceptiva/aplicacionWiiBoard/blob/master/scr/img/02_balanceBoardSensorsNorm.gif)Fuente: www.nitendo.com

La plataforma [Wii Balance Board](https://es.wikipedia.org/wiki/Wii_Balance_Board) es una palataforma de fuerza que permite medir el movimiento del centro de gravedad de una persona.

El movimiento del centro de gravedad se determina por medio de los 4 sensores de fuerza que tiene la plataforma. 

![Wii Balance Board](https://github.com/mecanoceptiva/aplicacionWiiBoard/blob/master/scr/img/01_balanceBoardSensors.gif)Fuente: www.nitendo.com

La aplicación desarrollada (se sigue trabajando en ella para mejorarla) para visualizar y captar los datos, procesándolos posteriormente está escrita en el lenguaje de programación [Python 3.x](https://www.python.org/) y probada en el sistema operativo [Ubuntu LTS 16.04](https://www.ubuntu.com/).

La aplicación conecta a la Wii Board con el PC a través de una conexión bluetooth obteniendo los datos de los cuatro sensores de fuerza.
Esta conexión se hace utilizando la librería **cwiid** para [Python](https://www.python.org/).

![conexion WB Bluetooth](https://github.com/mecanoceptiva/aplicacionWiiBoard/blob/master/scr/img/03_conexionBlue.jpg)

La visualización de los pesos y el movimeinto del centro de gravedad se ha utiliza la librería **Pygame** para [Python](https://www.python.org/).

![WB_CG](https://github.com/mecanoceptiva/aplicacionWiiBoard/blob/master/scr/img/04_PesosCG.png)

La instalación de las librerías y su programación está basada en el Trabajo Fin de Carrera (TFC) de [Carlos Pastor Herrán](http://www.iearobotics.com/wiki/index.php?title=Juan_Gonzalez:PFC:Wii-applications) y ha sido actualizada a la versión de [Python 3.x](https://www.python.org/).

