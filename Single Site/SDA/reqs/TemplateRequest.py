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

""" Catalyst Center request for creating a Template """

from SDA.models.TagsModel import TagsModel
from SDA.models.CompositeTemplateModel import CompositeTemplateModel
from SDA.models.ProductFamilyModel import ProductFamilyModel
from SDA.models.RollbackTemplateModel import RollbackTemplateModel
from SDA.models.TemplateParamsModel import TemplateParamsModel
from SDA.models.ValidationErrorModel import ValidationErrorModel
from SDA.enums.FailurePolicyEnum import FailurePolicyEnum
from SDA.enums.LanguageEnum import LanguageTypeEnum

class TemplateRequest:
    """
    API request for creating a Template
    """
    def __init__(self, productFamily:list[ProductFamilyModel],language:LanguageTypeEnum , name:str, projectname:str, sftware:str) -> None:
        """
        Constructor
        :param productFamily: Device Family info
        :param language: Template Language VELOCITY/JINJA
        :param name: Name of the template
        :param projectname: name of the project
        :param name: softwareType to which the Template should be applied.
        :return None
        """
        self.tags:list[TagsModel]
        self.author:str
        self.composite:bool
        self.containingTemplates:list[CompositeTemplateModel]
        self.createTime:int
        self.customParamsOrder:bool
        self.description:str
        self.deviceTypes:list[ProductFamilyModel] = productFamily
        self.failurePolicy:FailurePolicyEnum
        self.id:str
        self.language:LanguageTypeEnum = language
        self.lastUpdateTime:int
        self.latestVersionTime:int
        self.name:str = name
        self.parentTemplateId:str
        self.projectId:str
        self.projectName:str = projectname
        self.rollbackTemplateContent:str
        self.rollbackTemplateParams:list[RollbackTemplateModel]
        self.softwareType:str = sftware
        self.softwareVariant:str
        self.softwareVersion:str
        self.templateContent:str
        self.templateParams:list[TemplateParamsModel]
        self.validationErrors: ValidationErrorModel
        self.version:str
