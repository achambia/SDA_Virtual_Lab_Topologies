import shutil
import netmiko
from netmiko import ConnectHandler
import json
from SDA.SDA.api.SitesApiService import SitesApiService
from SDA.SDA.reqs.SiteRequest import SiteRequest
from SDA.SDA.enums.SiteTypeEnum import SiteTypeEnum
from SDA.SDA.reqs.GlobalPoolRequest import GlobalPoolRequest
from SDA.SDA.params.GetSiteParams import GetSiteParams
from SDA.SDA.api.NetworkSettingsApiService import NetworkSettingsApiService
from SDA.SDA.models.IPPoolModel import IPPoolModel
import urllib3
import csv
from SDA.SDA.api.CommandRunnerApiService import CommandRunnerApiService
from urllib3.exceptions import InsecureRequestWarning
from SDA.SDA.reqs.NetworkSettingsRequest import NetworkSettingsRequest
from SDA.SDA.models.NetworkSettingsModel import NetworkSettingsModel
from SDA.SDA.models.DnsServerModel import DnsServerModel
from SDA.SDA.models.MessageOfTheDayModel import MessageOfTheDayModel
urllib3.disable_warnings(InsecureRequestWarning)
import re
from SDA.SDA.reqs.ReserveIPPoolRequest import ReserveIpPoolReq
import os
from SDA.SDA.enums.TimezoneEnum import TimezoneEnum
from SDA.SDA.api.TemplateAPiService import TemplateApiService
from SDA.SDA.api.AuthenticationApiService import AuthenticationApiService
from SDA.SDA.reqs.ProjectRequest import ProjectRequest
from SDA.SDA.api.TaskApiService import TaskApiService
from SDA.SDA.reqs.TemplateRequest import TemplateRequest
from SDA.SDA.models.ProductFamilyModel import ProductFamilyModel
from SDA.SDA.reqs.VersionTemplateRequest import VersionTemplateRequest
from SDA.SDA.reqs.DeployTemplateRequest import DeployTemplateRequest
from SDA.SDA.models.TemplateTargetInfoModel import TemplateTargetInfoModel
from SDA.SDA.enums.TemplateTargetInfoTypeEnum import TemplateTargetInfoTypeEnum
import time
from SDA.SDA.api.FileApiService import FileApiService
from SDA.SDA.api.SDAApiService import SDAApiService
from SDA.SDA.params.GetlistProject import GetlistProject
from SDA.SDA.models.CommandRunnerModel import CommandRunnerModel
from SDA.SDA.params.GetDeviceListParams import GetDeviceListParams
from SDA.SDA.api.DevicesApiService import DevicesApiService
from SDA.SDA.params.GetlistTemplate import GetlistTemplate
from SDA.SDA.api.DiscoveryApiService import DiscoveryApiService
from SDA.SDA.api.AuthenticationServerApiService import ise_dnac_integration
from SDA.SDA.api.ProvisionApiService import provisionservice
import random
import requests
def copy_file(file):
    try:
        shutil.rmtree('C:/Users/admin/PycharmProjects/pythonProject/.venv/SDA')
        shutil.copytree(f'C:/Program Files/Git/cmd/{file}',
                        'C:/Users/admin/PycharmProjects/pythonProject/.venv/SDA')
    except Exception as e:
        print(e)
        shutil.copytree(f'C:/Program Files/Git/cmd/{file}','C:/Users/admin/PycharmProjects/pythonProject/.venv/SDA')

def device_config(rtr,config):
    
    try:
        net_connect = ConnectHandler(
            device_type="cisco_xe",
            host=rtr,
            username="netadmin",
            password="cisco",
        )

        output = net_connect.send_config_set(config, read_timeout=300)
        print(output)
        return output
    except Exception as e:
        print(e)
        time.sleep(120)
        net_connect = ConnectHandler(
            device_type="cisco_xe",
            host=rtr,
            username="netadmin",
            password="cisco",
        )

        output = net_connect.send_config_set(config, read_timeout=300)
        print(output)
        return output
        



def reserve_ip_pool(name,type,ipv6add,ipv4addpool,ipv4prefix,ipv4prefixlen,ipv4subnet,ipv4gw,dhcp,dns,site,url,token):

    reserve_ip_info = ReserveIpPoolReq(name,type,ipv6add,ipv4addpool,ipv4prefix)
    reserve_ip_info.ipv4PrefixLength = ipv4prefixlen
    reserve_ip_info.ipv4Subnet = ipv4subnet
    reserve_ip_info.ipv4GateWay = ipv4gw
    reserve_ip_info.ipv4DhcpServers = dhcp
    reserve_ip_info.ipv4DnsServers = dns
    reserveresp = NetworkSettingsApiService(f"https://{url}",token).reserveIPPool(site['siteId'], reserve_ip_info)
    print(reserveresp)
    return None

def create_area(name,ip,Auth):
    siteinfo = SiteRequest(SiteTypeEnum.AREA)
    siteinfo.site.area.name = name
    siteinfo.site.area.parentName = 'Global'
    areares = SitesApiService(f"https://{ip}", Auth).createSite(siteinfo)
    return areares


def create_building(name,parentName,latitude,longitude,ip,Auth):
    siteinfo = SiteRequest(SiteTypeEnum.BUILDING)
    siteinfo.site.building.name = name
    siteinfo.site.building.parentName = parentName
    siteinfo.site.building.latitude = latitude
    siteinfo.site.building.longitude = longitude
    buildres = SitesApiService(f"https://{ip}", Auth).createSite(siteinfo)
    return buildres

def create_floor(name,parentName,rfModel,width,length,height,floorNumber,ip,Auth):
    siteinfo = SiteRequest(SiteTypeEnum.FLOOR)
    siteinfo.site.floor.name = name
    siteinfo.site.floor.parentName = parentName
    siteinfo.site.floor.rfModel = rfModel
    siteinfo.site.floor.width = width
    siteinfo.site.floor.length = length
    siteinfo.site.floor.height = height
    siteinfo.site.floor.floorNumber = floorNumber
    floorres = SitesApiService(f"https://{ip}", Auth).createSite(siteinfo)
    return floorres




