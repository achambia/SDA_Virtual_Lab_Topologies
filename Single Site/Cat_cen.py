import shutil
import netmiko
from netmiko import ConnectHandler
import json
from SDA.SDA.api.SitesApiService import SitesApiService
from SDA.SDA.reqs.SiteRequest import SiteRequest
from SDA.SDA.enums.SiteTypeEnum import SiteTypeEnum
from SDA.SDA.reqs.GlobalPoolRequest import GlobalPoolRequest
from SDA.SDA.params.GetSiteParams import GetSiteParams
from SDA.SDA.enums.IPPoolTypeEnum import IPPoolTypeEnum
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
from SDA.SDA.enums.LanguageEnum import LanguageTypeEnum
from SDA.SDA.models.ProductFamilyModel import ProductFamilyModel
from SDA.SDA.reqs.VersionTemplateRequest import VersionTemplateRequest
from SDA.SDA.reqs.DeployTemplateRequest import DeployTemplateRequest
from SDA.SDA.models.TemplateTargetInfoModel import TemplateTargetInfoModel
from SDA.SDA.enums.TemplateTargetInfoTypeEnum import TemplateTargetInfoTypeEnum
import time
from SDA.SDA.api.SDAApiService import SDAApiService
from SDA.SDA.params.GetFabricSitesParams import GetFabricSitesParams
from SDA.SDA.params.GetlistProject import GetlistProject
from SDA.SDA.models.CommandRunnerModel import CommandRunnerModel
from SDA.SDA.params.GetSiteDeviceAssociationparam import GetSiteDeviceAssociationparam
from SDA.SDA.params.GetDeviceListParams import GetDeviceListParams
from SDA.SDA.api.DevicesApiService import DevicesApiService
from SDA.SDA.params.GetlistTemplate import GetlistTemplate
from SDA.SDA.reqs.GlobalCredentialRequest import GlobalCredentialRequest
from SDA.SDA.models.CliCredentialModel import CliCredentialModel
from SDA.SDA.models.SnmpV2cCredentialModel import SnmpV2cCredentialModel
from SDA.SDA.api.DiscoveryApiService import DiscoveryApiService
from SDA.SDA.api.AuthenticationServerApiService import ise_dnac_integration
from SDA.SDA.api.ProvisionApiService import provisionservice
import random
def copy_file(file):
    try:
        shutil.rmtree('C:/Users/admin/PycharmProjects/pythonProject/.venv/SDA')
        shutil.copytree(f'C:/Program Files/Git/cmd/{file}',
                        'C:/Users/admin/PycharmProjects/pythonProject/.venv/SDA')
    except Exception as e:
        print(e)
        shutil.copytree(f'C:/Program Files/Git/cmd/{file}','C:/Users/admin/PycharmProjects/pythonProject/.venv/SDA')

def device_config(rtr,config):
    net_connect = ConnectHandler(
        device_type="cisco_xe",
        host=rtr,
        username="netadmin",
        password="cisco",
    )

    output = net_connect.send_config_set(config,read_timeout=300)
    print(output)

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

def provision(ip):
    Auth = AuthenticationApiService('sysadmin', 'C1sco12345', f"https://{ip}").authenticate()
    siteid = SitesApiService(f"https://{ip}", Auth).getSite()
    for x in (siteid['response']):
        if x['name'] == 'SJC-04':
            sitid_id = x['id']
    taskid = []
    deviceid = DevicesApiService(f"https://{ip}", Auth).getDeviceList()
    for x in (deviceid['response']):
        provision_dev = [{'siteId': sitid_id, 'networkDeviceId': x['id']}]
        print(provision_dev)
        pr = provisionservice(f"https://{ip}", Auth).provision_device(provision_dev)
        print(pr)
        taskid.append(pr['response']['taskId'])

    while True:
        for task in taskid:
            taskval = TaskApiService(f"https://{ip}", Auth).getTaskById(task)
            print(taskval)
















#ise_integration('169.200.200.130','169.200.200.100')
#add_ise_2_design('169.200.200.130','169.200.200.100')
provision('169.200.200.130')
