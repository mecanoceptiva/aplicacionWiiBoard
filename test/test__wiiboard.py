from src import logger
from src.wii import WiiBoard


class TestWiiboard:
    def test_bateria(self, get_wiiboard: WiiBoard):
        wb = get_wiiboard
        carga = wb.bateria()
        assert isinstance(carga, float)

    def test_referencia_inicial(self, get_wiiboard: WiiBoard):
        wb = get_wiiboard
        wb.calibrar()
        logger.debug(f'Calibracion = {wb.referencia()}')
        for k, v in wb.referencia().items():
            assert len(v) == 3
