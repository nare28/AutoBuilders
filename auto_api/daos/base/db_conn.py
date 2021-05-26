import logging
import pg8000

logger = logging.getLogger(__name__)

class DBConn:
    def __init__(self, index, params):
        logger.info("Create connection at index : %d" %(index))
        self.__conn = pg8000.connect(**params)
        self.__available = True
        self.index = index
        
    #@synchronize
    def getConnection(self):
        logger.info("Get connection at index: %d" %(self.index))
        return self.__conn
        
    def isAvailable(self):
        return self.__available

    def release(self):
        logger.info("Release connection at index: %d" %(self.index))
        self.__available = True
    