import subprocess
import os
import sys


def deploy_cml(datastore,vm_name,user,password,network1,network2,host):
    '''
    :param datastore: datastore to save the VM.
    :param vm_name: Name of the VM.
    :param user: Name of the user for ESXI.
    :param password: Password for ESXI.
    :param network1: Port Group should be same as of 3rd interface assigned to Jump Server
    :param network2: Port Group that Connects to DNAC, ISE and WLC.
    :param host: Fqdn or IP address of ESXI
    :return: Returns None.
    '''
    try:
        
        if os.name == 'posix':
            subprocess.run(
            f'ovftool --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"CML={network1}" /home/cisco/Desktop/Lab_Build/cml/CML.ovf vi://{user}:{password}@{host}/',
            shell=True)
        elif os.name == 'nt':
            current_dir = os.getcwd()
            os.chdir(r'C:\Program Files\VMware\VMware OVF Tool') 
            subprocess.run(
            f'ovftool.exe --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"CML={network1}" C:/Users/admin/Desktop/Lab_Build/cml/CML.ovf vi://{user}:{password}@{host}/',
            shell=True)
            os.chdir(current_dir)
    except IOError as io_error:
        print(io_error)
        sys.exit()
    return None

def deploy_ise(datastore,vm_name,network1,user,password,host):
    '''
    :param datastore: datastore to save the VM.
    :param vm_name: Name of the VM.
    :param user: Name of the user for ESXI.
    :param password: Password for ESXI.
    :param network1: Port Group that Connects to DNAC and WLC in same LAN.
    :param host: Fqdn or IP address of ESXI
    :return: Returns None.
    '''
    try:
        if os.name == 'posix':
            subprocess.run(
            f'ovftool --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"Datacenter={network1}" /home/cisco/Desktop/Lab_Build/ISE/ISE.ovf vi://{user}:{password}@{host}/',
            shell=True)
        elif os.name == 'nt':
            current_dir = os.getcwd()
            os.chdir(r'C:\Program Files\VMware\VMware OVF Tool')
            subprocess.run(
            f'ovftool.exe --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"Datacenter={network1}" C:/Users/admin/Desktop/Lab_Build/ise/ise.ovf vi://{user}:{password}@{host}/',
            shell=True)
            os.chdir(current_dir)
        
    except IOError as io_error:
        print(io_error)
        sys.exit()
    return None


def deploy_wlc(datastore,vm_name,network1,user,password,host):
    '''
    :param datastore: datastore to save the VM.
    :param vm_name: Name of the VM.
    :param user: Name of the user for ESXI.
    :param password: Password for ESXI.
    :param network1: Port Group that Connects to ISE and DNAC in same LAN.
    :param host: Fqdn or IP address of ESXI.
    :return: Returns None.
    '''

    try:
        if os.name == 'posix':
            subprocess.run(
            f'ovftool --powerOn -ds={datastore} -n={vm_name} --noSSLVerify --disableVerification --net:"Datacenter={network1}" /home/cisco/Desktop/Lab_Build/wlc/WLC.ovf vi://{user}:{password}@{host}/',
            shell=True)
        elif os.name == 'nt':
            current_dir = os.getcwd()
            os.chdir(r'C:\Program Files\VMware\VMware OVF Tool')
            subprocess.run(
            f'ovftool.exe --powerOn -ds={datastore} -n={vm_name} --noSSLVerify --disableVerification --net:"Datacenter={network1}" C:/Users/admin/Desktop/Lab_Build/wlc/WLC.ovf vi://{user}:{password}@{host}/',
            shell=True)
            os.chdir(current_dir)
        
    except IOError as io_error:
        print(io_error)
        sys.exit()
    return None


def deploy_labrouter(datastore,vm_name,network1,network2,network3,user,password,host):
    '''
    :param datastore: datastore to save the VM.
    :param vm_name: Name of the VM.
    :param user: Name of the user for ESXI.
    :param password: Password for ESXI.
    :param network1: Port Group that Connects to Internet.
    :param network2: Port Group that Connects to ISE and DNAC in same LAN.
    :param network3: Port Group that Connects to Windows Jump Server and CML.
    :param host: Fqdn or IP address of ESXI.
    :return: Returns None
    '''

    try:
        if os.name == 'posix':
            subprocess.run(
            f'ovftool --powerOn -ds={datastore} -n={vm_name} --noSSLVerify --disableVerification --net:"Datacenter={network2}" --net:"VM Network={network1}" --net:"CML={network3}" /home/cisco/Desktop/Lab_Build/labrouter/LABRTR.ovf vi://{user}:{password}@{host}/',
            shell=True)
        elif os.name == 'nt':
            current_dir = os.getcwd()
            os.chdir(r'C:\Program Files\VMware\VMware OVF Tool')
            subprocess.run(
            f'ovftool.exe --powerOn -ds={datastore} -n={vm_name} --noSSLVerify --disableVerification --net:"Datacenter={network2}" --net:"VM Network={network1}" --net:"CML={network3}" C:/Users/admin/Desktop/Lab_Build/labrouter/LABRTR.ovf vi://{user}:{password}@{host}/',
            shell=True)
            os.chdir(current_dir)
        
    except IOError as io_error:
        print(io_error)
        sys.exit()
    return None

def deploy_cc(datastore,vm_name,network1,user,password,host):
    '''
    :param datastore: datastore to save the VM.
    :param vm_name: Name of the VM.
    :param user: Name of the user for ESXI.
    :param password: Password for ESXI.
    :param network1: Port Group that Connects to DNAC and WLC in same LAN.
    :param host: Fqdn or IP address of ESXI
    :return: Returns None.
    '''
    try:
        if os.name == 'posix':
            subprocess.run(
            f'ovftool --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"Datacenter={network1}" /home/cisco/Desktop/Lab_Build/DNAC/DNAC.ovf vi://{user}:{password}@{host}/',
            shell=True)
        elif os.name == 'nt':
            current_dir = os.getcwd()
            os.chdir(r'C:\Program Files\VMware\VMware OVF Tool')
            subprocess.run(
            f'ovftool.exe --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"Datacenter={network1}" C:/Users/admin/Desktop/Lab_Build/DNAC/DNAC1.ovf vi://{user}:{password}@{host}/',
            shell=True)
            os.chdir(current_dir)
        
    except IOError as io_error:
        print(io_error)
        sys.exit()
    return None
