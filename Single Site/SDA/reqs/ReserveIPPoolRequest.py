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

__author__ = "Abhishek Chambial"
__email__ = "achambia@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

""" Catalyst Center request for reserving IP Pool """

from SDA.SDA.enums.LanTypeEnum import LanTypeEnum

class ReserveIpPoolReq:
    '''
    API for reserving IP Pools
    '''

    def __init__(self, name:str, type , ipv6AddressSpace:bool, ipv4GlobalPool:str, ipv4Prefix:bool) -> None:
        """
        :param name: Name of the reserve ip sub pool
        :param type: Type of the reserve ip sub pool
        :param ipv6AddressSpace: If the value is false only ipv4 input are required, otherwise both ipv6 and ipv4 are required
        :param ipv4GlobalPool: IP v4 Global pool address with cidr, example: 175.175.0.0/16
        :param ipv4Prefix: IPv4 prefix value is true, the ip4 prefix length input field is enabled , if it is false ipv4 total Host input is enable
        :param ipv6Prefix: Ipv6 prefix value is true, the ip6 prefix length input field is enabled , if it is false ipv6 total Host input is enable
        :return None
        """
        self.name:str = name
        self.type:str = type
        self.ipv6AddressSpace:bool = ipv6AddressSpace
        self.ipv4GlobalPool:str = ipv4GlobalPool
        self.ipv4Prefix:bool = ipv4Prefix
        self.ipv4PrefixLength:int
        self.ipv4Subnet:str
        self.ipv4GateWay:str
        self.ipv4DhcpServers:list[str]
        self.ipv4DnsServers:list[str]
        self.ipv6GlobalPool:str
        self.ipv6Prefix:bool
        self.ipv6PrefixLength:int
        self.ipv6Subnet:str
        self.ipv6GateWay:str
        self.ipv6DhcpServers:list[str]
        self.ipv6DnsServers:list[str]
        self.ipv4TotalHost:int
        self.ipv6TotalHost:int
        self.slaacSupport:bool


