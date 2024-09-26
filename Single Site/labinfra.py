import csv
import os
import re
import subprocess
import sys
from SDA.SDA.api.deploy_ovf import deploy_ise,deploy_cml,deploy_wlc,deploy_labrouter,deploy_cc
from SDA.SDA.api.reachability import ping_test
from SDA.SDA.api.router_uplink import labrtr
import time
from SDA.SDA.api.CML import cml_tasks
from git import Repo
from SDA.SDA.api.WIN_info import getvms
from SDA.SDA.api.portgroup import portgroup
import json
from SDA.SDA.api.device_info import device_net
from SDA.SDA.api.deploy_vcenter_ovf import deploy_vcenter_wlc,deploy_vcenter_labrouter,deploy_vcenter_cml,deploy_vcenter_ise,deploy_vcenter_cc
import shutil
import warnings
warnings.filterwarnings(action='ignore', module='.*paramiko.*')


def labinfra(gitval,sda_build):
    try:
        topo = {}
        # DEfault IP's for VM's
        cml = '169.100.100.2'
        ise = '169.200.200.100'
        dnacip = '169.200.200.130'
        wlc = '169.200.200.3'
        # Fetching User Input for VM Build
        print('!!! Step 1 , Build ISE , CML and WLC VMs !!! \n')
        vm_input = input('!!! Do you wish to Deploy CML, ISE or vWLC VMs (y/Y)? [y]:: ') or 'y'
        if vm_input.lower() == 'y':
            vm_deployment_values = []
            vm_to_be_deployed = []
            print('!! Please ensure that the Windows Machine is Installed !! \n')
            win_server_esxi_ip = input('Enter the IP of the ESXI/Vcenter Server where the Windows Server is Installed ::: ')
            win_server_esxi_user = input('Enter the User of the ESXI/Vcenter Server where the Windows Server is Installed ::: ')
            win_server_esxi_password = input('Enter the Password of the ESXI/Vcenter Server where the Windows Server is Installed ::: ')
            win_info = getvms(win_server_esxi_ip,win_server_esxi_user,win_server_esxi_password,'443')
            win_input = '\n'
            for win in win_info:
                win_input = win_input + str(win) + '. '+ win_info[win] + '\n'
            windows = input('Enter the Number which identifies the Windows Machine deployed ' + win_input+'\n  :::::: ')
            win_esxi_data = (device_net(win_server_esxi_ip, win_server_esxi_user, win_server_esxi_password, '443', win_info[int(windows)]))

            if isinstance(win_esxi_data['network 1'],dict):
                print('!!Distributed Port Group Detected on Network Interface 1 of Windows !!\n')
                pg1 = portgroup(win_server_esxi_ip, win_server_esxi_user, win_server_esxi_password, '443', win_esxi_data['network 1']['swuuid'],win_esxi_data['network 1']['pgkey'])
                win_esxi_data['network 1'] = str(pg1)
            if isinstance(win_esxi_data['network 2'],dict):
                print('!!Distributed Port Group Detected on Network Interface 2 of Windows !!\n')
                pg2 = portgroup(win_server_esxi_ip, win_server_esxi_user, win_server_esxi_password, '443', win_esxi_data['network 2']['swuuid'],win_esxi_data['network 2']['pgkey'])
                win_esxi_data['network 1'] = str(pg2)
            if isinstance(win_esxi_data['network 3'],dict):
                print('!!Distributed Port Group Detected on Network Interface 3 of Windows !!\n')
                pg3 = portgroup(win_server_esxi_ip, win_server_esxi_user, win_server_esxi_password, '443', win_esxi_data['network 3']['swuuid'],win_esxi_data['network 3']['pgkey'])
                win_esxi_data['network 1'] = str(pg3)
            vcenter_esxi = input('!!! Do you wish to deploy VMs in \n 1. Standalone ESXI Host \n 2. Vcenter Server \n    ::::: ') or '1'
            cml_deploy_input = input('!!! Do you wish to deploy CML VM (Y/N) ? [Y]::: ') or 'y'
            if cml_deploy_input.lower() == 'y':
                if vcenter_esxi == '1':
                    cml_ds = input(f"!!! Enter the Datastore for the Host where CML needs to be deployed [{win_esxi_data['datastore']}]::: ") or win_esxi_data['datastore']
                    cml_host = input(f"!!! Enter the IP/FQDN for the Host where CML needs to be deployed [{win_server_esxi_ip}]::: ") or win_server_esxi_ip
                    cml_password = input(f"!!! Enter the password for the Host where CML needs to be deployed [{win_server_esxi_password}]::: ") or win_server_esxi_password
                    cml_user = input(f"!!! Enter the user for the Host where CML needs to be deployed [{win_server_esxi_user}]::: ") or win_server_esxi_user
                    cml_vm_name = input('!!! Enter the name for the CML VM [CML] ::: ') or 'CML'
                    vm_to_be_deployed.append('CML')
                elif vcenter_esxi == '2':
                    cml_ds = input(f"!!! Enter the Datastore for the Host where CML needs to be deployed [{win_esxi_data['datastore']}]::: ") or win_esxi_data['datastore']
                    cml_vcenter = input(f"!!! Enter the IP/FQDN for the Vcenter [{win_server_esxi_ip}]::: ") or win_server_esxi_ip
                    cml_password = input(f"!!! Enter the password for the vCenter where CML needs to be deployed [{win_server_esxi_password}]::: ") or win_server_esxi_password
                    cml_user = input(f"!!! Enter the user for the vCenter where CML needs to be deployed [{win_server_esxi_user}]::: ") or win_server_esxi_user
                    cml_host = input(f"!!! Enter the IP/FQDN for the Host where CML needs to be deployed [{win_esxi_data['host']}]::: ") or win_esxi_data['host']
                    cml_vm_name = input('!!! Enter the name for the CML VM [CML] ::: ') or 'CML'
                    vm_to_be_deployed.append('CML')

            ise_deploy_input = input('!!! Do you wish to deploy ISE VM (Y/N) ? [Y]::: ') or 'y'
            if ise_deploy_input.lower() == 'y':
                if vcenter_esxi =='1':
                    ise_ds = input(f"!!! Enter the Datastore for the Host where ISE needs to be deployed [{win_esxi_data['datastore']}]::: ") or win_esxi_data['datastore']
                    ise_host = input(f"!!! Enter the IP/FQDN for the Host where ISE needs to be deployed [{win_server_esxi_ip}]::: ") or win_server_esxi_ip
                    ise_password = input(f"!!! Enter the password for the Host where ISE needs to be deployed [{win_server_esxi_password}]::: ") or win_server_esxi_password
                    ise_user = input(f"!!! Enter the user for the Host where ISE needs to be deployed [{win_server_esxi_user}]::: ") or win_server_esxi_user
                    ise_vm_name = input('!!! Enter the name for the ISE VM [ISE] ::: ') or 'ISE'
                    vm_to_be_deployed.append('ISE')
                elif vcenter_esxi =='2':
                    ise_ds = input(f"!!! Enter the Datastore for the Host where ISE needs to be deployed [{win_esxi_data['datastore']}]::: ") or win_esxi_data['datastore']
                    ise_vcenter = input(f"!!! Enter the IP/FQDN for the vCenter [{win_server_esxi_ip}]::: ") or win_server_esxi_ip
                    ise_password = input(f"!!! Enter the password for the vCenter where ISE needs to be deployed [{win_server_esxi_password}]::: ") or win_server_esxi_password
                    ise_user = input(f"!!! Enter the user for the vCenter where ISE needs to be deployed [{win_server_esxi_user}]::: ") or win_server_esxi_user
                    ise_vm_name = input('!!! Enter the name for the ISE VM [ISE] ::: ') or 'ISE'
                    ise_host = input(f"!!! Enter the IP/FQDN for the Host where ISE needs to be deployed [{win_esxi_data['host']}]::: ") or win_esxi_data['host']
                    vm_to_be_deployed.append('ISE')
            dnac_deploy_input = input('!!! Do you wish to deploy Catalyst Center VM (Y/N) ? [Y]::: ') or 'y'
            if dnac_deploy_input.lower() == 'y':
                if vcenter_esxi =='1':
                    dnac_ds = input(f"!!! Enter the Datastore for the Host where DNAC needs to be deployed [{win_esxi_data['datastore']}]::: ") or win_esxi_data['datastore']
                    dnac_host = input(f"!!! Enter the IP/FQDN for the Host where DNAC needs to be deployed [{win_server_esxi_ip}]::: ") or win_server_esxi_ip
                    dnac_password = input(f"!!! Enter the password for the Host where DNAC needs to be deployed [{win_server_esxi_password}]::: ") or win_server_esxi_password
                    dnac_user = input(f"!!! Enter the user for the Host where DNAC needs to be deployed [{win_server_esxi_user}]::: ") or win_server_esxi_user
                    dnac_vm_name = input('!!! Enter the name for the DNAC VM [DNAC] ::: ') or 'DNAC'
                    vm_to_be_deployed.append('DNAC')
                elif vcenter_esxi =='2':
                    dnac_ds = input(f"!!! Enter the Datastore for the Host where DNAC needs to be deployed [{win_esxi_data['datastore']}]::: ") or win_esxi_data['datastore']
                    dnac_vcenter = input(f"!!! Enter the IP/FQDN for the vCenter [{win_server_esxi_ip}]::: ") or win_server_esxi_ip
                    dnac_password = input(f"!!! Enter the password for the vCenter where DNAC needs to be deployed [{win_server_esxi_password}]::: ") or win_server_esxi_password
                    dnac_user = input(f"!!! Enter the user for the vCenter where DNAC needs to be deployed [{win_server_esxi_user}]::: ") or win_server_esxi_user
                    dnac_vm_name = input('!!! Enter the name for the DNAC VM [DNAC] ::: ') or 'DNAC'
                    dnac_host = input(f"!!! Enter the IP/FQDN for the Host where DNAC needs to be deployed [{win_esxi_data['host']}]::: ") or win_esxi_data['host']
                    vm_to_be_deployed.append('ISE')



            wlc_deploy_input = input('!!! Do you wish to deploy WLC VM (Y/N) ? [Y]::: ') or 'y'
            if wlc_deploy_input.lower() == 'y':
                if vcenter_esxi =='1':
                    wlc_ds = input(f"!!! Enter the Datastore for the Host where WLC needs to be deployed [{win_esxi_data['datastore']}]::: ") or win_esxi_data['datastore']
                    wlc_host = input(f"!!! Enter the IP/FQDN for the Host where WLC needs to be deployed [{win_server_esxi_ip}]::: ") or win_server_esxi_ip
                    wlc_password = input(f"!!! Enter the password for the Host where WLC needs to be deployed [{win_server_esxi_password}]::: ") or win_server_esxi_password
                    wlc_user = input(f"!!! Enter the user for the Host where WLC needs to be deployed [{win_server_esxi_user}]::: ") or win_server_esxi_user
                    wlc_vm_name = input('!!! Enter the name for the WLC VM [WLC] :::') or 'WLC'
                    vm_to_be_deployed.append('WLC')
                elif vcenter_esxi =='2':
                    wlc_ds = input(f"!!! Enter the Datastore for the Host where WLC needs to be deployed [{win_esxi_data['datastore']}]::: ") or win_esxi_data['datastore']
                    wlc_vcenter = input(f"!!! Enter the IP/FQDN for the vCenter [{win_server_esxi_ip}]::: ") or win_server_esxi_ip
                    wlc_password = input(f"!!! Enter the password for the vCenter where WLC needs to be deployed [{win_server_esxi_password}]::: ") or win_server_esxi_password
                    wlc_user = input(f"!!! Enter the user for the vCenter where WLC needs to be deployed [{win_server_esxi_user}]::: ") or win_server_esxi_user
                    wlc_host = input(f"!!! Enter the IP/FQDN for the Host where WLC needs to be deployed [{win_esxi_data['host']}]::: ") or win_esxi_data['host']
                    wlc_vm_name = input('!!! Enter the name for the WLC VM [WLC] :::') or 'WLC'
                    vm_to_be_deployed.append('WLC')


            labrouter_deploy_input = input('!!! Do you wish to deploy Lab Router VM (Y/N) ? [Y]::: ') or 'y'
            if labrouter_deploy_input.lower() == 'y':
                if vcenter_esxi =='1':
                    rtr_ds = input(f"!!! Enter the Datastore for the Host where LABRTR needs to be deployed [{win_esxi_data['datastore']}]::: ") or win_esxi_data['datastore']
                    rtr_host = input(f"!!! Enter the IP/FQDN for the Host where LABRTR needs to be deployed [{win_server_esxi_ip}]::: ") or win_server_esxi_ip
                    rtr_password = input(f"!!! Enter the password for the Host where LABRTR needs to be deployed [{win_server_esxi_password}]::: ") or win_server_esxi_password
                    rtr_user = input(f"!!! Enter the user for the Host where LABRTR needs to be deployed [{win_server_esxi_user}]::: ") or win_server_esxi_user
                    rtr_vm_name = input('!!! Enter the name for the LABRTR VM [LABRTR] ::: ') or 'LABRTR'
                    rtr_ip = input('!!! Enter the Uplink IP of the router to connect to internet !!! ::: ')
                    rtr_subnet = input ('!!! Enter the Netmask of the router to connect to internet !!! ::: ')
                    rtr_next_hop = input ('!!! Enter the Nxt Hop IP for default route of the router !!! ::: ')
                    vm_to_be_deployed.append('ROUTER')
                elif vcenter_esxi == '2':
                    rtr_ds = input(f"!!! Enter the Datastore for the Host where LABRTR needs to be deployed [{win_esxi_data['datastore']}]::: ") or win_esxi_data['datastore']
                    rtr_vcenter = input(f"!!! Enter the IP/FQDN for the vCenter [{win_server_esxi_ip}]::: ") or win_server_esxi_ip
                    rtr_password = input(f"!!! Enter the password for the vCenter where LABRTR needs to be deployed [{win_server_esxi_password}]::: ") or win_server_esxi_password
                    rtr_user = input(f"!!! Enter the user for the vCenter where LABRTR needs to be deployed [{win_server_esxi_user}]::: ") or win_server_esxi_user
                    rtr_vm_name = input('!!! Enter the name for the LABRTR VM [LABRTR] ::: ') or 'LABRTR'
                    rtr_host = input(f"!!! Enter the IP/FQDN for the Host where LABRTR needs to be deployed [{win_esxi_data['host']}]::: ") or win_esxi_data['host']
                    rtr_ip = input('!!! Enter the Uplink IP of the router to connect to internet !!! ::: ')
                    rtr_subnet = input ('!!! Enter the Netmask of the router to connect to internet !!! ::: ')
                    rtr_next_hop = input ('!!! Enter the Nxt Hop IP for default route of the router !!! ::: ')
                    vm_to_be_deployed.append('ROUTER')
            # Verifying the IP's to be used with VM's
            ip_cml_verify = input(
                'Default IP for CML 169.100.100.2 , Continue using same IP for CML (Need to change it manually)?? Y/N ::: [Y]') or 'y'
            if ip_cml_verify.lower() == 'n':
                ip_cml = input(
                    'Enter the IP of CML, needs to be changed manually (Mgmt IP can be changed referencing the URL https://developer.cisco.com/docs/modeling-labs/editing-the-management-ip-address-via-the-console/ ) ::: ')
                cml = ip_cml
            ip_ise_verify = input(
                'Default IP for ISE 169.200.200.100 , Continue using same IP for ISE (Need to change it manually)?? Y/N ::: [Y]') or 'y'
            if ip_ise_verify.lower() == 'n':
                ip_ise = input('Enter the IP of ISE ::: ')
                ise = ip_ise
            ip_wlc_verify = input(
                'Default IP for WLC 169.200.200.3 , Continue using same IP for WLC (Need to change it manually) ?? Y/N ::: [Y]') or 'y'
            if ip_wlc_verify.lower() == 'n':
                ip_wlc = input('Enter the IP of CML ::: ')
                wlc = ip_wlc
            ip_dnac_verify = input(
                'Default IP for DNAC 169.200.200.130 , Continue using same IP for DNAC(Need to change it manually) ?? Y/N ::: [Y]') or 'y'
            if ip_dnac_verify.lower() == 'n':
                ip_dnac = input('Enter the IP of DNAC ::: ')
                dnacip = ip_dnac
            lab_build_ques = input('!! Step2. Do you want to deploy the Lab Topology in CML !![Y]::: ') or 'y'
            token_input = input('\n!! Enter the License Registration Token for CML from Smart Account :: ')
            prod = input(
                '\n !! Enter the Product Instance \n1.  Personal License with 20 nodes capacity - CML-PER-BASE\n2.  Personal License with 40 nodes capacity - CML-PER-PLUS\n3. Enterprise License - CML-ENT-BASE\n4. Education Institutoin License - CML-EDU-BASE\n   :::: ')
            under_or_over = input(
                '\n!! Step 3. Please select the deployment type \n 1. Underlay Only\n 2. End to End fabric Deployment \n  ::: ')
            if lab_build_ques.lower() == 'y':
                if vcenter_esxi == '1':
                    if 'CML' in vm_to_be_deployed:
                        vm_build_cml_esxi(cml_ds,cml_vm_name,cml_user,cml_password,win_esxi_data,cml_host)
                    if 'DNAC' in vm_to_be_deployed:
                        vm_build_dnac_esxi(win_esxi_data,dnac_ds,dnac_vm_name,dnac_user,dnac_password,dnac_host)
                    if 'ROUTER' in vm_to_be_deployed:
                        vm_build_labrtr_esxi(win_esxi_data,rtr_ds,rtr_vm_name,rtr_user,rtr_password,rtr_host)
                    if 'ISE' in vm_to_be_deployed:
                        vm_build_ise_esxi(win_esxi_data,ise_ds, ise_vm_name, ise_user, ise_password, ise_host)
                    if 'WLC' in vm_to_be_deployed:
                        vm_build_wlc_esxi(win_esxi_data,wlc_ds,wlc_vm_name, wlc_user, wlc_password,wlc_host)
                    if 'ROUTER' in vm_to_be_deployed:
                        print("!! Updating the uplink IP's of the router !!")
                        labrtr(rtr_ip, rtr_subnet, rtr_next_hop)

                elif vcenter_esxi == '2':
                    if 'CML' in vm_to_be_deployed:
                        vm_build_cml_vcenter(cml_ds,cml_vm_name,cml_user,cml_password,win_esxi_data,cml_vcenter,cml_host)
                    if 'DNAC' in vm_to_be_deployed:
                        vm_build_dnac_vcenter(win_esxi_data,dnac_ds,dnac_vm_name,dnac_user,dnac_password,dnac_vcenter,dnac_host)
                    if 'ROUTER' in vm_to_be_deployed:
                        vm_build_labrtr_vcenter(win_esxi_data,rtr_ds,rtr_vm_name,rtr_user,rtr_password,rtr_vcenter,rtr_host)
                    if 'ISE' in vm_to_be_deployed:
                        vm_build_ise_vcenter(win_esxi_data,ise_ds, ise_vm_name, ise_user, ise_password, ise_vcenter,ise_host)
                    if 'WLC' in vm_to_be_deployed:
                        vm_build_wlc_vcenter(win_esxi_data,wlc_ds,wlc_vm_name, wlc_user, wlc_password,wlc_vcenter,wlc_host)
                    if 'ROUTER' in vm_to_be_deployed:
                        print("!! Updating the uplink IP's of the router !!")
                        labrtr(rtr_ip, rtr_subnet, rtr_next_hop)


                reachability_cml(cml)
                reachability_ise(ise)
                reachability_dnac(dnacip)
                lab_build(sda_build, gitval[0], cml, dnacip, ise, under_or_over, token_input,prod)
        else:
            lab_build_ques = input('!! Step2. Do you want to deploy the Lab Topology in CML !![Y]::: ') or 'y'

            if lab_build_ques.lower() == 'y':
                token_input = input('\n!! Enter the License Registration Token for CML from Smart Account :: ')
                prod = input(
                    '\n !! Enter the Product Instance \n1.  Personal License with 20 nodes capacity - CML-PER-BASE\n2.  Personal License with 40 nodes capacity - CML-PER-PLUS\n3. Enterprise License - CML-ENT-BASE\n4. Education Institutoin License - CML-EDU-BASE\n   :::: ')
                under_or_over = input(
                    '\n!! Step 3. Please select the deployment type \n 1. Underlay Only\n 2. End to End fabric Deployment \n  ::: ')
                reachability_cml(cml)
                reachability_ise(ise)
                reachability_dnac(dnacip)
                lab_build(sda_build, gitval[0], cml, dnacip, ise, under_or_over, token_input, prod)
            else:
                under_or_over = input(
                    '\n!! Step 3. Please select the deployment type \n 1. Underlay Only\n 2. End to End fabric Deployment \n  ::: ')
                reachability_cml(cml)
                reachability_ise(ise)
                reachability_dnac(dnacip)
                no_lab_build_dnac_only(sda_build, gitval[0], dnacip, ise, under_or_over)




        print('**!! Congratulations , Lab Deployed Successfully !! **')

    except IOError as IOError:
        print(IOError)

