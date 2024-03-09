import logging
from sys import stdout

logger = logging.getLogger('TestTaskLogger')

logger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)

logger.addHandler(consoleHandler)
