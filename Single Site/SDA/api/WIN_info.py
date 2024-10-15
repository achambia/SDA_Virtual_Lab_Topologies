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

"""
Python program for listing the VMs on an ESX / vCenter host
"""

import re
from pyVmomi import vmodl, vim
from SDA.SDA.api import service_instance
getvm ={}


def print_vm_info(count,virtual_machine):

    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    summary = virtual_machine.summary
    getvm.update({count:summary.config.name})


def getvms(host,user,password,port):
    """
    Simple command-line program for listing the virtual machines on a system.
    """


    si = service_instance.connect(host,user,password,port)
    try:
        content = si.RetrieveContent()

        container = content.rootFolder  # starting point to look into
        view_type = [vim.VirtualMachine]  # object types to look for
        recursive = True  # whether we should look into it recursively
        container_view = content.viewManager.CreateContainerView(
            container, view_type, recursive)

        children = container_view.view
        count =1

        for child in children:
            print_vm_info(count,child)
            count = count+1

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1
    return getvm


