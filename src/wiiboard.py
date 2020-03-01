import cwiid


class WiiBoard:
    def __init__(self):
        self.wb = None

    def __conectar(self) -> bool:
        self.wb = cwiid.Wiimote()
        if self.wb:
            print(f'Estado = {self.wb.request_status()}')
            self.wb.led = cwiid.LED1_ON
            self.wb.rpt_mode = cwiid.RPT_BALANCE
            print('Wiiboard conectada')
            return True
        return False

    def conectar(self, intentos=3):
        print(f'Wiiboard.conectar( {intentos} )')
        if intentos:
            try:
                if self.__conectar():
                    return True
                else:
                    print('No se ha podido conectar, reintentando conexion')
                    self.conectar(intentos-1)
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
    opcion = input('Pulse cualquier botón para acabar')
    wb.desconectar()
