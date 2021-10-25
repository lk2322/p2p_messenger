import sys
import logging
from logging import StreamHandler, Formatter
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)