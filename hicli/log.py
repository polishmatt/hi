import logging
import sys


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.DEBUG, logging.INFO)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.addFilter(InfoFilter())
logger.addHandler(handler)

handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)
logger.addHandler(handler)