def vm_build_cml_esxi(cml_ds,cml_vm_name,cml_user,cml_password,win_esxi_data,cml_host):
    deploy_cml(cml_ds, cml_vm_name, cml_user, cml_password, win_esxi_data['network 3'],
               win_esxi_data['network 2'], cml_host)
    print('!!! Sleeping for 2 mins !!!\n')
    time.sleep(120)

def vm_build_cml_vcenter(cml_ds, cml_vm_name, cml_user, cml_password, win_esxi_data, cml_host,
                          cml_vcenter):
    deploy_vcenter_cml(cml_ds, cml_vm_name, cml_user, cml_password, win_esxi_data['network 3'],
                       win_esxi_data['network 2'], cml_vcenter, cml_host)
    print('!!! Sleeping for 2 mins !!!\n')
    time.sleep(120)



def vm_build_dnac_esxi(win_esxi_data,dnac_ds,dnac_vm_name,dnac_user,dnac_password,dnac_host):
    deploy_cc(dnac_ds, dnac_vm_name, win_esxi_data['network 2'], dnac_user, dnac_password,
              dnac_host)
    print('!!! Sleeping for 2 mins !!!\n')
    time.sleep(120)

def vm_build_dnac_vcenter(win_esxi_data, dnac_ds, dnac_vm_name, dnac_user, dnac_password, dnac_host, dnac_vcenter):
    deploy_vcenter_ise(dnac_ds, dnac_vm_name, win_esxi_data['network 2'], dnac_user, dnac_password,
                       dnac_vcenter, dnac_host)
    print('!!! Sleeping for 2 mins !!!\n')
    time.sleep(120)


