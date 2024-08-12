class startdiscoveryreq:
    """
    API request for creating Discovery
    """
    def __init__(self, ip:str, name:str, clicred, snmprocred,snmpwrcred) -> None:
        """
        Constructor
        :param type: Type of site to create
        :return: none
        """

        self.discoveryType:str = 'Range'
        self.ipAddressList:str = ip
        self.name = name
        self.netconfPort = '830'
        self.protocolOrder = "ssh"
        self.globalCredentialIdList:list  = [clicred,snmprocred,snmpwrcred]
