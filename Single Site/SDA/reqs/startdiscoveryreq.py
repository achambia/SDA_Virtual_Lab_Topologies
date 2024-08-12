class startdiscoveryreq:
    """
    API request for creating/updating a site
    """
    def __init__(self, ip:str, name:str) -> None:
        """
        Constructor
        :param type: Type of site to create
        :return: none
        """

        self.discoveryType:str = 'RANGE'
        self.enablePasswordList:list = ['cisco']
        self.ipAddressList:str = ip
        self.name = name
        self .netconfPort = '830'
        self.snmpROCommunity='RO'
        self.snmpRWCommunity='RW'
        self.userNameList = ['netadmin']
        self.passwordList = ['cisco']
