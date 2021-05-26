from daos.base.base_dao import BaseDAO
import logging
import os

class UserDAO(BaseDAO):
    def __init__(self):
        super().__init__()
        self.__logger = logging.getLogger(__name__)
        self.__reclimit = int(os.environ["APP_REC_LIMIT"])
        self.__logger.info("UserDAO Initialized")

    def fetchUsers(self, alias, lastrec):
        self.__logger.info("Fetch Users with alias: %s, lastrec: %d" % (alias, lastrec))
        results = self.fetchResults(
            ("SELECT uid, email, phone, fname, lname, pcode, orgid FROM master.users "
            "WHERE email ILIKE '%%%s%%' ORDER BY email LIMIT %s OFFSET %s", (alias,)), (self.__reclimit, lastrec))
        return results
    
    def fetchUsersByOrgId(self, orgid, lastrec):
        self.__logger.info("Fetch Users in org: %d, lastrec: %d" % (orgid, lastrec))
        results = self.fetchResults(
            "SELECT uid, email, phone, fname, lname, pcode, orgid FROM master.users "
            "WHERE orgid = %s AND active = TRUE ORDER BY uid LIMIT %s OFFSET %s", (orgid, self.__reclimit, lastrec))
        return results

    def validateUserPassCode(self, email, pcode):
        self.__logger.info("Validate User: %s" % (email))
        result = self.getRecord(
            "SELECT uid, email, phone, fname, lname, orgid, active FROM master.users "
            "WHERE email = %s and pcode = %s", (email, pcode))
        return result

    def getUser(self, email):
        self.__logger.info("Get User: %s" % (email))
        result = self.getRecord(
            "SELECT uid, email, phone, fname, lname, pcode, orgid FROM master.users "
            "WHERE email = %s", (email,))
        return result

    def findOrgForCorpId(self, corpid):
        self.__logger.info("Get OrgId for Corp: %s" % (corpid))
        result = self.getRecord(
            "SELECT orgid FROM master.orgs WHERE corpid = %s AND active = TRUE", (corpid,))
        return result

    def createUser(self, metadata):
        self.__logger.info("Create new user")
        result = self.addRecord("INSERT INTO master.users(email, phone, fname, lname, pcode, orgid) "
            "VALUES(%s, %s, %s, %s, %s, %s) RETURNING uid",
            (metadata["email"], metadata["phone"], metadata["fname"], metadata["lname"], 
             metadata["pcode"], metadata["orgid"]))
        return result

    def updateUser(self, metadata):
        self.__logger.info("Update User: %s" % (metadata))
        self.updateRecord("UPDATE master.users SET fname = %s, lname= %s "
            "WHERE email = %s", (metadata["fname"], metadata["lname"], metadata["email"]))
        
    def updatePassword(self, metadata):
        self.__logger.info("Change User: %s password" % (metadata["email"]))
        self.updateRecord("UPDATE master.users SET pcode = %s "
            "WHERE email = %s", (metadata["pcode"], metadata["email"]))

    def activateUser(self, role, uid, oid):
        self.__logger.info("Activate User: %s with role: %s" % (uid, role))
        self.updateRecord("UPDATE master.users SET active = True "
            "WHERE uid = %s" %(uid))
        self.__logger.info("Add roleid : %s to role table" % (role))
        self.addRecord("INSERT INTO master.roles(uid, rolecd, orgid, active, upby, updt) "
            "VALUES(%s, %s, %s, TRUE, %s, CURRENT_TIMESTAMP::TIMESTAMP WITHOUT TIME ZONE) RETURNING uid", 
            (uid, role, oid, uid))