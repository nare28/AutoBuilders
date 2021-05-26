from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
import os

class UserProf:

    def __init__(self, email, roleid, uid, orgid):
        self.email = email
        self.roleid = roleid
        self.uid = int(uid)
        self.orgid = int(orgid)

    def generate_token(self):
        s = Serializer(os.environ["APP_SKEY"], expires_in=int(os.environ["APP_TOKEN_EXP"]))
        res = {"email":self.email, "roleid":self.roleid, "uid":int(self.uid), "orgid":int(self.orgid)}
        return s.dumps(res)
    
    def setFullName(self, fullname):
        self.fullname = fullname