def vm_build_labrtr_esxi(win_esxi_data,rtr_ds,rtr_vm_name,rtr_user,rtr_password,rtr_host):
    deploy_labrouter(rtr_ds, rtr_vm_name, win_esxi_data['network 1'], win_esxi_data['network 2'],
                     win_esxi_data['network 3'], rtr_user, rtr_password, rtr_host)
    print('!!! Sleeping for 2 mins !!!\n')
    time.sleep(120)

def vm_build_labrtr_vcenter(win_esxi_data, rtr_ds, rtr_vm_name, rtr_user, rtr_password, rtr_host, rtr_vcenter):
    deploy_vcenter_labrouter(rtr_ds, rtr_vm_name, win_esxi_data['network 1'],
                                     win_esxi_data['network 2'], win_esxi_data['network 3'], rtr_user,
                                     rtr_password, rtr_vcenter, rtr_host)
    print('!!! Sleeping for 2 mins !!!\n')
    time.sleep(120)

def vm_build_ise_esxi(win_esxi_data,ise_ds, ise_vm_name, ise_user, ise_password, ise_host):
    deploy_ise(ise_ds, ise_vm_name, win_esxi_data['network 2'], ise_user, ise_password, ise_host)
    print('!!! Sleeping for 2 mins !!!\n')
    time.sleep(120)

