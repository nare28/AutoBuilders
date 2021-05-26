import time
import uuid

class UserTokens:

    __userTokens = None

    def __init__(self):
        self.__userTokensMap = {}

    @staticmethod
    def getInstance():
        if UserTokens.__userTokens == None:
            UserTokens.__userTokens = UserTokens()
        return UserTokens.__userTokens

    def getToken(self, uid, rid, roleid):
        token = str(uuid.uuid4())
        self.__userTokensMap[uid] = {'token': token, "life":int(round((time.time() + 300) * 1000)), "roleid":roleid}
        return token
    
    def validateToken(self, uid, token):
        if uid in self.__userTokensMap:
            metadata = self.__userTokensMap[uid]
            del self.__userTokensMap[uid]
            if metadata['token'] == token and metadata['life'] > int(round(time.time() * 1000)):                
                return metadata['roleid']
        return None

