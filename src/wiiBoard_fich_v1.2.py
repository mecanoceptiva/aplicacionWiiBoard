# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# -  wiiBoard_fich_v1.1.py
# -  Visualizazcion CG y pesos en cada sensor de la Wii Board
# -  Representación gráfica de CG y pesos de cada sensor
#------------------------------------------------------------------------------
# - Manuel Hidalgo - leobotmanuel
#-----------------------------------------------------------------------------
# Importar modulos
import shelve
import sys
import cwiid
import time
import pygame
import matplotlib.pyplot as plt


#------------------------------------------------------------------------------
# Devolver una cadena con el estado de la bateria
def estado_bateria(state):
    bateria = state['battery']
    porcentaje = (100.0 * bateria / cwiid.BATTERY_MAX)
    return 'Battery: {}%'.format(int(porcentaje))


#------------------------------------------------------------------------------
#Leer los valores normalizados de los 4 sensores
def leer_sensores(wiimote, calibration):
    state = wiimote.state

    sensor = 'left_top'
    valor = state['balance'][sensor]
    valor0 = calibration[sensor][0]
    valor1 = calibration[sensor][1]
    a = 1700 * float((valor - valor0)) / float((valor1-valor0))

    sensor = 'right_top'
    valor = state['balance'][sensor]
    valor0 = calibration[sensor][0]
    valor1 = calibration[sensor][1]
    b = 1700 * float((valor - valor0)) / float((valor1-valor0))

    sensor = 'left_bottom'
    valor = state['balance'][sensor]
    valor0 = calibration[sensor][0]
    valor1 = calibration[sensor][1]
    c = 1700 * float((valor - valor0)) / float((valor1-valor0))

    sensor = 'right_bottom'
    valor = state['balance'][sensor]
    valor0 = calibration[sensor][0]
    valor1 = calibration[sensor][1]
    d = 1700 * float((valor - valor0)) / float((valor1-valor0))

    return (a, b, c, d)


#------------------------------------------------------------------------------
# Comienzo programa
#------------------------------------------------------------------------------
# Variables en el establecimeinto de conexión PC-WiiBoard
intentos = 0  # contador de intentos de conexion
ok = False

# mensaje por pantalla para sincronizar PC-WiiBoard
print('Pulsa el boton de sync de la wiiboard (donde estan las pilas)...')

# Establecer conexion con Wiimote
while intentos < 3 and not ok:
    try:
        print("Intento de conexion numero: {}".format(intentos + 1))
        if len(sys.argv) > 1:
            wiimote = cwiid.Wiimote(sys.argv[1])
        else:
            wiimote = cwiid.Wiimote()
        ok = True
    except RuntimeError:
        intentos += 1

# Si se superan el numero de intentos, terminar
if intentos == 3:
    print(f"Sin conexion con Wii Board, intentos de conexión: {intentos}")
    sys.exit(-1)

# Conexion establecida
# Encender el led de la wii-board
wiimote.led = cwiid.LED1_ON

# Activar la wii-board
wiimote.rpt_mode = cwiid.RPT_BALANCE

print("CONEXION ESTABLECIDA")
#------------------------------------------------------------------------------
# Obtener los valores de calibracion, usados para calcular
# los valores normalizados de los sensores de presion
balance_calibration = wiimote.get_balance_cal()
calibration = {
    'right_top': balance_calibration[0],
    'right_bottom': balance_calibration[1],
    'left_top': balance_calibration[2],
    'left_bottom': balance_calibration[3]
}

pygame.init()
size = width, height = 410, 260
black = 0, 0, 0
white = 255, 255, 255
# color1 = 196, 160, 15
color1 = 0, 0, 0
font = pygame.font.Font(None, 16)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Grawiity_center")

# Cargamos la imagen de la wiiboard
fondo = pygame.image.load("wiiboard-top-view-1-1.jpg")
fondorect = fondo.get_rect()

time.sleep(0.2)