def create_reserve_pool_site(path,Auth,ip):
    area = []
    building = []
    with open(f"{path}") as file:
        heading = next(file)
        reader = csv.reader(file)
        for x in reader:
            if x[1] not in area:
                arearesp = create_area(x[1], ip, Auth)
                if arearesp['status'] == 'True':
                    print(f"Area {x[1]} created successfully.\n")
                if x[0] != 'None':
                    raw_ippool = re.split(';', x[0])
                    for ip_pool in raw_ippool:
                        reserve_ip = (re.split(',', ip_pool))
                        reserve_ip_pool(reserve_ip[0], reserve_ip[1], eval(reserve_ip[2]), reserve_ip[3], eval(reserve_ip[4]), reserve_ip[5], reserve_ip[6], reserve_ip[7], [reserve_ip[8]], [reserve_ip[9]], arearesp, ip, Auth)
                area.append(x[1])
                buildresp= create_building(x[2],f"Global/{x[1]}",x[4],x[5],ip,Auth)
                if buildresp['status'] == 'True':
                    print(f"Buiding {x[2]} in Area {x[1]} created successfully.\n")
                if x[3] != 'None':
                    raw_ippool = re.split(';', x[3])
                    for ip_pool in raw_ippool:
                        reserve_ip = (re.split(',', ip_pool))
                        reserve_ip_pool(reserve_ip[0], reserve_ip[1], eval(reserve_ip[2]), reserve_ip[3], eval(reserve_ip[4]), reserve_ip[5], reserve_ip[6], reserve_ip[7], [reserve_ip[8]], [reserve_ip[9]], buildresp, ip, Auth)
                building.append(str(x[1])+str(x[2]))
                floorresp = create_floor(x[7],f"Global/{x[1]}/{x[2]}",x[8],x[9],x[10],x[11],x[12],ip,Auth)
                if floorresp['status'] == 'True':
                    print(f"Floor {x[7]} in Building {x[2]} created successfully.\n")
                if x[6] != 'None':
                    raw_ippool = re.split(';', x[6])
                    print(raw_ippool)
                    for ip_pool in raw_ippool:
                        reserve_ip = (re.split(',', ip_pool))
                        reserve_ip_pool(reserve_ip[0], reserve_ip[1], eval(reserve_ip[2]), reserve_ip[3], eval(reserve_ip[4]),
                                        reserve_ip[5], reserve_ip[6], reserve_ip[7], [reserve_ip[8]], [reserve_ip[9]],
                                        floorresp, ip, Auth)
            elif str(x[1]) + str(x[2]) not in building:
                buildresp = create_building(x[2], f"Global/{x[1]}", x[4], x[5], ip, Auth)
                if buildresp['status'] == 'True':
                    print(f"Buiding {x[2]} in Area {x[1]} created successfully.\n")
                if x[3] != 'None':
                    raw_ippool = re.split(';', x[3])
                    for ip_pool in raw_ippool:
                        reserve_ip = (re.split(',', ip_pool))
                        reserve_ip_pool(reserve_ip[0], reserve_ip[1], eval(reserve_ip[2]), reserve_ip[3],
                                        eval(reserve_ip[4]), reserve_ip[5], reserve_ip[6], reserve_ip[7],
                                        [reserve_ip[8]], [reserve_ip[9]], buildresp, ip, Auth)
                building.append(str(x[1]) + str(x[2]))
                floorresp = create_floor(x[7],f"Global/{x[1]}/{x[2]}",x[8],x[9],x[10],x[11],x[12],ip,Auth)
                if floorresp['status'] == 'True':
                    print(f"Floor {x[7]} in Building {x[2]} created successfully.\n")
                if x[6] != 'None':
                    raw_ippool = re.split(';', x[6])
                    print(raw_ippool)
                    for ip_pool in raw_ippool:
                        reserve_ip = (re.split(',', ip_pool))
                        reserve_ip_pool(reserve_ip[0], reserve_ip[1], eval(reserve_ip[2]), reserve_ip[3], eval(reserve_ip[4]),
                                        reserve_ip[5], reserve_ip[6], reserve_ip[7], [reserve_ip[8]], [reserve_ip[9]],
                                        floorresp, ip, Auth)

            else:
                floorresp = create_floor(x[7],f"Global/{x[1]}/{x[2]}",x[8],x[9],x[10],x[11],x[12],ip,Auth)
                if floorresp['status'] == 'True':
                    print(f"Floor {x[7]} in Building {x[2]} created successfully.\n")
                if x[6] != 'None':
                    raw_ippool = re.split(';', x[6])
                    print(raw_ippool)
                    for ip_pool in raw_ippool:
                        reserve_ip = (re.split(',', ip_pool))
                        reserve_ip_pool(reserve_ip[0], reserve_ip[1], eval(reserve_ip[2]), reserve_ip[3], eval(reserve_ip[4]),
                                        reserve_ip[5], reserve_ip[6], reserve_ip[7], [reserve_ip[8]], [reserve_ip[9]],
                                        floorresp, ip, Auth)

def create_global_pool(path,Auth,ip):
    rotation = 0
    with open(f"{path}") as file:
        heading = next(file)
        reader = csv.reader(file)
        Globalparam = GlobalPoolRequest()
        for x in reader:
            ipmodelparam = IPPoolModel(x[0],x[1],x[2],x[3])
            Globalparam.settings.ippool = [ipmodelparam]
            globalres = NetworkSettingsApiService(f"https://{ip}", Auth).createGlobalPool(Globalparam)
            if globalres['status'] == 'true':
                print(f'Global Pool {x[0]} was successfully created \n')
            else:
                print(f"!!! ERROR !!! {globalres['errorMessage']}")
            print("!!! Entering Global Network Settings !!! \n")
            globalsite = GetSiteParams()
            globalsite.groupNameHierarchy = 'Global'
            globalsiteid = SitesApiService(f"https://{ip}", Auth).getSite(globalsite)
            print(globalsiteid['response'][0]['id'])
            if rotation == 0:
                nwinfo = NetworkSettingsModel(TimezoneEnum.UTC)
                dns = DnsServerModel(x[5],x[6])
                motm = MessageOfTheDayModel(x[8])
                nwinfo.dhcpServer = [f"{x[4]}"]
                nwinfo.dnsServer = dns
                nwinfo.ntpServer = [f"{x[7]}"]
                motm.retainExistingBanner = False
                nwinfo.messageOfTheday = motm
                nwsetting = NetworkSettingsRequest(nwinfo)
                networkupdate = NetworkSettingsApiService(f"https://{ip}", Auth).createNetwork(
                    globalsiteid['response'][0]['id'], nwsetting)
                print(networkupdate)
                print("!!! Network Settings Updated !!! \n")
                rotation = rotation + 1

