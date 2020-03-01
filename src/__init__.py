import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[0]
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)
# Crear logger
logger = logging.getLogger('MisLogs')
logger.setLevel(logging.DEBUG)
# Crear handlers (donde van a ir los datos)
datetime_filename = ':%Y-%m-%d %H:%M:%S'
fh = logging.FileHandler(filename='{}.log'.format(datetime_filename))
fh.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
# Crear formatter y añadir a los handlers
fmt = '%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s'
formatter = logging.Formatter(fmt)
fh.setFormatter(formatter)
sh.setFormatter(formatter)
# Añadir handlers al logger
logger.addHandler(fh)
logger.addHandler(sh)
