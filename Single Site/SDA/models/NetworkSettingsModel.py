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

""" Catalyst Center Network settings model """

from enums.TimezoneEnum import TimezoneEnum
from models.AAAModel import AAAModel
from models.DnsServerModel import DnsServerModel
from models.MessageOfTheDayModel import MessageOfTheDayModel
from models.NetflowCollectorModel import NetflowCollectorModel
from models.ServerModel import ServerModel

class NetworkSettingsModel:
    """
    Network settings model
    """
    def __init__(self, timezone:TimezoneEnum) -> None:
        """
        Constructor
        :param timezone: Timezone
        :return: none
        """
        self.timezone:TimezoneEnum = timezone
        self.dhcpServer:list[str]
        self.ntpServer:list[str]
        self.clientAndEndpoint_aaa:AAAModel = AAAModel(None, None, None)
        self.dnsServer:DnsServerModel = DnsServerModel(None, None)
        self.messageOfTheday:MessageOfTheDayModel = MessageOfTheDayModel(None)
        self.netflowcollector:NetflowCollectorModel = NetflowCollectorModel(None, None)
        self.network_aaa:AAAModel = AAAModel(None, None, None)
        self.snmpServer:ServerModel = ServerModel(None)
        self.syslogServer:ServerModel = ServerModel(None)