def build_design(ip):
    curretdir = os.getcwd()
    sitepath = 'C:/Users/admin/PycharmProjects/pythonProject/.venv/SDA/SDA/BatchFiles/DNAC_NW.csv'
    Globalpath = 'C:/Users/admin/PycharmProjects/pythonProject/.venv/SDA/SDA/BatchFiles/Global_pool.csv'
    print("!!! Gathering the Security Token from Catalyst Manager !!! \n")
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    print("!!! Entering the Global Pool and NW information to Catalyst Manager !!! \n")
    create_global_pool(Globalpath, Auth, ip)
    print("!!! Creating Sites and Reserving Ip Pools !!! \n")
    create_reserve_pool_site(sitepath, Auth, ip)

def global_creds(ip):
    cli_creds = {'cliCredential': [{'description':'CLI',
                                    'username':'netadmin',
                                    'password':'cisco',
                                    'enablePassword':'cisco'}],
                 'snmpV2cRead':[{'description':'SNMP read',
                            'readCommunity':'RO'}],
                 'snmpV2cWrite':[{'description':'SNMP write',
                             'writeCommunity':'RW'}]}

    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    create_creds = DiscoveryApiService(f"https://{ip}", Auth).createGlobalCredentials(cli_creds)
    print(create_creds['response']['taskId'])

def discovery(ip,name):
    discover_info = {'name': name,
                     'discoveryType': 'RANGE',
                     'ipAddressList': "192.168.1.4-192.168.1.9",
                     'ipFilterList': ["192.168.1.7"],
                     'protocolOrder':'ssh',
                     'netconfPort':'830',
                     'snmpROCommunity':'RO',
                     'snmpRWCommunity':'RW',
                     'enablePasswordList':['cisco'],
                     'passwordList':['cisco'],
                     'userNameList':['netadmin']}
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    discover = DiscoveryApiService(f"https://{ip}", Auth).startdiscovery(discover_info)
    return discover['response']['taskId']

def discovery_fusion(ip,name):
    discover_info = {'name': name,
                     'discoveryType': 'SINGLE',
                     'ipAddressList': "192.168.1.7",
                     'protocolOrder':'ssh',
                     'snmpROCommunity':'RO',
                     'snmpRWCommunity':'RW',
                     'enablePasswordList':['cisco'],
                     'passwordList':['cisco'],
                     'userNameList':['netadmin']}
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    discover = DiscoveryApiService(f"https://{ip}", Auth).startdiscovery(discover_info)
    return discover['response']['taskId']

def task(taskid,ip):
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    taskval = TaskApiService(f"https://{ip}", Auth).getTaskById(taskid)
    print(taskval)
    return taskval

def discovered_devices(ip,discoveryid):
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    discover_dev = DiscoveryApiService(f"https://{ip}", Auth).discovereddevices(discoveryid)
    print('!! Discovered Devices !!')
    return discover_dev

def assign_2_site(ip,device):
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    siteid = SitesApiService(f"https://{ip}", Auth).getSite()
    for x in (siteid['response']):
        if x['name'] == 'SJC-04':
            sitid_id = x['id']
    for x in device:
        device_list = {"device": [{"ip":x}]}
        dev_ip = DiscoveryApiService(f"https://{ip}", Auth).assign_to_site(sitid_id, device_list)
        print(dev_ip)


def create_underlay(ip):
    build_design(ip)
    global_creds(ip)
    rand = random.randint(1, 999)
    a = discovery(ip, 'Fabric')
    discover_check = task(a, ip)
    if discover_check['response']['progress'] == 'Failed to create discovery' and discover_check['response'][
        'failureReason'] == 'NCDS12001: Discovery already exists with the same name':
        print('!! Discovery with same name exists !! \n')
        a = discovery(ip, 'Fabric_' + str(rand))
    time.sleep(20)
    discover_check = task(a, ip)
    print(discover_check['response'])
    while 'status' not in discover_check['response']['data']:
        discover_check = task(a, ip)
        time.sleep(10)
    print('!! Discovery Successfull !!\n')
    print('!! Discovered Devices !!\n')
    device_in = discovered_devices(ip, discover_check['response']['progress'])
    devlist = []
    for de in device_in['response']:
        print(de['managementIpAddress'])
        devlist.append(de['managementIpAddress'])
    print(f'!! Devices Assigned to site {devlist} !!')
    assign_2_site(ip, devlist)
    a = discovery_fusion(ip, 'FUSION')
    discover_check = task(a, ip)
    if discover_check['response']['progress'] == 'Failed to create discovery' and discover_check['response'][
        'failureReason'] == 'NCDS12001: Discovery already exists with the same name':
        print('!! Discovery with same name exists !! \n')
        a = discovery(ip, 'Fabric_' + str(rand))
    time.sleep(20)
    discover_check = task(a, ip)
    print(discover_check['response'])
    while 'status' not in discover_check['response']['data']:
        discover_check = task(a, ip)
        time.sleep(10)
    print('!! Discovery Successfull !!\n')
    print('!! Discovered Devices !!\n')
    device_in = discovered_devices(ip, discover_check['response']['progress'])
    devlist = []
    for de in device_in['response']:
        print(de['managementIpAddress'])
        devlist.append(de['managementIpAddress'])
    print(f'!! Devices Assigned to site {devlist} !!')
    assign_2_site(ip, devlist)
    print('!! Underlay Build up successfully completed !!\n')

