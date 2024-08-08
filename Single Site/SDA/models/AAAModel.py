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

""" Catalyst Center AAA data model """

from enums.AAAProtocolEnum import AAAProtocolEnum
from enums.AAAServerTypeEnum import AAAServerTypeEnum

class AAAModel:
    """
    AAA data model
    """
    def __init__(self, servers:AAAServerTypeEnum, network:str, protocol:AAAProtocolEnum) -> None:
        """
        Constructor
        :param servers: Server type for AAA network
        :param network: IP Address for AAA or ISE server
        :param protocol: Protocol for AAA or ISE server
        :return: none
        """
        self.ipAddress:str
        self.network:str = network
        self.protocol:AAAProtocolEnum = protocol
        self.servers:AAAServerTypeEnum = servers
        self.sharedSecret:str