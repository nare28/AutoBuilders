from daos.base.base_dao import BaseDAO
import logging

class TFST_ENTITY_NAME_TFEDDAO(BaseDAO):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.rec_limit = 11
        self.DEL_ERR_MSG = {"status":"DEL_FAILED", "code":301}
        #TBST_SQL_QUERY_SET_TBED#
        self.logger.info("Initialized TFST_ENTITY_NAME_TFEDDAO")   

    def fetchTFST_ENTITY_NAME_TFEDList(self, uid, lastrec):
        self.logger.info("Fetch TFST_ENTITY_NAME_TFED List from record : %s" %(lastrec))
        results = super().fetchResults(self.FETCH_RESULTS, (self.rec_limit, lastrec))
        return results

    def getTFST_ENTITY_NAME_TFED(self, uid, rid):
        self.logger.info("Get TFST_ENTITY_NAME_TFED for : %d" %(rid))
        result = super().getRecord(self.GET_DETAILS, (str(rid),))
        return result

    def createTFST_ENTITY_NAME_TFED(self, uid, metadata):
        self.logger.info("Create TFST_ENTITY_NAME_TFED with data: %s" %(metadata))
        result = super().addRecord(self.CREATE_RECORD, (TFST_FIELDS_SET_TFED, uid))
        return result

    def updateTFST_ENTITY_NAME_TFED(self, uid, rid, ts, metadata):
        self.logger.info("Update TFST_ENTITY_NAME_TFED : %d with data: %s" %(rid, metadata))
        result = super().updateRecord(self.UPDATE_RECORD, (TFST_FIELDS_SET_TFED, uid, rid, ts))
        return result

    def deleteTFST_ENTITY_NAME_TFED(self, uid, rid, ts):
        self.logger.info("Delete TFST_ENTITY_NAME_TFED : %d" %(rid))
        result = super().addRecord(self.CREATE_HIST_RECORD, (uid, rid, ts))
        
        if result is not None:
            print("Hist Timestamp :: "+str(result))
            super().deleteRecord(self.DELETE_RECORD, (rid, ts))
            return self.OK_MSG
        else:
            return self.DEL_ERR_MSG

    def updateTFST_ENTITY_NAME_TFEDState(self, uid, rid, ts, state):
        self.logger.info("Update TFST_ENTITY_NAME_TFED : %d status with : %s" %(rid, state))
        result = super().updateRecord(self.UPDATE_RECORD_STATE, (state, uid, rid, ts))
        return result

    ### REPETE BLOCK START - FIELD UPDATES ###
    ### Update TFST_ENTITY_NAME_TFED field :: TFST_FIELD_NAME_TFED ###
    def updateTFST_ENTITY_NAME_TFEDTFST_FIELD_NAME_TFED(self, uid, rid, ts, val):
        self.logger.info("Update TFST_ENTITY_NAME_TFED : %d field TFST_FIELD_NAME_TFED with : %s" %(rid, val))
        result = super().updateRecord(self.UPDATE_RECORD_FIELD_TFST_COL_NAME_TFED, (val, uid, rid, ts))
        return result

    ### REPETE BLOCK END - FIELD UPDATES ###
