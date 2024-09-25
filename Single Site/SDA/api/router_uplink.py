import netmiko
from netmiko import ConnectHandler
import warnings
warnings.filterwarnings(action='ignore', module='.*paramiko.*')

def labrtr(ip,netmask,next_hop):
    net_connect = ConnectHandler(
        device_type="cisco_xe",
        host="169.100.100.1",
        username="admin",
        password="C1sco12345",
    )

    output = net_connect.send_config_set(
        ['hostname FUSION','int GigabitEthernet1', f'ip address {ip} {netmask}', f'ip route 0.0.0.0 0.0.0.0 {next_hop}','do wr'])
    print(output)

