import logging
from .conn_pool import ConnPool 

class BaseDAO:
    
    __abstract__ = True

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.OK_MSG = {"status":"OK", "code":200}
        self.__logger.info("BaseDAO initiated")
        self.conn_pool = ConnPool.getInstance()
        self.__logger.info("Connection pool initiated")

    def fetchResults(self, query, vals):
        self.__logger.debug(query)
        cursor = None
        results = None
        dbconn = self.conn_pool.getPoolConnection()
        try:
            conn = dbconn.getConnection()
            cursor = conn.cursor()
            cursor.execute(("SELECT row_to_json(row) FROM (%s) row" %(query)), vals)
            results = cursor.fetchall()
            #self.__logger.debug("Results:%s " %(results)) 
        except Exception as e:
            self.__logger.error(e)
        finally:
            cursor.close()         
            dbconn.release()
        return results

    def getRecord(self, query, vals):
        self.__logger.debug(query)
        cursor = None
        result = None
        dbconn = self.conn_pool.getPoolConnection()
        try:
            conn = dbconn.getConnection()
            cursor = conn.cursor()
            cursor.execute(("SELECT row_to_json(row) FROM (%s) row" %(query)), vals)
            result = cursor.fetchone()
            self.__logger.debug("Result:%s " %(result)) 
        except Exception as e:
            self.__logger.error(e)
        finally:
            cursor.close()         
            dbconn.release()
        return result

    def addRecord(self, query, values):
        self.__logger.debug(query)
        cursor = None
        result = None
        dbconn = self.conn_pool.getPoolConnection()
        conn = None
        try:
            conn = dbconn.getConnection()
            cursor = conn.cursor()
            result = cursor.execute(query, values)
            result = result.fetchone()
            conn.commit()
        except Exception as e:
            print(e)
            self.__logger.error(e)
            conn.rollback()
            raise Exception("Failed to add a record")
        finally:
            cursor.close()       
            dbconn.release()
        return result

    def updateRecord(self, query, values):
        self.__logger.debug(query)
        self.__logger.info(values)
        cursor = None
        dbconn = self.conn_pool.getPoolConnection()
        conn = None
        try:
            conn = dbconn.getConnection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
        except Exception as e:
            self.__logger.error(e)
            conn.rollback()
            raise Exception("Failed to update a record")
        finally:
            cursor.close()       
            dbconn.release()
        return self.OK_MSG

    def deleteRecord(self, query, values):
        self.__logger.debug(query)
        cursor = None
        dbconn = self.conn_pool.getPoolConnection()
        conn = None
        try:
            conn = dbconn.getConnection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
        except Exception as e:
            self.__logger.error(e)
            conn.rollback()
            raise Exception("Failed to delete a record")
        finally:
            cursor.close()   
            dbconn.release()
        return self.OK_MSG