def vm_build_ise_vcenter(win_esxi_data, ise_ds, ise_vm_name, ise_user, ise_password, ise_host, ise_vcenter):
    deploy_vcenter_ise(ise_ds, ise_vm_name, win_esxi_data['network 2'], ise_user, ise_password,
                               ise_vcenter, ise_host)
    print('!!! Sleeping for 2 mins !!!\n')
    time.sleep(120)

def vm_build_wlc_esxi(win_esxi_data,wlc_ds,wlc_vm_name, wlc_user, wlc_password,wlc_host):
    deploy_wlc(wlc_ds, wlc_vm_name, win_esxi_data['network 2'], wlc_user, wlc_password, wlc_host)
    print('!!! Sleeping for 2 mins !!!\n')
    time.sleep(120)

def vm_build_wlc_vcenter(win_esxi_data, wlc_ds, wlc_vm_name, wlc_user, wlc_password, wlc_host, wlc_vcenter):
    deploy_vcenter_wlc(wlc_ds, wlc_vm_name, win_esxi_data['network 2'], wlc_user, wlc_password,
                       wlc_vcenter, wlc_host)
    print('!!! Sleeping for 2 mins !!!\n')
    time.sleep(120)

def lab_build(sda_build,topo,cml,dnacip,iseip,under_or_over,token,prod_ins):
    from SDA.Cat_cen import device_config, create_underlay, overlay_automation
    print('!! Verifying the License Status !!\n')
    cml_lic = cml_tasks(cml, 'admin', 'CISCO123').get_licensing()
    if cml_lic['registration']['status'] == 'COMPLETED' and cml_lic['authorization']['status'] == 'IN_COMPLIANCE':
        print('!! CML License status is good !!\n')
    elif len(cml_lic['features']) == 0:
        print('!! CML License not updated .. Updating CML Licenses !! \n')
        cml_tasks(cml, 'admin', 'CISCO123').set_product_ins(prod_ins)
        cml_tasks(cml, 'admin', 'CISCO123').set_token(token)
    else:
        print('!! CML License not updated .. Updating CML Licenses !! \n')
        cml_tasks(cml, 'admin', 'CISCO123').set_token(token)
    # topo_num = input(f'Enter the number to identify the Topology to be deployed {topologies}\n    :::: ')

    os.chdir(f'C:/Program Files/Git/cmd/{topo[str(sda_build)]}')
    with open(f'C:/Program Files/Git/cmd/{topo[str(sda_build)]}/resources.json') as file:
        resource = (json.loads(file.read()))
        cml_ins = cml_tasks(cml, 'admin', 'CISCO123').cml_resources()
        avail_cpu = ((cml_ins['all']['cpu']['count']) * (cml_ins['all']['cpu']['percent']) / 100)
        print(
            f'\n!! Current available vCPU : {((cml_ins['all']['cpu']['count']) - avail_cpu)} and Memory: {cml_ins['all']['memory']['free']}\n')
        # print(cml_ins['all']['cpu'])
        # print(cml_ins['all']['memory']['free'])
        print(f'!! {resource['cpu']} vCPU and {resource['memory']} memory required to run the topology  !!\n')
        if ((cml_ins['all']['cpu']['count']) - avail_cpu) >= resource['cpu']:
            cml_topo_build = cml_tasks(cml, 'admin', 'CISCO123').topology_build(
                f'C:/Program Files/Git/cmd/{topo[str(sda_build)]}/lab.yml')
        else:
            print('!! Error !! Lack of resources detected to run the topology !! \n')
            power_off = input(
                'Would you try to deploy the topology after powering off the running topologies in CML y/n ? [y]\n     :::: ') or 'y'
            if power_off == 'y':
                print('!! Powering Off Labs !!\n')
                cml_tasks(cml, 'admin', 'CISCO123').power_off_labs()
                cml_topo_build = cml_tasks(cml, 'admin', 'CISCO123').topology_build(
                    f'C:/Program Files/Git/cmd/{topo[str(sda_build)]}/lab.yml')
        print('!! Sleeping for 10 mins !!\n')
        time.sleep(600)
        print('!! Verifying the Reachability of all the fabric Edges !! \n')
        with open(f'C:/Program Files/Git/cmd/{topo[str(sda_build)]}/device_mgmt.json') as device:
            dev = (json.loads(device.read()))
            devreach = []
            for devicetest in dev:
                devreachvar = ping_test(dev[devicetest])
                devreach.append(devreachvar)
                if devreachvar == 'failure':
                    print(f'!! Ping failed for device {devicetest} !! \n')
            while 'failure' in devreach:
                devreach.clear()
                for devicetest in dev:
                    devreachvar = ping_test(dev[devicetest])
                    devreach.append(devreachvar)
                    if devreachvar == 'failure':
                        print(f'!! Ping failed for device {devicetest} !! \n')
                print('!! Sleeping for 4 mins !!\n')
                time.sleep(240)
        print('!! All Devices are up and running !!\n')
        print('!! Reloading the fabric Devices to apply DNA Adv Licenses !!\n')
        cml_tasks(cml, 'admin', 'CISCO123').power_off_specifc_labs(cml_topo_build['id'])
        time.sleep(30)
        cml_tasks(cml, 'admin', 'CISCO123').power_on_specifc_labs(cml_topo_build['id'])
        print('!! Sleeping for 10 mins !!\n')
        time.sleep(600)
        print('!! Verifying the Reachability of all the fabric Edges !! \n')
        with open(f'C:/Program Files/Git/cmd/{topo[str(sda_build)]}/device_mgmt.json') as device:
            dev = (json.loads(device.read()))
            devreach = []
            for devicetest in dev:
                devreachvar = ping_test(dev[devicetest])
                devreach.append(devreachvar)
                if devreachvar == 'failure':
                    print(f'!! Ping failed for device {devicetest} !! \n')
            while 'failure' in devreach:
                devreach.clear()
                for devicetest in dev:
                    devreachvar = ping_test(dev[devicetest])
                    devreach.append(devreachvar)
                    if devreachvar == 'failure':
                        print(f'!! Ping failed for device {devicetest} !! \n')
                print('!! Sleeping for 4 mins !!\n')
                time.sleep(240)
            print('!! Reachability succeeded for all nodes , Pushing ISIS and BGP config to nodes !!\n')
            for devic in dev:
                config = cml_tasks(cml, 'admin', 'CISCO123').get_config(cml_topo_build['id'], devic)
                device_config(dev[devic], config)
    time.sleep(20)
    lab_up_verify(sda_build,topo)
    if under_or_over == '1':
        create_underlay(dnacip)
    elif under_or_over == '2':
        overlay_automation(dnacip, iseip)