def ise_integration(ip,iseip):
    print('!! Integrating ISE and Catalyst Center !!\n')
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    ise_info = {'authenticationPort':1812,'accountingPort':1813,'ciscoIseDtos':[{'fqdn':'ISE-LAB.demo.local','password':'C1sco12345','ipAddress':f'{iseip}','subscriberName':'pxgrid_client_1662589467','userName':'admin'}],'ipAddress':f'{iseip}',
                'isIseEnabled':True,'port':'43','protocol':'RADIUS','retries':'3','sharedSecret':'C1sco12345','timeoutSeconds':'10','role':'primary'}
    print('!! Pushed ISE Info in DNAC !!\n')
    ise = ise_dnac_integration(f"https://{ip}", Auth).ise_add(ise_info)
    time.sleep(20)
    ise_status = ise_dnac_integration(f"https://{ip}", Auth).ise_status()
    print(ise_status)
    id = ise_status['aaaServerSettingId']
    accept_cert = ise_status['steps'][0]['certAcceptedByUser']
    status = ise_status['overallStatus']
    if accept_cert == False:
        cert = {'isCertAcceptedByUser':True}
        ise_accept_cert = ise_dnac_integration(f"https://{ip}", Auth).ise_accept_cert(id,cert)
    ise_status = ise_dnac_integration(f"https://{ip}", Auth).ise_status()
    status = ise_status['overallStatus']
    print(status)
    while status != 'COMPLETE':
        ise_status = ise_dnac_integration(f"https://{ip}", Auth).ise_status()
        status = ise_status['overallStatus']
        print(status)
        time.sleep(10)
    print('!! Integration completed successfully !!\n')
    time.sleep(5)

def add_ise_2_design(ip,iseip):
    print('!! Adding the ISE server to the Design in Catalyst Center !! \n')
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    siteid = SitesApiService(f"https://{ip}", Auth).getSite()
    for x in (siteid['response']):
        if x['name'] == 'Global':
            sitid_id = x['id']
    nwinfo ={"settings": {'clientAndEndpoint_aaa':{'servers':'ISE','ipAddress':f'{iseip}','network':f'{iseip}','protocol':'RADIUS','sharedSecret':'C1sco12345'},'timezone':'UTC'}}
    networkupdate = NetworkSettingsApiService(f"https://{ip}", Auth).updateNetwork(sitid_id,nwinfo)
    print('!! Successfully Updated the ISE server !!\n')
    time.sleep(5)

def provision(ip):
    print('!! Provisioning the Devices !!')
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    siteid = SitesApiService(f"https://{ip}", Auth).getSite()
    for x in (siteid['response']):
        if x['name'] == 'SJC-04':
            sitid_id = x['id']
    provisionfinal = []
    deviceid = DevicesApiService(f"https://{ip}", Auth).getDeviceList()
    for x in (deviceid['response']):
        provisionfinal.append({'siteId': sitid_id, 'networkDeviceId': x['id']})
        print(f'!! Network device with ID {x['id']} submitted for provisioning !!\n')

    pr = provisionservice(f"https://{ip}", Auth).provision_device(provisionfinal)
    print(pr)
    if 'message' in pr['response']:
        if re.search(
                'Device Provisioning failed. Cannot provision already provisioned device with networkDeviceId = (.*)',
                pr['response']['detail']):
            print('!! Re-Provisioning Devices !!\n')
            provisionfinal.clear()
            getdevice = provisionservice(f"https://{ip}", Auth).get_provision()
            print(getdevice)
            for y in getdevice['response']:
                provisionfinal.append(y)
            pr = provisionservice(f"https://{ip}", Auth).re_provision_device(provisionfinal)

    print(pr)
    taskval = []
    task = TaskApiService(f"https://{ip}", Auth).taskdetail(pr['response']['taskId'])
    timeout = time.time() + 600   # 10 minutes from now
    timeout_start = time.time()
    for ta in task['response']:
        taskval.append(ta['status'])
    while 'PENDING' in taskval:
        if time.time()>timeout:
            print('!!Execution took More than 10 Mins ..  Error Below!! \n')
            print(task)
            break
        taskval.clear()
        task = TaskApiService(f"https://{ip}", Auth).taskdetail(pr['response']['taskId'])
        for ta in task['response']:
            taskval.append(ta['status'])
        print(task)
        time.sleep(10)


    print(f'!! Successfully Provisioned the device !!\n')


def createfabric(ip):
    print('!! Creating Fabric Site !!\n')
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    siteid = SitesApiService(f"https://{ip}", Auth).getSite()
    for x in (siteid['response']):
        if x['name'] == 'SJC-04':
            sitid_id = x['id']
    fabinfo = [{'siteId':sitid_id,'authenticationProfileName':'Closed Authentication','isPubSubEnabled':True}]
    fab_site = SDAApiService(f"https://{ip}", Auth).addFabricSites(fabinfo)
    print(fab_site)
    if 'message' in fab_site['response']:
        if re.search('Bad Request', fab_site['response']['message']):
            print(fab_site['response']['detail'])
            pass

    else:
        task = TaskApiService(f"https://{ip}", Auth).taskdetail(fab_site['response']['taskId'])
        timeout = time.time() + 600  # 10 minutes from now
        timeout_start = time.time()
        while task['response'][0]['status'] != 'SUCCESS':
            if time.time() > timeout:
                print('!!Execution took More than 10 Mins ..  Error Below!! \n')
                print(task)
                break
            else:
                task = TaskApiService(f"https://{ip}", Auth).taskdetail(fab_site['response']['taskId'])
                print(task)
                time.sleep(2)

    print('!! Successfully created the Fabric Site at Site SJC-04 !!\n')

    time.sleep(5)


def create_VN(ip):
    print('!! Creating Virtual Networks !!\n')
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    fab = SDAApiService(f"https://{ip}", Auth).gerFabricSites()
    fabid = fab['response'][0]['id']
    VN = ['GUEST','CAMPUS']
    vninfo = []
    for v in VN:
        vninfo.append({'virtualNetworkName':v,'fabricIds':[fabid]})
    create_vn = SDAApiService(f"https://{ip}", Auth).add_VN(vninfo)
    if 'message' in  create_vn['response']:
        if re.search('Bad Request', create_vn['response']['message']):
            print(create_vn['response']['detail'])
            pass

    else:
        task = TaskApiService(f"https://{ip}", Auth).taskdetail(create_vn['response']['taskId'])
        timeout = time.time() + 600  # 10 minutes from now
        timeout_start = time.time()
        taskval = []
        for ta in task['response']:
            taskval.append(ta['status'])
        while 'PENDING' in taskval:
            if time.time() > timeout:
                print('!!Execution took More than 10 Mins ..  Error Below!! \n')
                print(task)
                break
            taskval.clear()
            task = TaskApiService(f"https://{ip}", Auth).taskdetail(create_vn['response']['taskId'])
            for ta in task['response']:
                taskval.append(ta['status'])
            print(task)
            time.sleep(10)

    print(f'!! Successfully created VN !!\n')

    time.sleep(10)

