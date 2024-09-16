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

""" Catalyst Center request for Deploying a Template """

from SDA.SDA.models.TemplateTargetInfoModel import TemplateTargetInfoModel

class DeployTemplateRequest:
    """
    API request for Deploying a Template
    """

    def __init__(self, templatetargetInfo:list[TemplateTargetInfoModel],tempId:str) -> None:
        """
        Constructor
        :param templatetargetInfo: Information around the template push
        :param tempId: ID of the template to be provisioned
        :return: none
        """
        self.forcePushTemplate:bool
        self.isComposite:bool
        self.mainTemplateId:str
        self.memberTemplateDeploymentInfo:list[str]
        self.targetInfo:list[TemplateTargetInfoModel] = templatetargetInfo
        self.templateId:str = tempId
