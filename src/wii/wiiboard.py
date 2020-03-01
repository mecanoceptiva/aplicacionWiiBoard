from datetime import datetime
import cwiid
from src import logger


class WiiBoard:
    def __init__(self):
        logger.info('Wiiboard created')
        self.__wb = None
        self.__calibracion = {
            'right_top': [],
            'right_bottom': [],
            'left_top': [],
            'left_bottom': []
        }

    def __configurar(self):
        self.__wb.led = cwiid.LED1_ON
        self.__wb.rpt_mode = cwiid.RPT_BALANCE
        logger.debug('Wiiboard configurada')
        logger.debug(f'Estado = {self.__wb.state}')
        # logger.debug(f'Estado = {self.__wb.request_status()}')

    def __conectar(self) -> bool:
        t = datetime.now()
        self.__wb = cwiid.Wiimote()
        if self.__wb:
            logger.debug(f'Tiempo en conectar = {datetime.now() - t}')
            self.__configurar()
            logger.info('Wiiboard conectada')
            return True
        logger.error('Error conectando')
        return False

    def conectar(self, intentos=3) -> bool:
        logger.info(f'Wiiboard.conectar( {intentos} )')
        if intentos:
            try:
                if self.__conectar():
                    return True
                else:
                    logger.error('Reintentando conexion')
                    self.conectar(intentos-1)
            except RuntimeError as err:
                logger.error(f'Error conectando = {err}')
                return self.conectar(intentos-1)
        logger.critical('Imposible conectar')
        return False

    def desconectar(self):
        logger.error('Wiiboard.desconectar()')
        self.__wb.close()

    def bateria(self) -> float:
        self.__wb.request_status()
        bateria = self.__wb.state['battery']
        carga = bateria / cwiid.BATTERY_MAX
        logger.info(f'Carga de la batería {(100.0 * carga):.2f} %')
        return carga

    def calibrar(self):
        calibracion = self.__wb.get_balance_cal()
        self.__calibracion['right_top'] = calibracion[0]
        self.__calibracion['right_bottom'] = calibracion[1]
        self.__calibracion['left_top'] = calibracion[2]
        self.__calibracion['left_bottom'] = calibracion[3]
        logger.info(f'Calibracion = {self.__calibracion}')

    def referencia(self) -> dict:
        return self.__calibracion

    def obtener_valores(self):
        logger.info(f'Estado {self.__wb.state}')
