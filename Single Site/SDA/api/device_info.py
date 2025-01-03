#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2021 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
import sys
from SDA.SDA.api import  service_instance, pchelper
from pyVmomi import vim

# Demonstrates:
# =============
# * How to write python 2.7 and 3.3 compatible code in one script
# * How to parse arguments in a python script
# * How to pretty print format a dictionary
# * How to connect to a vSphere instance
# * How to search for virtual machines efficiently
# * How to interrogate virtual machine hardware info
# * How to determine the data type of a dynamic object instance
# * How to build a summary of a virtual device & virtual disk
# * How to interrogate a datastore and its hosts mounts
#
# Not shown, how to ask a datastore for all the virtual machines it 'owns'
#
# Sample output:
#
# $ virtual_machine_device_info.py -s vcsa -u my_user -i 172.16.254.101
#
# Found Virtual Machine
# =====================
#   guest OS name            : Ubuntu Linux (64-bit)
#   name                     : box
#   last booted timestamp    : 2014-10-13 01:45:57.647340+00:00
#   bios UUID                : 420264ab-848b-1586-b589-b9bd3a71b3aa
#   path to VM               : [storage0] box/box.vmx
#   guest OS id              : ubuntu64Guest
#   host name                : esx_host_01
#   instance UUID            : 500221fe-3473-60ff-fab2-1811600208a0
#   Devices:
#   --------
#   label: IDE 0
#   ------------------
#     device type    : vim.vm.device.VirtualIDEController
#     backing type   : NoneType
#     key            : 200
#     summary        : IDE 0
#   label: IDE 1
#   ------------------
#     device type    : vim.vm.device.VirtualIDEController
#     backing type   : NoneType
#     key            : 201
#     summary        : IDE 1
#   label: PS2 controller 0
#   ------------------
#     device type    : vim.vm.device.VirtualPS2Controller
#     backing type   : NoneType
#     key            : 300
#     summary        : PS2 controller 0
#   label: PCI controller 0
#   ------------------
#     device type    : vim.vm.device.VirtualPCIController
#     backing type   : NoneType
#     key            : 100
#     summary        : PCI controller 0
#   label: SIO controller 0
#   ------------------
#     device type    : vim.vm.device.VirtualSIOController
#     backing type   : NoneType
#     key            : 400
#     summary        : SIO controller 0
#   label: Keyboard
#   ------------------
#     device type    : vim.vm.device.VirtualKeyboard
#     backing type   : NoneType
#     key            : 600
#     summary        : Keyboard
#   label: Pointing device
#   ------------------
#     device type    : vim.vm.device.VirtualPointingDevice
#     backing type   : vim.vm.device.VirtualPointingDevice.DeviceBackingInfo
#     key            : 700
#     summary        : Pointing device; Device
#   ------------------
#   label: Video card
#   ------------------
#     device type    : vim.vm.device.VirtualVideoCard
#     backing type   : NoneType
#     key            : 500
#     summary        : Video card
#   label: VMCI device
#   ------------------
#     device type    : vim.vm.device.VirtualVMCIDevice
#     backing type   : NoneType
#     key            : 12000
#     summary        : Device on the virtual machine PCI bus that provides supp
#   label: SCSI controller 0
#   ------------------
#     device type    : vim.vm.device.VirtualLsiLogicController
#     backing type   : NoneType
#     key            : 1000
#     summary        : LSI Logic
#   label: Hard disk 1
#   ------------------
#     device type    : vim.vm.device.VirtualDisk
#     backing type   : vim.vm.device.VirtualDisk.FlatVer2BackingInfo
#     key            : 2000
#     summary        : 16,777,216 KB
#     datastore
#         name: storage0
#         host: esx_host_01
#         summary
#             url: ds:///vmfs/volumes/501fa6d9-8907f56a-fa19-782bcb74158e/
#             freeSpace: 5750390784
#             file system: VMFS
#             capacity: 494726545408
#     fileName: [storage0] box/box.vmdk
#     device ID: None
#   ------------------
#   label: CD/DVD drive 1
#   ------------------
#     device type    : vim.vm.device.VirtualCdrom
#     backing type   : vim.vm.device.VirtualCdrom.AtapiBackingInfo
#     key            : 3002
#     summary        : ATAPI /vmfs/devices/cdrom/mpx.vmhba0:C0:T0:L0
#   ------------------
#   label: Network adapter 1
#   ------------------
#     device type    : vim.vm.device.VirtualE1000
#     backing type   : vim.vm.device.VirtualEthernetCard.NetworkBackingInfo
#     key            : 4000
#     summary        : VM Network
#   ------------------
#   label: Floppy drive 1
#   ------------------
#     device type    : vim.vm.device.VirtualFloppy
#     backing type   : vim.vm.device.VirtualFloppy.RemoteDeviceBackingInfo
#     key            : 8000
#     summary        : Remote
#   ------------------
# =====================

dev ={}

def device_net(host,user,password,port,vmname):
    # form a connection...
    si = service_instance.connect(host,user,password,port)

    # http://pubs.vmware.com/vsphere-55/topic/com.vmware.wssdk.apiref.doc/vim.SearchIndex.html
    search_index = si.content.searchIndex

    # without exception find managed objects using durable identifiers that the
    # search index can find easily. This is much better than caching information
    # that is non-durable and potentially buggy.

    vm = None
    content = si.RetrieveContent()
    vm = pchelper.get_obj(content, [vim.VirtualMachine], vmname)


    if not vm:
        print(u"Could not find a virtual machine to examine.")
        sys.exit(1)


    details = {'name': vm.summary.config.name,
               'instance UUID': vm.summary.config.instanceUuid,
               'bios UUID': vm.summary.config.uuid,
               'path to VM': vm.summary.config.vmPathName,
               'guest OS id': vm.summary.config.guestId,
               'guest OS name': vm.summary.config.guestFullName,
               'host name': vm.runtime.host.name,
               'last booted timestamp': vm.runtime.bootTime}
    count =1
    for device in vm.config.hardware.device:
        # diving into each device, we pull out a few interesting bits
        dev_details = {'key': device.key,
                       'summary': device.deviceInfo.summary,
                       'device type': type(device).__name__,
                       'backing type': type(device.backing).__name__,
                       'label': (device.deviceInfo.label)}



        #print(u"  label: {0}".format(device.deviceInfo.label))
        #print(u"  ------------------")
        if re.search('Network .*',dev_details['label']):
            if re.search('DVSwitch.*',dev_details['summary']):
                dev.update({f'network {str(count)}': {'swuuid':device.backing.port.switchUuid,'pgkey':device.backing.port.portgroupKey}})
            else:
                dev.update({f'network {str(count)}':dev_details['summary']})
            count = count + 1



        if device.backing is None:
            continue

        # the following is a bit of a hack, but it lets us build a summary
        # without making many assumptions about the backing type, if the
        # backing type has a file name we *know* it's sitting on a datastore
        # and will have to have all of the following attributes.
        if hasattr(device.backing, 'fileName'):
            datastore = device.backing.datastore
            if datastore:
                #print(u"    datastore")
                #print(u"        name: {0}".format(datastore.name))
                dev.update({'datastore':datastore.name})
                # there may be multiple hosts, the host property
                # is a host mount info type not a host system type
                # but we can navigate to the host system from there
                for host_mount in datastore.host:
                    host_system = host_mount.key
                    #print(u"        host: {0}".format(host_system.name))
                    dev.update({'host':host_system.name})
    return dev
