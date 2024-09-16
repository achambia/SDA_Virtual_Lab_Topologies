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

""" Catalyst Center Composite Template data model """

from SDA.SDA.models.TagsModel import TagsModel
from SDA.SDA.models.ProductFamilyModel import ProductFamilyModel
from SDA.SDA.models.RollbackTemplateModel import RollbackTemplateModel
from SDA.SDA.models.TemplateParamsModel import TemplateParamsModel

class CompositeTemplateModel:
    """
    Composite Template Data Model
    """

    def __init__(self) -> None:
        """
        Constructor
        :return: none
        """
        self.tags:list[TagsModel]
        self.composite:bool
        self.description:str
        self.deviceTypes:list[ProductFamilyModel]
        self.id:str
        self.language:str
        self.name:str
        self.projectName:str
        self.rollbackTemplateParams:list[RollbackTemplateModel]
        self.templateContent:str
        self.templateParams:list[TemplateParamsModel]
        self.version:str
