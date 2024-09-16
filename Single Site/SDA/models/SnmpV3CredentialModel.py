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

""" Catalyst Center SNMP v3 Credential data model """

from SDA.SDA.enums.SnmpV3AuthTypeEnum import SnmpV3AuthTypeEnum
from SDA.SDA.enums.SnmpV3PrivacyTypeEnum import SnmpV3PrivacyTypeEnum
from SDA.SDA.enums.SnmpV3SnmpModeEnum import SnmpV3SnmpModeEnum

class SnmpV3CredentialModel:
    """
    SNMP v3 Credential data model
    """
    def __init__(self, description:str, username:str, privacyType:SnmpV3PrivacyTypeEnum, privacyPassword:str, authType:SnmpV3AuthTypeEnum, authPassword:str, snmpMode:SnmpV3SnmpModeEnum) -> None:
        """
        Constructor
        :param description: Description for SNMP V3 credential
        :param username: SNMP V3 username
        :param privacyType: SNMP privacy protocol
        :param privacyPassword: Privacy password for SNMP privacy
        :param authType: SNMP auth protocol
        :param authPassword: Auth password for SNMP
        :param snmpMode: Mode of SNMP
        :return: none
        """
        self.description:str = description
        self.username:str = username
        self.privacyType:SnmpV3PrivacyTypeEnum = privacyType
        self.privacyPassword:str = privacyPassword
        self.authType:SnmpV3AuthTypeEnum = authType
        self.authPassword:str = authPassword
        self.snmpMode:SnmpV3SnmpModeEnum = snmpMode
