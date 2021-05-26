import pg8000
import logging
import os
from .db_conn import DBConn

logger = logging.getLogger(__name__)

class ConnPool:
    __connpool = None

    def __init__(self):
        self.__connections = []
        self.dbconfig = {"host": os.environ["dbhost"], "database":os.environ["database"], 
            "user":os.environ["dbuser"], "password":os.environ["dbpassword"], 
            "port":int(os.environ["dbport"])}
        print(self.dbconfig)
        self.__createPool(int(os.environ["APP_DBPOOL_MIN"]))
    
    @staticmethod
    def getInstance():
        if ConnPool.__connpool is None:
            ConnPool.__connpool = ConnPool()
        return ConnPool.__connpool
        
    def __createPool(self, minPool):
        logger.info("Started creating the connectin pool with minimum connections %d" %(minPool))
        for i in range(minPool):
            logger.info("Create connection at pool location: %d" %(i+1))
            dbconn = DBConn(i+1, self.dbconfig)
            self.__connections.append(dbconn)
        logger.info("Connection pool creation is successfull")

    def getPoolConnection(self):
        for conn in self.__connections:
            if conn.isAvailable():
                logger.info("Found connection at: %d" %(conn.index))
                return conn
        logger.info("No connections available in pool")
        raise("No connections")