def create_ip_pool(ip):
    print('!! Creating IP Pools in Virtual Networks !!\n')
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    fab = SDAApiService(f"https://{ip}", Auth).gerFabricSites()
    fabid = fab['response'][0]['id']
    ipoolinfo = []
    with open(f'C:/Users/admin/PycharmProjects/pythonProject/.venv/SDA/sdapool.json') as pool:
        dev = (json.loads(pool.read()))
    for x in (dev):
        print(f'!! updating the pool for VN {x} !!\n')
        if len(dev[x])>1:
            for pool in dev[x]:
                print(f'!! Updating the Pool {pool[1]} in VN {x} !!\n')
                ipoolinfo = [{"fabricId": fabid, "virtualNetworkName": x, "ipPoolName": pool[0], "vlanName": pool[1],
                              "vlanId": pool[2], "trafficType": pool[3], "isCriticalPool": pool[4],
                              "isLayer2FloodingEnabled": pool[5], "isWirelessPool": pool[6],"isIpDirectedBroadcast":pool[7],"isIntraSubnetRoutingEnabled":pool[8],"isMultipleIpToMacAddresses":pool[9]}]
                print(ipoolinfo)
                anycast = SDAApiService(f"https://{ip}", Auth).add_ip_pools(ipoolinfo)
                print(anycast)
                if 'message' in anycast['response']:
                    if re.search('Bad Request', anycast['response']['message']):
                        print(anycast['response']['detail'])
                        pass
                else:
                    task = TaskApiService(f"https://{ip}", Auth).taskdetail(anycast['response']['taskId'])
                    print(task)
                    timeout = time.time() + 600  # 10 minutes from now
                    timeout_start = time.time()
                    while task['response'][0]['status'] != 'SUCCESS':
                        if time.time() > timeout:
                            print('!!Execution took More than 10 Mins ..  Error Below!! \n')
                            print(task)
                            break
                        else:
                            task = TaskApiService(f"https://{ip}", Auth).taskdetail(anycast['response']['taskId'])
                            print(task)
                            time.sleep(2)


        print(f'!! Updating the Pool {dev[x][0][1]} in VN {x} !!\n')
        ipoolinfo = [{"fabricId": fabid, "virtualNetworkName": x, "ipPoolName": dev[x][0][0], "vlanName": dev[x][0][1],
                       "vlanId": dev[x][0][2], "trafficType": dev[x][0][3], "isCriticalPool": dev[x][0][4],
                       "isLayer2FloodingEnabled": dev[x][0][5], "isWirelessPool": dev[x][0][6], "isIpDirectedBroadcast": dev[x][0][7],
                       "isIntraSubnetRoutingEnabled": dev[x][0][8], "isMultipleIpToMacAddresses": dev[x][0][9]}]
        anycast = SDAApiService(f"https://{ip}", Auth).add_ip_pools(ipoolinfo)
        print(anycast)
        if 'message' in anycast['response']:
            if re.search('Bad Request', anycast['response']['message']):
                print(anycast['response']['detail'])
                pass
        else:

            task = TaskApiService(f"https://{ip}", Auth).taskdetail(anycast['response']['taskId'])
            print(task)
            timeout = time.time() + 600  # 10 minutes from now
            timeout_start = time.time()
            while task['response'][0]['status'] != 'SUCCESS':
                if time.time() > timeout:
                    print('!!Execution took More than 10 Mins ..  Error Below!! \n')
                    print(task)
                    break
                else:
                    task = TaskApiService(f"https://{ip}", Auth).taskdetail(anycast['response']['taskId'])
                    print(task)
                    time.sleep(2)


    print(f'!! Successfully updated the pools!!')

def add_border_cp_edge(ip):
    print('!! Adding Devices the fabric Role !!\n')
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    fab = SDAApiService(f"https://{ip}", Auth).gerFabricSites()
    fabid = fab['response'][0]['id']
    deviceid = DevicesApiService(f"https://{ip}", Auth).getDeviceList()
    bdr_cp = ['192.168.1.4','192.168.1.5']
    edges = ['192.168.1.8','192.168.1.9']
    devaddinfo =[]
    for x in (deviceid['response']):

        if x['managementIpAddress'] in bdr_cp:
            print(f'!!Adding the role BDR/CP Role on device {x['managementIpAddress']} !!\n')
            devaddinfo = [{"networkDeviceId":x['id'],"fabricId":fabid,"deviceRoles":["CONTROL_PLANE_NODE","BORDER_NODE"],"borderDeviceSettings":{"borderTypes":["LAYER_3"],"layer3Settings":{"localAutonomousSystemNumber":"65001","isDefaultExit":True,'importExternalRoutes':False}}}]
            devpush = SDAApiService(f"https://{ip}", Auth).add_fabric_devices(devaddinfo)
            print(devpush)
            if 'message' in devpush['response']:
                if re.search('Bad Request', devpush['response']['message']):
                    print(devpush['response']['detail'])
                    pass
            else:
                task = TaskApiService(f"https://{ip}", Auth).taskdetail(devpush['response']['taskId'])
                timeout = time.time() + 600  # 10 minutes from now
                timeout_start = time.time()
                while task['response'][0]['status'] != 'SUCCESS':
                    if time.time() > timeout:
                        print('!!Execution took More than 10 Mins ..  Error Below!! \n')
                        print(task)
                        break
                    else:
                        task = TaskApiService(f"https://{ip}", Auth).taskdetail(devpush['response']['taskId'])
                        print(task)
                        time.sleep(2)
        elif x['managementIpAddress'] in edges:
            print(f'!!Adding the role Edge Role on device {x['managementIpAddress']} !!\n')
            devaddinfo = [{"networkDeviceId":x['id'],"fabricId":fabid,"deviceRoles":["EDGE_NODE"]}]
            devpush = SDAApiService(f"https://{ip}", Auth).add_fabric_devices(devaddinfo)
            print(devpush)
            if 'message' in devpush['response']:
                if re.search('Bad Request', devpush['response']['message']):
                    print(devpush['response']['detail'])
                    pass
            else:
                task = TaskApiService(f"https://{ip}", Auth).taskdetail(devpush['response']['taskId'])
                timeout = time.time() + 600  # 10 minutes from now
                timeout_start = time.time()
                while task['response'][0]['status'] != 'SUCCESS':
                    if time.time() > timeout:
                        print('!!Execution took More than 10 Mins ..  Error Below!! \n')
                        print(task)
                        break
                    else:
                        task = TaskApiService(f"https://{ip}", Auth).taskdetail(devpush['response']['taskId'])
                        print(task)
                        time.sleep(2)


