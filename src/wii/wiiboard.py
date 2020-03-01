from datetime import datetime
import cwiid
from src import logger


class WiiBoard:
    def __init__(self):
        logger.info('Wiiboard created')
        self.wb = None

    def __configurar(self):
        self.wb.led = cwiid.LED1_ON
        self.wb.rpt_mode = cwiid.RPT_BALANCE
        logger.debug('Wiiboard configurada')
        logger.debug(f'Estado = {self.wb.state}')
        # logger.debug(f'Estado = {self.wb.request_status()}')

    def __conectar(self) -> bool:
        t = datetime.now()
        self.wb = cwiid.Wiimote()
        if self.wb:
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
        self.wb.close()

    def bateria(self) -> float:
        bateria = self.wb.state['battery']
        carga = 100.0 * bateria / cwiid.BATTERY_MAX
        logger.info(f'Carga de la batería {carga:.2f} %')
        return carga
