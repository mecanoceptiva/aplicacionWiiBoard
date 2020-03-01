from pytest import fixture


@fixture(scope='class')
def get_wiiboard():
    from src.wii import WiiBoard
    wb = WiiBoard()
    #input('Aprieta el botón de la Wii para conectar')
    if wb.conectar():
        # opcion = input('Pulse cualquier botón para acabar')
        wb.bateria()
        yield wb
        wb.desconectar()
