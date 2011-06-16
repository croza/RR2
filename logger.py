import logging
import sys
import os

LOGNAME = "orr.log"

try:
	os.unlink(LOGNAME)
except OSError:
	pass

logger = logging.getLogger("ORR")
logger.setLevel(logging.DEBUG)

logstream = logging.StreamHandler(sys.stderr)
logstream.setLevel(logging.WARNING)

logfile = logging.FileHandler(LOGNAME, "w")
logfile.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

logfile.setFormatter(formatter)
logstream.setFormatter(formatter)
logger.addHandler(logfile)
logger.addHandler(logstream)

logger.debug("Logger loaded successfully.")
