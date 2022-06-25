class Session():
    def __init__(self):
        self.sessionId=""
        self.attributeDict={}
    def setSessionId(self,sessionId):
        self.sessionId=sessionId
    def getSessionId(self):
        return self.sessionId
    def setAttribute(self,key,value):
        self.attributeDict[key]=value
    def getAttribute(self,key):
        if key not in self.attributeDict.keys():
            raise Exception("Key "+key+" not found")
        return self.attributeDict[key]
    def destroy():
        self.sessionId=""
        self.attributeDict.clear()