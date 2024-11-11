import netmiko
from netmiko import ConnectHandler
import warnings
warnings.filterwarnings(action='ignore', module='.*paramiko.*')
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

def labrtr(ip,netmask,next_hop):
    net_connect = ConnectHandler(
        device_type="cisco_xe",
        host="169.100.100.1",
        username="admin",
        password="C1sco12345",
    )

    output = net_connect.send_config_set(
        ['hostname FUSION','int GigabitEthernet1', f'ip address {ip} {netmask}', f'ip route 0.0.0.0 0.0.0.0 {next_hop}','do wr'])
    logger.info(output)
    print('!! Router configured with uplink IP and next HOP !! \n')

