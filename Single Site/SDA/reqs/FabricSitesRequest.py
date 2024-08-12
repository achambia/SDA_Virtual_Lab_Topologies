class FabricSitesRequest:
    """
    API request for adding a fabric site
    """
    def __init__(self, siteNameHierarchy:str) -> None:
        """
        Constructor
        :param siteNameHierarchy: Fully qualified name of the site
        :param authenticationProfileName: Name of the authentication profile to be set on the site
        :param isPubSubEnabled: Specify if this fabric site uses pub/sub
        :return: none
        """
        super().__init__()

        self.siteNameHierarchy:str = siteNameHierarchy
