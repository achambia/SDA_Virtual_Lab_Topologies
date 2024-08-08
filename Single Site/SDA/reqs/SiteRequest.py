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

""" Catalyst Center request for creating/updating a site """

from enums.SiteTypeEnum import SiteTypeEnum
from models.SiteModel import SiteModel

class SiteRequest:
    """
    API request for creating/updating a site
    """
    def __init__(self, type:SiteTypeEnum) -> None:
        """
        Constructor
        :param type: Type of site to create
        :return: none
        """
        super().__init__()

        self.type:SiteTypeEnum = type
        self.site:SiteModel = SiteModel()