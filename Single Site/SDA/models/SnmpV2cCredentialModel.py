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

""" Catalyst Center SNMP v2c Credential data model """

class SnmpV2cCredentialModel:
    """
    SNMP v2c Credential data model
    """
    def __init__(self, description:str, readCommunity:str, writeCommunity:str) -> None:
        """
        Constructor
        :param description: Description for SNMP community
        :param readCommunity: SNMP RO community (set this to 'None' when creating 'WRITE' credential)
        :param writeCommunity: SNMP RW community (set this to 'None' when creating 'READ' credential)
        :return: none
        """
        self.description:str = description
        self.readCommunity:str = readCommunity
        self.writeCommunity:str = writeCommunity