def create_transit(ip):
    print('!! Creating Transit !!\n')
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    trans = [{"name":"IP Transit","type":"IP_BASED_TRANSIT","ipTransitSettings":{"routingProtocolName":"BGP","autonomousSystemNumber":"65000"}}]
    trans_create = SDAApiService(f"https://{ip}", Auth).create_transit(trans)
    print(trans_create)
    print('!! Successfully Created transit !!\n')
    if 'message' in trans_create['response']:
        if re.search('Bad Request', trans_create['response']['message']):
            print(trans_create['response']['detail'])
            pass
    time.sleep(15)

def border_auto(ip):
    print('!! Creating l3 Handoff !!\n')
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    fab = SDAApiService(f"https://{ip}", Auth).gerFabricSites()
    fabid = fab['response'][0]['id']
    fabinfo = {'fabricId':fabid}
    fabric = SDAApiService(f"https://{ip}", Auth).get_fab_devices(fabinfo)
    trans  = SDAApiService(f"https://{ip}", Auth).get_transit()
    print(trans)
    l3info = []
    for res in fabric['response']:
        if 'BORDER_NODE' in res['deviceRoles']:
            mgmtip = DevicesApiService(f"https://{ip}", Auth).getDeviceById(res['networkDeviceId'])
            if mgmtip['response']['managementIpAddress'] == '192.168.1.4':
                vn = {'CAMPUS':3001, 'GUEST':3002}
                for v in vn:
                    l3info.append(
                        {'networkDeviceId': res['networkDeviceId'], "fabricId": res['fabricId'],
                         "transitNetworkId": trans['response'][0]['id'], "interfaceName":'GigabitEthernet1/0/1','externalConnectivityIpPoolName':'SJC-BDR-HOF','virtualNetworkName':v,'vlanId':vn[v]})
                    print(l3info)

            if mgmtip['response']['managementIpAddress'] == '192.168.1.5':
                l3info.clear()
                vn = {'CAMPUS': 3003, 'GUEST': 3004}
                for v in vn:
                    l3info.append(
                        {'networkDeviceId': res['networkDeviceId'], "fabricId": res['fabricId'],
                         "transitNetworkId": trans['response'][0]['id'], "interfaceName": 'GigabitEthernet1/0/1',
                         'externalConnectivityIpPoolName': 'SJC-BDR-HOF', 'virtualNetworkName': v, 'vlanId': vn[v]})
                    print(l3info)
    l3handoff = SDAApiService(f"https://{ip}", Auth).l3handoff(l3info)
    print(l3handoff)
    if 'message' in l3handoff['response']:
        if re.search('Bad Request', l3handoff['response']['message']):
            print(l3handoff['response']['detail'])
            pass

    else:
        taskval = []
        task = TaskApiService(f"https://{ip}", Auth).taskdetailparent(l3handoff['response']['taskId'])
        timeout = time.time() + 600  # 10 minutes from now
        timeout_start = time.time()
        for ta in task['response']:
            taskval.append(ta['status'])
        while 'PENDING' in taskval:
            if time.time() > timeout:
                print('!!Execution took More than 10 Mins ..  Error Below!! \n')
                print(task)
                break
            taskval.clear()
            task = TaskApiService(f"https://{ip}", Auth).taskdetailparent(l3handoff['response']['taskId'])
            for ta in task['response']:
                taskval.append(ta['status'])
            print(task)
            time.sleep(10)



def runCommands(url: str, token: str, devices: list, commands: list) -> None:
    #
    # Run CLI commands
    #

    commandRunnerApiService = CommandRunnerApiService(f"https://{url}", token)
    taskApiService = TaskApiService(f"https://{url}", token)
    fileApiService = FileApiService(f"https://{url}", token)

    apiResponse = commandRunnerApiService.RunReadOnlyCommand(CommandRunnerModel(commands, devices))
    taskId = apiResponse['response']['taskId']

    #
    # Loop until task is completed andn File ID is available
    #
    completed = False
    while not completed:
        time.sleep(2)
        task = taskApiService.getTaskById(taskId)['response']
        # JSON is returned only when task is ready, hence try/except is used
        try:
            fileId = json.loads(task['progress'])['fileId']
            completed = True
        except ValueError as e:
            pass
    #
    # Obtain File ID when available
    #
    file = fileApiService.downloadFile(fileId)

    for item in file:
        if item['commandResponses']['SUCCESS'] != {}:
            for command in commands:
                text = item['commandResponses']['SUCCESS'].get(command)
        if item['commandResponses']['FAILURE'] != {}:
            for command in commands:
                text = item['commandResponses']['FAILURE'].get(command)
        if item['commandResponses']['BLOCKLISTED'] != {}:
            for command in commands:
                text = item['commandResponses']['BLOCKLISTED'].get(command)
    return text

def Project(url,token):
    project = ProjectRequest('Fusion_Automation')
    project_req = TemplateApiService(f"https://{url}",token).createProject(project)
    task_id = TaskApiService(f"https://{url}",token).getTaskById(project_req['response']['taskId'])
    project_id =task_id['response']['data']
    print('Project Created Successfully.\n')
    task1 = TaskApiService(f"https://{url}", token).taskdetail(project_req['response']['taskId'])
    timeout = time.time() + 600   # 10 minutes from now
    timeout_start = time.time()
    while task1['status'] != 'SUCCESS':
        if time.time() > timeout:
            print('!!Execution took More than 10 Mins ..  Error Below!! \n')
            print(task1)
            break
        else:
            task1 = TaskApiService(f"https://{url}", token).taskdetail(project_req['response']['taskId'])
            print(task1)
            time.sleep(2)
    print('!! Template created and provisioned successfully !!\n')
    time.sleep(10)
    return project_id

