class Categoria: 
    def __init__(self,id,name,description,item_ids):
        self.__id=id
        self.__name = name
        self.__description = description
        self.__father_id = None
        self.__child_ids = {}
        self.__item_ids=item_ids or {}

    def __init__(self,id,name,description):
        self.__id = id 
        self.__name=name 
        self.__description=description
        
    def getId(self):
        return self.__id
    def getName(self):
        return self.__name 
    def getDescription(self):
        return self.__description
    def getChild_ids(self):
        return self.__child_ids
    def getItem_ids(self):
        return self.__item_ids
    def getFather_id(self):
        return self.__father_id
    