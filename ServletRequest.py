import re


class ServletRequest():
  def __init__(self):
    self.requestParamsDict={}
    self.httpRequest = None
    self.session=None
  def setRequestParamDict(self,requestParamsDict):
    self.requestParamsDict=requestParamsDict
  def setSession(self,session):
    self.session=session
  def getSession(self):
    return self.session
  def getParameter(self,key):
    for k,value in self.requestParamsDict.items():
      if k==key:
        return value
    raise Exception("Key Not Found")
  def setAttribute(self,key,value):
         self.httpRequest.requestParamsDict[key]= value
  def getAttribute(self,key):
          return self.httpRequest.requestParamsDict[key]   
  def setHttpRequestWrapper(self,request):
    self.httpRequest = request


