import json
import time
import urllib3
import yaml
from yaml import load,dump,SafeLoader
import requests
import re


class cml_tasks:

    def __init__(self,url,user,password):
        urllib3.disable_warnings()
        self.url = f'https://{url}/api/v0/'
        auth = {
            "username": user,
            "password": password
        }
        self.header = {'content-type': 'application/json',
                  'accept': 'application/json'}
        self.token = requests.post(self.url+'/authenticate',json=auth, headers=self.header, verify=False)
        self.header.update({'Authorization': f'Bearer {self.token.json()}'})

    def cml_resources(self):
        uri = self.url+'/system_stats'
        cml_resource = requests.get(uri,headers=self.header,verify=False)
        return cml_resource.json()

    def topology_build(self,path):
        with open(path) as file:
            lab = file.read()
        lab_config = yaml.load(lab, Loader=SafeLoader)
        lab_topo = requests.post(f'{self.url}/import', headers=self.header,
                                 json={'lab': lab_config['lab'], 'nodes': lab_config['nodes'],
                                       'links': lab_config['links'], 'annotations': lab_config['annotations']},
                                 verify=False)
        if lab_topo.status_code == 200:
            print('!! Topology Deployed Successfully !! \n')
            print('!! Powering On the Lab !! \n')
            time.sleep(10)
            start_request = requests.put(f'{self.url}/labs/{lab_topo.json()["id"]}/start',headers=self.header,verify=False)
            if start_request.status_code == 204:
                print('!! Successfully Powered ON the Lab. !! \n')
            else:
                print('!! Power On failure , reason below !!\n')
                print(start_request.status_code , start_request.json())
        else:
            print('!! Topology Deployment Failed !!\n')
            print(lab_topo.status_code, lab_topo.json())
        return lab_topo.json()


    def power_off_labs(self):
        lab_id = requests.get(f'{self.url}/labs',headers=self.header,verify=False)
        for labs in lab_id.json():
            stop_request = requests.put(f'{self.url}/labs/{labs}/stop',headers=self.header,verify=False)
            if (stop_request.status_code) == 204:
                print('!! Lab Powered Off Successfully !!\n')
            else:
                print('Powering off Lab Failed')

    def power_off_specifc_labs(self,labid):
        stop_request = requests.put(f'{self.url}/labs/{labid}/stop', headers=self.header, verify=False)
        if (stop_request.status_code) == 204:
            print('!! Lab Powered Off Successfully !!\n')
        else:
            print('Powering off Lab Failed')


    def power_on_specifc_labs(self,labid):
        start_request = requests.put(f'{self.url}/labs/{labid}/start', headers=self.header, verify=False)
        if (start_request.status_code) == 204:
            print('!! Lab Powered On Successfully !!\n')
        else:
            print('Powering on Lab Failed')

    def get_config(self,labid,device):
        start_request = requests.get(f'{self.url}/labs/{labid}/nodes', headers=self.header, verify=False)
        if (start_request.status_code) == 200:
            for node in (start_request.json()):
                node_config = requests.get(f'{self.url}/labs/{labid}/nodes/{node}', headers=self.header, verify=False)
                if (node_config.json()['label']) == device:
                    value  = (re.split('\n',node_config.json()['configuration']))
        else:
            print('CML not responding')
        return value



    def get_licensing(self):
        lic = requests.get(f'{self.url}/licensing',headers=self.header,verify=False)
        return lic.json()


    def set_product_ins(self,prod):
        prod_dict = {'1': 'CML_Personal', '2': 'CML_Personal40', '3': r'"CML_Enterprise"', '4': 'CML_Education'}
        prod_ins = requests.put(f'{self.url}/licensing/product_license',headers=self.header,verify=False,data=prod_dict[prod])
        if prod_ins.status_code == 204:
            print('!! Product Instance Successfully Updated !!\n')
        else:
            print('!! ERROR while registering Product Instance !!\n')
            print(prod_ins.status_code,prod_ins.json())


    def set_token(self,token_input):
        token_push = requests.post(f'{self.url}/licensing/registration',headers=self.header,verify=False,json={"token": token_input,
                                                                                                               "reregister": True})
        if token_push.status_code == 204:
            print('!! Token Applied Successfully !!\n\n !! Sleeping for 1 min !! \n')
            time.sleep(60)
            print('!! Verifying the Status of License Application !!\n')
            cml_verify =requests.get(f'{self.url}/licensing',headers=self.header,verify=False)
            while cml_verify.json()['registration']['status'] != 'COMPLETED' and cml_verify.json()['authorization']['status'] != 'IN_COMPLIANCE':
                print('!! Licenses not in compliance, PLease check the network reachability of CML to tools.cisco.com .. Script will continue to reregister every 1 min !!\n')
                cml_reg_renew = requests.put(f'{self.url}/licensing/registration/renew', headers=self.header, verify=False)
                if cml_reg_renew.status_code ==204:
                    print('!! Renewed the Registeration successfully !!\n')
                else:
                    print(cml_reg_renew.json())
                cml_auth_renew = requests.put(f'{self.url}/licensing/authorization/renew', headers=self.header, verify=False)
                if cml_auth_renew.status_code ==204:
                    print('!! Renewed the Authorization successfully !!\n')
                else:
                    print(cml_auth_renew.json())
                cml_verify = requests.get(f'{self.url}/licensing', headers=self.header, verify=False)
                time.sleep(60)
                print('!! Sleeping for 1 min .. will conitue registration after sleep !!  \n')
            print('!!Licenses in Compliance!!\n')

        else:
            print(token_push.json())