def createtemplate(rtr, prod_series,temp_name, project_name,content,projectid,url,token,fusion_mgmt):
    headers = {
        'X-Auth-Token': f'{token}',
        'Content-Type': "application/json",
    }
    device_info = ProductFamilyModel()
    device_info.productFamily = rtr
    #device_info.productType = prod_series
    temp_lang = 'JINJA'
    temp_req = TemplateRequest([device_info.__dict__],temp_lang,temp_name,project_name,'IOS-XE')
    temp_req.templateContent = content
    print(temp_req.__dict__)
    create_temp = requests.post(f'https://{url}/dna/intent/api/v1/template-programmer/project/{projectid}/template', headers=headers,
                                      verify=False,
                                      json=temp_req.__dict__)
    print(create_temp.json())
    task = requests.get(f'https://{url}/dna/intent/api/v1/task/{create_temp.json()["response"]["taskId"]}', headers=headers,
                                      verify=False,
                                      )
    print(task.json())
    if (task.json()['response']['progress']) != 'Successfully created template with name FUSION.demo.local. Template content has validation errors.':
        time.sleep(7)
        task = requests.get(f'https://{url}/dna/intent/api/v1/task/{create_temp.json()["response"]["taskId"]}',
                            headers=headers,
                            verify=False,
                            )
    time.sleep(7)
    task = requests.get(f'https://{url}/dna/intent/api/v1/task/{create_temp.json()["response"]["taskId"]}', headers=headers,
                                      verify=False,
                                      )

    version_req = VersionTemplateRequest()
    version_req.comments = 'this is 1st commit'
    temp_id = json.loads(task.json()['response']['data'])
    version_req.templateId = temp_id['templateId']
    time.sleep(10)
    version_push = TemplateApiService(f"https://{url}",token).versionTemplate(version_req)
    temp_target_info = TemplateTargetInfoModel(TemplateTargetInfoTypeEnum.MANAGED_DEVICE_IP,temp_id['templateId'])
    temp_target_info.id = fusion_mgmt
    deploy_temp_req = DeployTemplateRequest([temp_target_info], temp_id['templateId'])
    deploy_temp = TemplateApiService(f"https://{url}",token).deploytemplate(deploy_temp_req)
    print(deploy_temp)
    deploy = re.search('.*Template Deployemnt Id: (.*)',deploy_temp['deploymentId'])
    task1 = TemplateApiService(f"https://{url}", token).getDeployment(deploy.group(1))
    timeout = time.time() + 600   # 10 minutes from now
    timeout_start = time.time()
    while task1['status'] != 'SUCCESS':
        if time.time() > timeout:
            print('!!Execution took More than 10 Mins ..  Error Below!! \n')
            print(task1)
            break
        else:
            task1 = TemplateApiService(f"https://{url}", token).getDeployment(deploy.group(1))
            print(task1)
            time.sleep(2)
    print('!! Template created and provisioned successfully !!\n')


def temp_content(url,token):
    fusion_temp = ''
    fab = SDAApiService(f"https://{url}", token).gerFabricSites()
    fabid = fab['response'][0]['id']
    number = 1
    site_dict = {}
    border_list = []
    dev_family = ''
    dev_type = ''
    fusion_mgmt = ''
    fusion_dict = {}
    localas = {}
    print("Collecting Devices in the Sites !! \n")
    border = "Border Devices in the site "
    num = 1
    bordern = SDAApiService(f"https://{url}", token).getSdaDeviceInfo(fabid)
    print(bordern)
    for bor in bordern['response']:
        print(bor['networkDeviceId'])
        border= border + f'\n {num}. Device with NwId {bor["networkDeviceId"]}'
        num = num+1
        border_list.append(bor["networkDeviceId"])
        localas.update({bor["networkDeviceId"]:bor['borderDeviceSettings']['layer3Settings']['localAutonomousSystemNumber']})

    print(f'{border} ')
    print(border_list)
    for ext_con in border_list:
        print("Collecting the Fusion Hostname and Uplink !!\n")
        cdp_intf = runCommands(url, token, [f'{ext_con}'], [f'show cdp neighbor GigabitEthernet1/0/1 detail'])
        print(cdp_intf)
        Fusion_hostname = re.search('Device ID: (.*)', str(cdp_intf))
        Fusion_Intf = re.search('Port ID \(outgoing port\): (.*)', str(cdp_intf))
        Fusion_Param = GetDeviceListParams()
        Fusion_Param.hostname = [f'{Fusion_hostname.group(1)}']
        print(f"Fusion {Fusion_hostname.group(1)} has uplink {Fusion_Intf.group(1)} towards BDR {border}\n")
        Fusion = DevicesApiService(f"https://{url}", token).getDeviceList(Fusion_Param)
        dev_family = Fusion['response'][0]['family']
        dev_type = Fusion['response'][0]['type']
        fusion_mgmt = Fusion['response'][0]['dnsResolvedManagementAddress']
        hostname = runCommands(url, token, [f'{ext_con}'], [f'show run | sec hostname'])
        bdr_host = re.search('hostname (.*)', str(hostname))
        print(bdr_host.group(1))
        if Fusion['response'][0]['family'] == 'Routers':
            print('Fusion Device is a Router !!\n')
            bdrinfo = SDAApiService(f"https://{url}", token).getSdaBorderInfo(fabid, ext_con)
            for l3handoff in bdrinfo['response']:
                print(l3handoff)
                fusion_intf = ''
                fusion_bgp_nei = ''
                vrf = runCommands(url, token, [f'{ext_con}'], [f'show run interface vlan {l3handoff["vlanId"]}'])
                vrf_info = re.search('vrf forwarding (.*)', str(vrf))
                print(f'Running Border Automation on Fusion for VRF {vrf_info.group(1)}\n')
                get_vrf = runCommands(url, token, [f'{ext_con}'], [f'show run vrf {vrf_info.group(1)}'])
                rd_info = re.search('rd (.*)', get_vrf)
                fusion_cfg = re.search(f'(vrf def.* {rd_info.group(1)})', get_vrf, re.DOTALL)
                fusion_cfg_new = fusion_cfg.group(0) + "\n exit-address-family\n"
                local_ip = re.split('/', l3handoff['localIpAddress'])
                remote_ip = re.split('/', l3handoff['remoteIpAddress'])
                fusion_interface = f"""interface {Fusion_Intf.group(1)}.{l3handoff['vlanId']}\n encapsulation dot1Q {l3handoff['vlanId']}\n vrf forwarding {vrf_info.group(1)}\n ip address {remote_ip[0]} 255.255.255.252\n no ip redirects\n ip route-cache same-interface"""
                fusion_intf = fusion_intf + fusion_interface
                fusion_bgp_neigh = f""" maximum-paths 2\n neighbor {local_ip[0]} remote-as {localas[ext_con]}\n neighbor {local_ip[0]} activate\n neighbor {local_ip[0]} send-community both\n neighbor {local_ip[0]} update-source {Fusion_Intf.group(1)}.{l3handoff['vlanId']}\n neighbor {local_ip[0]} weight 65535"""
                fusion_bgp_nei = fusion_bgp_nei + fusion_bgp_neigh
                fusion_vrf_check = runCommands(url, token, [f"{Fusion['response'][0]['id']}"],
                                               [f'show run vrf {vrf_info.group(1)}'])
                print('Verifying whether VRF Definition is present in the Fusion !!\n')
                if re.search(f'vrf definition {vrf_info.group(1)}', fusion_vrf_check):
                    print('VRF Definition present, therefore skipping the VRF definition config!! \n')
                    fusion_temp = fusion_temp + '\n' + fusion_intf + f'\nrouter bgp 65000\n address-family ipv4 vrf {vrf_info.group(1)}\n' + fusion_bgp_nei + "\nexit-address-family"
                else:
                    print('VRF Definition not present, adding VRF definition config!! \n')
                    fusion_temp = fusion_temp + '\n' + fusion_cfg_new + fusion_intf + f'\nrouter bgp 65000\n address-family ipv4 vrf {vrf_info.group(1)}\n' + fusion_bgp_nei + "\nexit-address-family"
                print(f'Config generated for Fusion \n{fusion_temp}')
                time.sleep(5)


        fusion_dict.update({Fusion_hostname.group(1):fusion_temp})
    return fusion_dict,dev_family,dev_type,fusion_mgmt