try:
    print("Para terminar pulsar Control-C")
    print("Quieres tomar medidas, pulsar '1'.")
    opcion = input("Introduce una opcion: ")

    while opcion == 1:
        # Variable para mostrar/ocultar el peso
        view_peso = True

        # variables para el crono
        tiempo_transcurrido = 0
        time1 = 0
        time2 = 0
        inicio_de_tiempo = time.time()

        # variable para la lista
        lista_xpos = []
        lista_ypos = []
        lista_lt = []
        lista_lb = []
        lista_rt = []
        lista_rb = []
        lista_peso = []

        while (time1 < 30):
            # Leer los valores nomalizados de los sensores
            lt, rt, lb, rb = leer_sensores(wiimote, calibration)

            # Calcular el peso en kilos
            peso = (lt + rt + lb + rb) / 100.0

            # crono
            tiempo_final = time.time()
            tiempo_transcurrido = tiempo_final - inicio_de_tiempo
            time2 = (tiempo_transcurrido)  # time2=  int(tiempo_transcurrido)
            if time2 != time1:
                time1 = time2

            # Se usa un umbral de peso para determinar si hay
            # alguien subido. El peso debe ser mayor de 2Kg
            if peso > 2:
                # Calcular las posiciones x,y del centro de gravedad
                try:
                    x_balance = (rt + rb) / (lt + lb)
                    if x_balance > 1:
                        x_balance = -1.0 * (lt + lb) / (rt + rb) + 1.0
                    else:
                        x_balance = x_balance - 1.0

                    y_balance = (lb + rb) / (lt + rt)

                    if y_balance > 1:
                        y_balance = -1.0 * (lt + rt) / (lb + rb) + 1.0
                    else:
                        y_balance = y_balance - 1.0
                except Exception:
                    x_balance = 1.0
                    y_balance = 1.0

            # Peso menor de dos kilos: no hay nadie subido
            else:
                x_balance = 0.0
                y_balance = 0.0

            # Escalar las coordenadas y establecer el criterio de signos
            xpos = 200 * x_balance + 200
            ypos = 124 * y_balance + 124

            # Comprobar si programa terminado
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wiimote.close()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if view_peso:
                        view_peso = False
                else:
                    view_peso = True

            screen.blit(fondo, fondorect)
            text_bateria = font.render(
                str(estado_bateria(wiimote.state)), True, black)
            screen.blit(text_bateria, (75, 242))

            text_crono = font.render(
                "Crono: %d segundos." % time1, True, black)
            screen.blit(text_crono, (150, 242))

            if view_peso:
                text_peso = font.render("Peso: %d" % peso, True, black)
                screen.blit(text_peso, (275, 242))

            # Estado sensores de peso
            text_lt = font.render("%d" % (lt / 100), True, color1)
            screen.blit(text_lt, (80, 70))

            text_lb = font.render("%d" % (lb / 100), True, color1)
            screen.blit(text_lb, (80, 175))

            text_rt = font.render("%d" % (rt / 100), True, color1)
            screen.blit(text_rt, (320, 70))

            text_rb = font.render("%d" % (rb / 100), True, color1)
            screen.blit(text_rb, (320, 175))

            # Circulo para indicar la posicion del centro de gravedad
            pygame.draw.circle(screen, (255, 0, 0), (int(xpos), int(ypos)), 10)
            pygame.display.flip()

            # Escalar las coordenadas y establecer el criterio de signos
            # para la representación gráfica
            xgpos = int(100 * x_balance)
            ygpos = int(-100 * y_balance)

            # Carga las coordenada de CG
            lista_xpos.append(xgpos)
            lista_ypos.append(ygpos)
            # Carga los valores de los sensores
            lista_lt.append(lt / 100)
            lista_lb.append(lb / 100)
            lista_rt.append(rt / 100)
            lista_rb.append(rb / 100)
            # Carga el resultado del peso
            lista_peso.append(peso)
            # print(lista_lt)

        print("--Fin de toma de datos--")
        datos = len(lista_peso)
        print("Numero de datos tomados: ", datos)
        #print(lista_xpos)
        #print(lista_ypos)

        #-- Guardar las listas en ficheros
        f_xpos = open('./ficheros/fichero_xpos.txt', 'w')
        for l in lista_xpos:
            f_xpos.write(str(l) + '\n')
        f_xpos.close()

        f_ypos = open('./ficheros/fichero_ypos.txt', 'w')
        for l in lista_ypos:
            f_ypos.write(str(l) + '\n')
        f_ypos.close()

        f_lt = open('./ficheros/fichero_lt.txt', 'w')
        for l in lista_lt:
            f_lt.write(str(l) + '\n')
        f_lt.close()

        f_lb = open('./ficheros/fichero_lb.txt', 'w')
        for l in lista_lb:
            f_lb.write(str(l) + '\n')
        f_lb.close()

        f_rt = open('./ficheros/fichero_rt.txt', 'w')
        for l in lista_rt:
            f_rt.write(str(l) + '\n')
        f_rt.close()

        f_rb = open('./ficheros/fichero_rb.txt', 'w')
        for l in lista_rb:
            f_rb.write(str(l) + '\n')
        f_rb.close()

        f_peso = open('./ficheros/fichero_peso.txt', 'w')
        for l in lista_peso:
            f_peso.write(str(l) + '\n')
        f_peso.close()

        # Fichero binario
        fichBinario = shelve.open(r"./ficheros/datosWB")
        fichBinario["lista_xpos"] = lista_xpos
        fichBinario["lista_ypos"] = lista_ypos
        fichBinario["lista_lt"] = lista_lt
        fichBinario["lista_lb"] = lista_lb
        fichBinario["lista_rt"] = lista_rt
        fichBinario["lista_rb"] = lista_rb
        fichBinario["lista_peso"] = lista_peso
        # cierre de fichero
        fichBinario.close()

        # Medias de los sensores de fuerza y peso
        suma_lt = 0
        suma_lb = 0
        suma_rt = 0
        suma_rb = 0
        suma_peso = 0

        for i in range(datos):
            suma_lt = suma_lt + lista_lt[i]
            suma_lb = suma_lb + lista_lb[i]
            suma_rt = suma_rt + lista_rt[i]
            suma_rb = suma_rb + lista_rb[i]
            suma_peso = suma_peso + lista_peso[i]

        media_lt = format((suma_lt / datos), ".2f")
        media_lb = format((suma_lb / datos), ".2f")
        media_rt = format((suma_rt / datos), ".2f")
        media_rb = format((suma_rb / datos), ".2f")
        media_peso = format((suma_peso / datos), ".2f")
        print("Valor medio del peso sensor superior izq: ", media_lt)
        print("Valor medio del peso sensor inferior izq: ", media_lb)
        print("Valor medio del peso sensor superior dch: ", media_rt)
        print("Valor medio del peso sensor inferior dch: ", media_rb)
        print("Valor medio del peso: ", media_peso)

        # Representacion grafica
        plt.suptitle("Desplazamiento Centro de Gravedad", fontsize=24)
        plt.xlabel("Desplazamiento eje X", fontsize=11)
        plt.ylabel("Desplazamiento eje Y", fontsize=11)
        plt.grid()
        plt.xlim(-100, 100)
        plt.ylim(-100, 100)
        plt.plot(lista_xpos, lista_ypos)
        plt.show()

        print("\n-----------------------------------------------")
        print("\nPara terminar pulsar Control-C")
        print("Quieres volver a tomar medidas, pulsar 's'.")
        opcion = input("Introduce una opcion, Control-C o 's': ")

    wiimote.close()
    print("--FIN--")
# Terminar con Control-C
except KeyboardInterrupt:
    wiimote.close()
    print("\n-- FIN --")
