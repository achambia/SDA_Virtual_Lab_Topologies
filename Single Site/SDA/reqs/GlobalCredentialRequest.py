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

""" Catalyst Center request for creating global credentials """

from SDA.models.CliCredentialModel import CliCredentialModel
from SDA.models.HttpsCredentialModel import HttpsCredentialModel
from SDA.models.SnmpV2cCredentialModel import SnmpV2cCredentialModel
from SDA.models.SnmpV3CredentialModel import SnmpV3CredentialModel

class GlobalCredentialRequest:
    """
    API request for creating global credentials
    """
    def __init__(self) -> None:
        """
        Constructor
        :return: none
        """
        super().__init__()

        self.cliCredential:list[CliCredentialModel]
        self.snmpV2cRead:list[SnmpV2cCredentialModel]
        self.snmpV2cWrite:[SnmpV2cCredentialModel]
        self.snmpV3:list[SnmpV3CredentialModel]
        self.httpsRead:list[HttpsCredentialModel]
        self.httpsWrite:list[HttpsCredentialModel]
