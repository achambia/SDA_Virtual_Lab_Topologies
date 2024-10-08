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

""" Catalyst Center Product Template Target Info data model """

from SDA.SDA.enums.TemplateTargetInfoTypeEnum import TemplateTargetInfoTypeEnum

class TemplateTargetInfoModel:
    """
    Template Target Info data model
    """

    def __init__(self, templateTargetInfoType:TemplateTargetInfoTypeEnum,versionTempId:str) -> None:
        """
        Constructor
        :param templateTargetInfoType: Enum value for Type of Target Device
        :param versionTempId: Version of the Template
        :return: none
        """
        self.hostName:str
        self.id:str
        self.params:dict
        self.resourceParams:str
        self.type:TemplateTargetInfoTypeEnum = templateTargetInfoType
        self.versionedTemplateId:str = versionTempId
