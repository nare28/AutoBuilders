from .core_dao import CoreDAO
import logging

class ENTITY_NAMEDAO(CoreDAO):
    
    def __init__(self, connpool):
        super().__init__(connpool)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialized ENTITY_NAMEDAO")   
        
    def fetchENTITY_NAMEList(self, lastrec):
        self.logger.info("Fetch ENTITY_NAME List from record : %s" %(lastrec))
        results = super().fetchResults(dbid, FETCH_RESULTS, (self.rec_limit, lastrec))
        return results
                
    def getENTITY_NAMEDetails(self, rid):
        self.logger.info("Get ENTITY_NAME Details for : %d" %(rid))
        result = super().fetchResult(GET_DETAILS, (str(rid)))
        return result
    
    def createENTITY_NAME(self, metadata):
        self.logger.info("Create ENTITY_NAME with data: %s" %(metadata))
        result = super().insertRecord(CREATE_RECORD, metadata)
        return result
    
    def updateENTITY_NAME(self, rid, ts, metadata):
        self.logger.info("Update ENTITY_NAME : %d with data: %s" %(rid, metadata))
        result = super().updateRecord(UPDATE_RECORD, metadata, rid, ts)
        return OK_MSG
        
    def deleteENTITY_NAME(self, rid, ts):
        self.logger.info("Delete ENTITY_NAME : %d" %(rid))
        result = super().deleteRecord(DELETE_RECORD, rid, ts)
        return OK_MSG
        
    def updateENTITY_NAMEState(self, rid, ts, state):
        self.logger.info("Update ENTITY_NAME : %d status with : %s" %(rid, state))
        result = super().updateRecord(UPDATE_RECORD_STATE, (state, rid, ts))
        return OK_MSG
    