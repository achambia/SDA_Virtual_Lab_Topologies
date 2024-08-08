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

""" Catalyst Center request for adding a fabric site """

from SDA.enums.AuthenticationProfileNameEnum import AuthenticationProfileNameEnum

class FabricSitesRequest:
    """
    API request for adding a fabric site
    """
    def __init__(self, siteNameHierarchy:str, authenticationProfileName:AuthenticationProfileNameEnum, isPubSubEnabled:bool) -> None:
        """
        Constructor
        :param siteNameHierarchy: Fully qualified name of the site
        :param authenticationProfileName: Name of the authentication profile to be set on the site
        :param isPubSubEnabled: Specify if this fabric site uses pub/sub
        :return: none
        """
        super().__init__()

        self.siteNameHierarchy:str = siteNameHierarchy
        self.authenticationProfileName:AuthenticationProfileNameEnum = authenticationProfileName
        self.isPubSubEnabled:bool = isPubSubEnabled
