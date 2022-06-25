import re


class HttpRequest():
      def __init__(self):
          self.requestParamsDict={}
      def setAttribute(self,key,value):
         self.requestParamsDict[key]= value
      def getAttribute(self,key):
          return self.requestParamsDict[key]   
    
