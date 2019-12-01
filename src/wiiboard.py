import cwiid


class WiiBoard:
    def __init__(self):
        self.wb = None

    def conectar(self, intentos=3):
        print(f'Wiiboard.conectar( {intentos} )')
        if intentos:
            try:
                self.wb = cwiid.Wiimote()
                if not self.wb:
                    print('No se ha podido conectar, reintentando conexion')
                    return self.conectar(intentos-1)
                print(f'Estado = {self.wb.request_status()}')
                self.wb.led = cwiid.LED1_ON
                self.wb.rpt_mode = cwiid.RPT_BALANCE
                print('Wiiboard conectada')
                return True
            except RuntimeError as err:
                print(f'Error conectando = {err}')
                return self.conectar(intentos-1)
        print('Imposible conectar')

    def desconectar(self):
        print('Wiiboard.desconectar()')
        self.wb.close()


if __name__ == "__main__":
    wb = WiiBoard()
    input('Aprieta el botón de la Wii para conectar')
    wb.conectar()
    opcion = input('Pulse 1 para acabar')
    wb.desconectar()