def no_lab_build_dnac_only(sda_build,topo,dnacip,ise,under_or_over):
    from SDA.Cat_cen import device_config, create_underlay, overlay_automation
    if under_or_over == '1':
        create_underlay(dnacip)
    elif under_or_over == '2':
        overlay_automation(dnacip, ise)


def reachability_cml(cml):

    print('!!! Running reachability test on CML !!! \n')
    count = 0
    cml_test = ping_test(cml)
    if cml_test == 'success':
        print('!!! Reachability to CML succeeded from Jump Host !!! \n')

    else:
        while cml_test != 'success' and count <=5:
            print('!!! Reachability to CML failed from Jump Host, sleeping for 5 mins !!!\n')
            time.sleep(300)
            count = count +1
            cml_test = ping_test(cml)
            if cml_test == 'success':
                print('!!! Reachability to CML succeeded from Jump Host !!! \n')
                break
            else:
                continue
        print('!! Reachability to CML failed from Jump Host, Script Terminating .. Please check the Network Connection !!\n')
        sys.exit()

def reachability_ise(ise):
    print('!!! Running reachability test on ISE !!! \n')

    count = 0
    cml_test = ping_test(ise)
    if cml_test == 'success':
        print('!!! Reachability to ISE succeeded from Jump Host !!! \n')

    else:
        while cml_test != 'success' and count <=5:
            print('!!! Reachability to ISE failed from Jump Host, sleeping for 5 mins !!!\n')
            time.sleep(300)
            count = count +1
            cml_test = ping_test(ise)
            if cml_test == 'success':
                print('!!! Reachability to ISE succeeded from Jump Host !!! \n')
                break
            else:
                continue
        print('!! Reachability to ISE failed from Jump Host, Script Terminating .. Please check the Network Connection !!\n')
        sys.exit()



