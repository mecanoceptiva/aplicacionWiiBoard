
class TestWiiboard:
    def test_bateria(self, get_wiiboard):
        wb = get_wiiboard
        carga = wb.bateria()
        assert isinstance(carga, float)
