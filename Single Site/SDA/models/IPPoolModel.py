#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Atul Trasi"
__email__ = "atrasi@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

""" Catalyst Center IP Pool data model """

from enums.IPAddressSpaceEnum import IPAddressSpaceEnum
from enums.IPPoolTypeEnum import IPPoolTypeEnum

class IPPoolModel:
    """
    IP Pool data model
    """
    
    def __init__(self, ipPoolName:str, type:IPPoolTypeEnum, ipPoolCidr:str, IpAddressSpace:IPAddressSpaceEnum) -> None:
        """
        Constructor
        :param ipPoolName: Name of the IP pool
        :param type: Type of the IP pool
        :param ipPoolCidr: IP address CIDR
        :param IpAddressSpace: IP address space
        :return: none
        """
        self.ipPoolName:str = ipPoolName
        self.type:IPPoolTypeEnum = type
        self.ipPoolCidr:str = ipPoolCidr
        self.gateway:str
        self.dhcpServerIps:list[str]
        self.dnsServerIps:list[str]
        self.IpAddressSpace:IPAddressSpaceEnum = IpAddressSpace