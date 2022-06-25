from HttpRequest import HttpRequest

class TemplateParser():
    def __init__(self):
        self.stack = []
        self.buffer = None
        self.content = ""
        self.delimeter = '$'
        self.openBracket = '{'
        self.closingBracket = '}'
        self.extension = "psp"
        self.httpRequest = None
    def setHttpRequest(self,httpRequest):
        self.httpRequest = httpRequest    
    def parse(self,fileName):
        if fileName.endswith(self.extension) == False:
            raise Exception("Invalid file type")
        file = open(fileName,"r")
        self.buffer = file.read()
        i = 0
        flag = False
        while i < len(self.buffer):
            if i< len(self.buffer) -1 and self.buffer[i] == self.delimeter and self.buffer[i+1] == self.openBracket:
                flag = True
                startingIndex = i
            elif self.buffer[i] == self.closingBracket:
                endingIndex = i
                ## Replacing ${key} with request.getParameter("key")
                content = ""
                obj = ""
                string = self.buffer[startingIndex+2:endingIndex].split(".")
                key = self.buffer[startingIndex+2:endingIndex].split(".")[0]
                if key in self.httpRequest.requestParamsDict.keys():
                    content = self.httpRequest.requestParamsDict[key]
                    obj = content
                    for x in range(1,len(string)):
                      obj = getattr(obj, string[x])
                if len(string) == 0:
                    val = str(content)
                else : val = str(obj)    
                self.content += val
                flag = False
            elif flag == False:
                self.content += str(self.buffer[i])
            i += 1    
        return self.content