def reachability_dnac(dnac):
    print('!!! Running reachability test on DNAC !!! \n')

    count = 0
    cml_test = ping_test(dnac)
    if cml_test == 'success':
        print('!!! Reachability to DNAC succeeded from Jump Host !!! \n')

    else:
        while cml_test != 'success' and count <=5:
            print('!!! Reachability to DNAC failed from Jump Host, sleeping for 5 mins !!!\n')
            time.sleep(300)
            count = count +1
            cml_test = ping_test(dnac)
            if cml_test == 'success':
                print('!!! Reachability to DNAC succeeded from Jump Host !!! \n')
                break
            else:
                continue
        print('!! Reachability to DNAC failed from Jump Host, Script Terminating .. Please check the Network Connection !!\n')
        sys.exit()

def reachability_wlc(wlc):
    wlc_test = ping_test(wlc)
    if wlc_test == 'success':
        print('!!! Reachability to WLC succeeded from Jump Host !!!\n')
    else:
        print('!!! Reachability to WLC failed from Jump Host, please check !!!\n')


def lab_up_verify(sda_build,topo):
    edge_reach = []
    from SDA.Cat_cen import device_config
    with open(f'C:/Program Files/Git/cmd/{topo[str(sda_build)]}/device_mgmt.json') as edge:
        fab_edge = (json.loads(edge.read()))
        for ed in fab_edge:
            if re.search('.*-FE.*',ed):
                out = device_config(fab_edge[ed],['do ping 169.200.200.130 so lo0'])
                if re.search('(.*)\nSuccess rate is 100 percent (.*)',(out)):
                    print(f'!! Reachability succeeded to DNAC from Edge {ed} !!')
                    edge_reach.append('success')
                else:
                    print(f'!! Reachability failed to DNAC from Edge {ed} !!')
                    edge_reach.append('failure')
                    print('failure')
        print('!!Sleeping for 1 min!!')
        time.sleep(60)
        timeout = time.time() + 3600  # 1 Hour from now
        timeout_start = time.time()
        while 'failure' in edge_reach:
            if time.time() > timeout:
                print('!! Reachability of Devices took more than 1 hout to verify .. Please reach out to GPSA team !!\n')
                break
            edge_reach.clear()
            for ed in fab_edge:
                if re.search('.*-FE.*', ed):
                    out = device_config(fab_edge[ed], ['do ping 169.200.200.130 so lo0'])
                    if re.search('(.*)\nSuccess rate is 100 percent (.*)', (out)):
                        print(f'!! Reachability succeeded to DNAC from Edge {ed} !!')
                        edge_reach.append('success')
                    else:
                        print(f'!! Reachability failed to DNAC from Edge {ed} !!')
                        edge_reach.append('failure')
                        print('failure')
            print('!!Sleeping for 5 mins !!\n')
