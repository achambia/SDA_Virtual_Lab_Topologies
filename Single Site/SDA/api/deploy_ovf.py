import re
import subprocess
import os
import sys
import logging

from paramiko.agent import value

logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/cisco/app.log'),  # Log messages will be written to 'app.log'
            ]
        )

logger = logging.getLogger(__name__)


def run_subprocess_and_log(command):
    """
    Run a subprocess and log its output in real-time.

    :param command: List of command arguments to execute.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,shell=True)

    # Log stdout
    for stdout_line in iter(process.stdout.readline, ""):
        logger.info(stdout_line.strip())
        if re.search('.*Task.*|.*Disk progress.*|.*Powering.*|.*Transfer.*',stdout_line.strip()):
            print(stdout_line.strip())

    # Log stderr
    for stderr_line in iter(process.stderr.readline, ""):
        logger.error(stderr_line.strip())

    process.stdout.close()
    process.stderr.close()
    process.wait()

    return process.returncode

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
        print('\n!! Initiated the deployment of CML VM !!\n')
        if os.name == 'posix':
            current_dir = os.getcwd()
            os.chdir ('/usr/bin/ovftool')
            return_code = run_subprocess_and_log(f'/usr/bin/ovftool/ovftool --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"CML={network1}" /home/cisco/Desktop/Lab_Build/cml/CML.ovf vi://{user}:{password}@{host}/')
            os.chdir(current_dir)

            
        elif os.name == 'nt':
            current_dir = os.getcwd()
            os.chdir(r'C:\Program Files\VMware\VMware OVF Tool') 
            return_code = run_subprocess_and_log(
            f'ovftool.exe --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"CML={network1}" C:/Users/admin/Desktop/Lab_Build/cml/CML.ovf vi://{user}:{password}@{host}/')
            os.chdir(current_dir)

    except IOError as io_error:
        logger.error(io_error)
        print('!! Deployment of CML failed !!\n')
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
            current_dir = os.getcwd()
            os.chdir ('/usr/bin/ovftool')
            run_subprocess_and_log(f'/usr/bin/ovftool/ovftool --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"Datacenter={network1}" /home/cisco/Desktop/Lab_Build/ISE/ISE.ovf vi://{user}:{password}@{host}/')
            os.chdir(current_dir)


        elif os.name == 'nt':
            current_dir = os.getcwd()
            os.chdir(r'C:\Program Files\VMware\VMware OVF Tool')
            run_subprocess_and_log(f'ovftool.exe --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"Datacenter={network1}" C:/Users/admin/Desktop/Lab_Build/ise/ise.ovf vi://{user}:{password}@{host}/')
            os.chdir(current_dir)

        
    except IOError as io_error:
        logger.error(io_error)
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
            current_dir = os.getcwd()
            os.chdir ('/usr/bin/ovftool')
            run_subprocess_and_log(
            f'/usr/bin/ovftool/ovftool --powerOn -ds={datastore} -n={vm_name} --noSSLVerify --disableVerification --net:"Datacenter={network1}" /home/cisco/Desktop/Lab_Build/wlc/WLC.ovf vi://{user}:{password}@{host}/')
            os.chdir(current_dir)
        elif os.name == 'nt':
            current_dir = os.getcwd()
            os.chdir(r'C:\Program Files\VMware\VMware OVF Tool')
            run_subprocess_and_log(
            f'ovftool.exe --powerOn -ds={datastore} -n={vm_name} --noSSLVerify --disableVerification --net:"Datacenter={network1}" C:/Users/admin/Desktop/Lab_Build/wlc/WLC.ovf vi://{user}:{password}@{host}/')
            os.chdir(current_dir)
        
    except IOError as io_error:
        logger.info(io_error)
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
            current_dir = os.getcwd()
            os.chdir ('/usr/bin/ovftool')
            run_subprocess_and_log(
            f'/usr/bin/ovftool/ovftool --powerOn -ds={datastore} -n={vm_name} --noSSLVerify --disableVerification --net:"Datacenter={network2}" --net:"VM Network={network1}" --net:"CML={network3}" /home/cisco/Desktop/Lab_Build/labrouter/LABRTR.ovf vi://{user}:{password}@{host}/')
            os.chdir(current_dir)
        elif os.name == 'nt':
            current_dir = os.getcwd()
            os.chdir(r'C:\Program Files\VMware\VMware OVF Tool')
            run_subprocess_and_log(
            f'ovftool.exe --powerOn -ds={datastore} -n={vm_name} --noSSLVerify --disableVerification --net:"Datacenter={network2}" --net:"VM Network={network1}" --net:"CML={network3}" C:/Users/admin/Desktop/Lab_Build/labrouter/LABRTR.ovf vi://{user}:{password}@{host}/')
            os.chdir(current_dir)
        
    except IOError as io_error:
        logger.error(io_error)
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
            current_dir = os.getcwd()
            os.chdir ('/usr/bin/ovftool')
            run_subprocess_and_log(
            f'/usr/bin/ovftool/ovftool --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"Datacenter={network1}" /home/cisco/Desktop/Lab_Build/DNAC/DNAC.ovf vi://{user}:{password}@{host}/')
            os.chdir(current_dir)
        elif os.name == 'nt':
            current_dir = os.getcwd()
            os.chdir(r'C:\Program Files\VMware\VMware OVF Tool')
            run_subprocess_and_log(
            f'ovftool.exe --powerOn -ds={datastore} -n={vm_name} -dm=thin --noSSLVerify --disableVerification --net:"Datacenter={network1}" C:/Users/admin/Desktop/Lab_Build/DNAC/DNAC1.ovf vi://{user}:{password}@{host}/')
            os.chdir(current_dir)
        
    except IOError as io_error:
        logger.error(io_error)
        sys.exit()
    return None
