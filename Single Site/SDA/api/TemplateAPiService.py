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

""" Catalyst Center Task for Template API """

from SDA.SDA.api.ApiService import ApiService
from SDA.SDA.reqs.ProjectRequest import ProjectRequest
from SDA.SDA.reqs.TemplateRequest import TemplateRequest
from SDA.SDA.reqs.VersionTemplateRequest import VersionTemplateRequest
from SDA.SDA.reqs.DeployTemplateRequest import DeployTemplateRequest
from SDA.SDA.params.GetlistProject import GetlistProject
from SDA.SDA.params.GetlistTemplate import GetlistTemplate
class TemplateApiService(ApiService):
    """
    Template API
    """

    def __init__(self, url:str, token:str) -> dict:
        """
        Constructor
        :param url: Catalyst Center URL
        :param token: Authentication token
        :return: none
        """
        super().__init__(url, token)

    def createProject(self, createProjectRequest:ProjectRequest) -> dict:
        """
        Create Project API
        :param CreateProjectRequest: Request object containing information to be updated
        :return: API response
        """

        return self.post('/dna/intent/api/v1/template-programmer/project' , createProjectRequest)

    def createTemplate(self,createTemplateRequest:TemplateRequest, projectId:str) -> dict:
        """
        Create Template API
        :param CreateTemplateRequest: Request object containing information to be updated
        :param projectId: Project ID of the Project, to which the template is going to be attached
        :return: API response
        """
        return self.post(f'/dna/intent/api/v1/template-programmer/project/{projectId}/template', createTemplateRequest)

    def updateTemplate(self,createTemplateRequest:TemplateRequest) -> dict:
        """
        Update Template API
        :param CreateTemplateRequest: Request object containing information to be updated
        :return: API response
        """
        return self.put(f'/dna/intent/api/v1/template-programmer/template', createTemplateRequest)

    def versionTemplate(self,createVersionTemplateRequest:VersionTemplateRequest):
        """
        Version Template API
        :param CreateVersionTemplateRequest: Request object containing information to be updated
        :return: API response
        """
        return self.post('/dna/intent/api/v1/template-programmer/template/version', createVersionTemplateRequest)

    def deploytemplate(self,createDeployTemplate:DeployTemplateRequest):
        """
        Version Template API
        :param createDeployTemplate: Request object containing information to be updated
        :return: API response
        """
        return self.post('/dna/intent/api/v1/template-programmer/template/deploy', createDeployTemplate)

    def getlistproject(self,getListProject:GetlistProject):
        """
        list Project API
        :param listproject: Request object containing information to be updated
        :return: API response
        """
        return self.get('/dna/intent/api/v1/template-programmer/project', getListProject)

    def getTemplate(self,getListtemplate:GetlistTemplate):
        """
        list template API
        :param listproject: Request object containing information to be updated
        :return: API response
        """
        return self.get('/dna/intent/api/v1/template-programmer/template', getListtemplate)







