
class DataBase:
    def __init__(self,db):
        self.__db = db
        self.__cursor = db.cursor()