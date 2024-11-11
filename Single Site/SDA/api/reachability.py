from pythonping import ping
import re
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set the log level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format of log messages
    handlers=[
        logging.FileHandler('app.log'),  # Log messages will be written to 'app.log'
        logging.StreamHandler()  # Log messages will also be printed to the console
    ]
)

logger = logging.getLogger(__name__)

def ping_test(dest):
    a = ping(dest, count=5)
    b = re.findall(f'Reply from {dest}',str(a))
    logger.info(b)
    if len(b) >= 3 :
        value = 'success'
    else:
        value = 'failure'
    return value