def updatetemplate(rtr, prod_series,temp_name, project_name,content,projectid,url,token,fusion_mgmt,tempid):
    headers = {
        'X-Auth-Token': f'{token}',
        'Content-Type': "application/json",
    }
    device_info = ProductFamilyModel()
    device_info.productFamily = rtr
    #device_info.productType = prod_series
    temp_lang = 'JINJA'
    temp_req = TemplateRequest([device_info.__dict__],temp_lang,temp_name,project_name,'IOS-XE')
    temp_req.templateContent = content
    temp_req.id=tempid
    print(temp_req.__dict__)
    create_temp = requests.put(f'https://{url}/dna/intent/api/v1/template-programmer/template', headers=headers,
                                      verify=False,
                                      json=temp_req.__dict__)
    print(create_temp.json())
    task = requests.get(f'https://{url}/dna/intent/api/v1/task/{create_temp.json()["response"]["taskId"]}', headers=headers,
                                      verify=False,
                                      )
    if (task.json()['response']['progress']) != 'Successfully created template with name FUSION.demo.local. Template content has validation errors.':
        time.sleep(7)
    time.sleep(7)
    task = requests.get(f'https://{url}/dna/intent/api/v1/task/{create_temp.json()["response"]["taskId"]}', headers=headers,
                                      verify=False,
                                      )
    print(task)
    version_req = VersionTemplateRequest()
    version_req.comments = 'this is 1st commit'
    temp_id = tempid
    version_req.templateId = temp_id
    time.sleep(10)
    version_push = TemplateApiService(f"https://{url}",token).versionTemplate(version_req)
    temp_target_info = TemplateTargetInfoModel(TemplateTargetInfoTypeEnum.MANAGED_DEVICE_IP,tempid)
    temp_target_info.id = fusion_mgmt
    deploy_temp_req = DeployTemplateRequest([temp_target_info], tempid)
    deploy_temp = TemplateApiService(f"https://{url}",token).deploytemplate(deploy_temp_req)
    print(deploy_temp)
    deploy = re.search('.*Template Deployemnt Id: (.*)',deploy_temp['deploymentId'])
    print(deploy.group(1))
    task1 = TemplateApiService(f"https://{url}", token).getDeployment(deploy.group(1))
    timeout = time.time() + 600   # 10 minutes from now
    while task1['status'] != 'SUCCESS':
        if time.time() > timeout:
            print('!!Execution took More than 10 Mins ..  Error Below!! \n')
            print(task1)
            break
        else:
            task1 = TemplateApiService(f"https://{url}", token).getDeployment(deploy.group(1))
            print(task1)
            time.sleep(2)
    print('!! Template created and provisioned successfully !!\n')


def fusion_auto(ip):
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    print('Gathering Fabric Site Information !!\n')
    template = temp_content(ip, Auth)
    print('Verifying whether Project is present !!\n ')
    projectlist = GetlistProject()
    projectlist.name = 'Fusion_Automation'
    project_info = TemplateApiService(f"https://{ip}", Auth).getlistproject(projectlist)
    if not project_info:
        print('Project not present , Creating a new Project with Name Fusion_Automation !!\n')
        project = Project(ip, Auth)
    else:
        print('Project  present , gathering Project ID !!\n')
        project = project_info[0]['id']

    print('Verifying whether Template is present !!\n')
    temp_param = GetlistTemplate()

    for te in template[0]:
        temp_param.projectId = project
        temp_present = TemplateApiService(f'https://{ip}', Auth).getTemplate(temp_param)
        if not temp_present:
            print('Template Not Present, Creating and Deploying Template !!\n')
            createtemplate(template[1], template[2], te, 'FUSION_AUTOMATION', template[0][te], project, ip, Auth,
                           template[3])
        else:
            print('Template Present, Updating and Deploying Template !!\n')
            updatetemplate(template[1], template[2], te, 'FUSION_AUTOMATION', template[0][te], project, ip, Auth,
                           template[3], temp_present[0]['templateId'])
    print('TASK Completed')


def overlay_automation(ip,ise):
    create_underlay(ip)
    ise_integration(ip,ise)
    add_ise_2_design(ip,ise)
    provision(ip)
    createfabric(ip)
    create_VN(ip)
    create_ip_pool(ip)
    add_border_cp_edge(ip)
    create_transit(ip)
    border_auto(ip)
    try:
        fusion_auto(ip)
    except:
        fusion_auto(ip)
