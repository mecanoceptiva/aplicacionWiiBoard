import cwiid

print('Conectando la wii')
wiimote = None
try:
    wiimote = cwiid.Wiimote()
    if wiimote:
        print('conectado')
        wiimote.led = cwiid.LED1_ON
        # Activar la wii-board
        wiimote.rpt_mode = cwiid.RPT_BALANCE        
except RuntimeError:
    print('error conectando')
else:
    print('Wiiboard lista')
    rta = input('Pulse tecla para acabar')
    wiimote.close()
finally:
    print('Adios')
