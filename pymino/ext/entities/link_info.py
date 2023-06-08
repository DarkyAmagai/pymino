from typing import Union

"""
class LinkInfo:
    def __init__(self, data: Union[dict, str]) -> None:
        self.data               = data
        self.linkInfoV2         = {}
        self.path               = None
        self.extensions         = {}
        self.objectId           = None
        self.shareURLShortCode  = None
        self.targetCode         = None
        self.ndcId              = None
        self.comId              = None
        self.fullPath           = None
        self.shortCode          = None
        self.objectType         = None

        if isinstance(data, dict):
            self.linkInfoV2:        dict = self.data.get("linkInfoV2", self.linkInfoV2)
            self.path:              Union[str, None] = self.data.get("path", self.path)             or self.linkInfoV2.get("path", self.path)
            self.extensions:        dict = self.data.get("extensions", self.extensions)             or self.linkInfoV2.get("extensions", self.extensions)
            self.objectId:          Union[str, None] = self.data.get("objectId", self.objectId)     or self.extensions.get("linkInfo", {}).get("objectId", self.objectId)
            self.shareURLShortCode: Union[str, None] = self.data.get("shareURLShortCode", self.shareURLShortCode) or self.extensions.get("linkInfo", {}).get("shareURLShortCode", self.shareURLShortCode)
            self.targetCode:        Union[str, None] = self.data.get("targetCode", self.targetCode) or self.extensions.get("linkInfo", {}).get("targetCode", self.targetCode)
            self.ndcId:             Union[int, None] = self.data.get("ndcId", self.ndcId)           or self.extensions.get("linkInfo", {}).get("ndcId", self.ndcId)
            self.comId:             Union[int, None] = self.ndcId
            self.fullPath:          Union[str, None] = self.data.get("fullPath", self.fullPath)     or self.extensions.get("linkInfo", {}).get("fullPath", self.fullPath)
            self.shortCode:         Union[str, None] = self.data.get("shortCode", self.shortCode)   or self.extensions.get("linkInfo", {}).get("shortCode", self.shortCode)
            self.objectType:        Union[str, None] = self.data.get("objectType", self.objectType) or self.extensions.get("linkInfo", {}).get("objectType", self.objectType)

    def json(self) -> Union[dict, str]:
        return self.data
"""
class LinkInfo:
    def __init__(self, data: dict) -> None:
        try:
            self.data = data
        except AttributeError:
            self.data = None

    
    @property
    def linkInfoV2(self) -> Union[str, None]:
        """Returns the linkInfoV2 of the API response."""
        return self.data.get("linkInfoV2")
    
    @property
    def path(self) -> Union[int, None]:
        """Returns the path of the API response."""
        return self.data.get("path") or self.linkInfoV2.get("path")
    
    @property
    def extensions(self) -> Union[dict, None]:
        """Returns the extensions of the API response."""
        return self.data.get("extensions") or self.linkInfoV2.get("extensions")
    
    @property
    def objectId(self) -> Union[str, None]:
        """Returns the objectId of the API response."""
        return self.data.get("objectId") or self.extensions.get("linkInfo", {}).get("objectId")
    
    @property
    def shareURLShortCode(self) -> Union[str, None]:
        """Returns the shareURLShortCode of the API response."""
        return self.data.get("shareURLShortCode") or self.extensions.get("linkInfo", {}).get("shareURLShortCode")
    
    @property
    def targetCode(self) -> Union[str, None]:
        """Returns the targetCode of the API response."""
        return self.data.get("targetCode") or self.extensions.get("linkInfo", {}).get("targetCode")
    
    @property
    def ndcId(self) -> Union[int, None]:
        """Returns the ndcId of the API response."""
        return self.data.get("ndcId") or self.extensions.get("linkInfo", {}).get("ndcId")
    
    @property
    def comId(self) -> Union[int, None]:
        """Returns the comId of the API response."""
        return self.ndcId
    
    @property
    def fullPath(self) -> Union[str, None]:
        """Returns the fullPath of the API response."""
        return self.data.get("fullPath") or self.extensions.get("linkInfo", {}).get("fullPath")
    
    @property
    def shortCode(self) -> Union[str, None]:
        """Returns the shortCode of the API response."""
        return self.data.get("shortCode") or self.extensions.get("linkInfo", {}).get("shortCode")
    
    @property
    def objectType(self) -> Union[str, None]:
        """Returns the objectType of the API response."""
        return self.data.get("objectType") or self.extensions.get("linkInfo", {}).get("objectType")
    
    def json(self) -> Union[dict, str]:
        """Returns the JSON data of the API response."""
        return self.data
    
    def __repr__(self) -> str:
        """Returns the representation of the Link Info response."""
        return f"<LinkInfo data={self.data}>"