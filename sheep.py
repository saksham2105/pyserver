from http.server import BaseHTTPRequestHandler,HTTPServer
import os
import json
import cgi
import time
import socket
import importlib
from urllib import parse
from HttpRequest import HttpRequest
import ServletRequest as sReq
import ServletResponse as sRes
from HttpService import HttpService
from TemplateParser import TemplateParser
from colorama import init
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format
from art import *

#### Sheep Server to Server Static as well as dynamic content
#### Developer can create customized template using ${key}
#### Developer can create custom python scripts to serve as Servlet
#### Right now it is able to support only GET and POST type of Requests

webApps=[]
currentContextName=""
r=0
extension = ".psp"
httpRequest = HttpRequest()

##Processing PSP Content
def processPSPContent(ptr):
  templateParser = TemplateParser() 
  mimetype='text/html'
  sendReply=True
  templateParser.setHttpRequest(httpRequest)
  content = templateParser.parse(ptr.path)
  ptr.send_response(200)
  ptr.send_header('Content-type',mimetype)
  ptr.end_headers()
  ptr.wfile.write(bytes(content,'utf-8'))

##Class to Take care of Server's Configuration
class ServerConfiguration:
  def __init__(self):
    self.port=0
    self.host=""
  def setPortNumber(self,port):
    self.port=port
  def getPortNumber(self):
    return self.port
  def setHost(self,host):
    self.host=host
  def getHost(self):
    return self.host

## Class to take care of WebApplicationConfiguration
class WebApplicationConfiguration:
 def __init__(self):  
  self.homepageName=""
 def setHomepageName(self,homepageName):
  self.homepageName=homepageName
 def getHomepageName(self):
  return self.homepageName

## Class to take care of Web Application
class WebApplication:
 def __init__(self):
  self.contextName=""
  self.webApplicationConfiguration=None
 def setContextName(self,contextName):
  self.contextName=contextName
 def getContextName(self):
  return self.contextName
 def setWebApplicationConfiguration(self,webApplicationConfiguration):
  self.webApplicationConfiguration=webApplicationConfiguration
 def getWebApplicationConfiguration(self):
  return self.webApplicationConfiguration

##Global Function to Populate Web Application List on startup
def getWebApplicationsList():
 webApplications=[]
 files = os.listdir("applications")
 for name in files:
  webApplicationConf=WebApplicationConfiguration()
  if os.path.exists("applications/"+name+"/secured/config.json")==True:
   config=json.loads(open('applications/'+name+'/secured/config.json').read())
  if 'Homepage' not in config:
   webApplicationConf.setHomepageName("index.html")
  else:
   webApplicationConf.setHomepageName(config["Homepage"])
  if os.path.exists("applications/"+name+"/secured/config.json")==False:
   webApplicationConf.setHomepageName("index.html")
  webApplication=WebApplication()
  webApplication.setContextName(name)
  webApplication.setWebApplicationConfiguration(webApplicationConf)
  webApplications.append(webApplication)
 return webApplications

##Utility compareLength function
def compareLength(a):
 webApplicationsList=[]
 webApplicationsList=getWebApplicationsList() 
 found=False
 for i in range(0,len(webApplicationsList)):
  if a==webApplicationsList[i].getContextName():
   found=True
   break
 return found

## Utility Search Position F
def searchPosition(a,str):
 count=-1
 applications=[]
 applications=getWebApplicationsList()
 for k in range(0,len(applications)):
  if a==applications[k].getContextName() or str==applications[k].getContextName():
   count=k
 return count

## Utility function to searchAbsolutePath    
def searchAbsolutePath(pathName):
 if pathName!="/":
  i=len(pathName)-1
  e=i+1
  idx=i
  while i>=0:
    if pathName[i]=="/":
      e-=1
      i-=1
    else:
      break
  if idx!=i:
    pathName=pathName[0:e]
 j=pathName[1:len(pathName)]
 apps=[]
 apps=getWebApplicationsList()
 found=False
 contextNameString=""
 mappingString=""
 for e in range(0,len(j)):
  if(j[e]=="/"):
   contextNameString=j[0:e]
   mappingString=j[e+1:len(j)]
   break
 for i in range(0,len(apps)):
  if(contextNameString==apps[i].getContextName()):
   found=True
   break
 if found==True:
  config=json.loads(open('applications/'+contextNameString+'/secured/config.json').read())
  if 'mappings' not in config:
   pth="applications/"+pth
   return pth
  else:
   mappings=config["mappings"]
   for i in range(0,len(mappings)):
     temp=mappings[i]
     if mappingString==temp["path"]:
      pth="applications/"+contextNameString+"/"+temp["path"]
      return pth
 for r in range(0,len(apps)):
  if(j.startswith(apps[r].getContextName()+"/secured") and j.endswith("html")):
   pth="Root/error.html"
   return pth
 pth=pathName
 str=""
 a=j 
 for x in range(0,len(j)):
  if(j[x]=="/"):
   str=j[0:x]
   break 
 count=searchPosition(a,str)
 if count==-1:
  if pth=="/":
   pth="Root/index.html"
   return pth
  else:
   pth="Root"+pth
 if compareLength(a)==True:
  pth="applications/"+apps[count].getContextName()+"/"+apps[count].getWebApplicationConfiguration().getHomepageName()
  return pth
 else:
  if str==apps[count].getContextName() and (pth.endswith(".jpg") or pth.endswith(".png") or pth.endswith(".txt") or pth.endswith(".css") or pth.endswith(".html") or pth.endswith(extension) or pth.endswith(".gif") or pth.endswith(".js") or pth.endswith(".pdf") or pth.endswith(".mp4")):
   pth="applications"+pth
   if os.path.exists(pth)==False:
    pth="Root/error.html"
    return pth
 if(os.path.exists(pth)==True and (pth.endswith(".jpg")==False and pth.endswith(".txt") and  pth.endswith(".png")==False and pth.endswith(".css")==False and pth.endswith(extension)==False and pth.endswith(".html")==False and pth.endswith(".gif")==False and pth.endswith(".js")==False and pth.endswith(".pdf") and pth.endswith(".mp4")) and pth.startswith("applications")):
  pth="Root/error.html"
  return pth
 return pth
  

## Utility function to populate server configuration  
def populateServerConfiguration():
  serverConfig=json.loads(open('Root/server.json').read())
  serverConfiguration=ServerConfiguration()
  if "port" not in serverConfig:
    serverConfiguration.setPortNumber(8080)
  else:
    serverConfiguration.setPortNumber(int(serverConfig["port"]))
  if "host" not in serverConfig:
    serverConfiguration.setHost("localhost")
  else:
    serverConfiguration.setHost(serverConfig["host"])
  return serverConfiguration

## Utility function to check if method exist
def methodExist(instance,method):
  return hasattr(instance,method)

## Utility function to check is servlet
def isServlet(path):
  try:
   pth=path.split("/")
   contextName=""
   if path.startswith("application"):
     contextName=pth[1]
   with open('applications/'+contextName+'/secured/config.json') as f:
     config=json.load(f)
   if 'mappings' not in config:
     return False
   else:
    mappings=config["mappings"]
    for i in range(0,len(mappings)):
      k=mappings[i]
      if k["path"]==pth[len(pth)-1] and k["isServlet"]==True:
        ss=k["resource"].split(".")
        p="applications/"+contextName
        for i in range(len(ss)):
          p=p+"/"+ss[i]
        p=p+".py"
        if os.path.exists(p):
          return True
        else:
          return False
    return False

  except:
    return False

## utility function to get servlet path
def getServletPath(path):
  pth=path.split("/")
  contextName=""
  if path.startswith("application"):
    contextName=pth[1]
  with open('applications/'+contextName+'/secured/config.json') as f:
    config=json.load(f)
  mappings=config["mappings"]
  for i in range(0,len(mappings)):
    k=mappings[i]
    if k["path"]==pth[len(pth)-1] and k["isServlet"]==True:
      return k["resource"]
  return ""

## utility function to get class name from py file
def getClassName(path):
  pth=path.split("/")
  contextName=""
  if path.startswith("application"):
    contextName=pth[1]
  with open('applications/'+contextName+'/secured/config.json') as f:
    config=json.load(f)
  mappings=config["mappings"]
  for i in range(0,len(mappings)):
    k=mappings[i]
    if k["path"]==pth[len(pth)-1] and k["isServlet"]==True:
      x=k["resource"].split(".")
      return x[len(x)-1]
  return ""


## utility function to check if is path is url
def isUrlPattern(path):
  try:
   pth=path.split("/")
   contextName=""
   if path.startswith("application"):
     contextName=pth[1]
   with open('applications/'+contextName+'/secured/config.json') as f:
     config=json.load(f)
   if 'mappings' not in config:
     return False
   else:
    mappings=config["mappings"]
    for i in range(0,len(mappings)):
      k=mappings[i]
      if k["path"]==pth[len(pth)-1]:
        if "isServlet" not in k:
          ss=k["resource"]
          p="applications/"+contextName+"/"+ss
          if os.path.exists(p):
            return True
          else:
            return False
        else:
          if k["isServlet"]==True:
            return False
          else:
            return True
    return False
  except:
    return False


## utility to extract mime type by path
def getMimeTypeByPath(path):
  pth=path.split("/")
  contextName=""
  if path.startswith("applications"):
    contextName=pth[1]
  with open('applications/'+contextName+'/secured/config.json') as f:
    config=json.load(f)
  mappings=config["mappings"]
  for i in range(0,len(mappings)):
    k=mappings[i]
    if k["path"]==pth[len(pth)-1]:
      if k["resource"].endswith(".txt"):
        return "text/plain"
      if k["resource"].endswith(".html"):
        return "text/html"
      if k["resource"].endswith(".css"):
        return "text/css"
      if k["resource"].endswith(".jpg"):
        return "image/jpg"
      if k["resource"].endswith(".png"):
        return "image/png"
      if k["resource"].endswith(".js"):
        return "application/javascript"
      if k["resource"].endswith(".gif"):
        return "image/gif"
      if k["resource"].endswith(".mp3"):
        return "audio/mpeg"
      if k["resource"].endswith(".mp4"):
        return "video/mp4"
      if k["resource"].endswith(".pdf"):
        return "application/pdf"

  return "text/plain"

## utility function to get value mapped with url
def getValueMappedWithUrl(path):
    pth=path.split("/")
    contextName=""
    if path.startswith("application"):
      contextName=pth[1]
    with open('applications/'+contextName+'/secured/config.json') as f:
      config=json.load(f)
    mappings=config["mappings"]
    for i in range(0,len(mappings)):
      k=mappings[i]
      if k["path"]==pth[len(pth)-1]:
        x=k["resource"]
        return x
    return ""


## Custom wrapper like PrintWriter
class Writer():
  def __init__(self):
    self.dataString=""
    self.container=None
    self.contentType=""
  def getContainer(self):
    return self.container
  def setContainer(self,container):
    self.container=container
  def send(self):
    self.container.send_response(200)
    self.container.send_header("Content-type",self.contentType)
    self.container.end_headers()
    self.container.wfile.write(bytes(self.dataString,"utf8"))
  def setContentType(self,contentType):
    self.contentType=contentType
  def getContentType(self):
    return self.contentType
  def write(self,dataString):
    self.dataString+=dataString

## Utility function to serve custom error page
def serveCustomError(path,ref):
     servletResponse=sRes.ServletResponse()
     servletResponse.setContainer(ref)
     servletResponse.setContentType("text/html")
     w=Writer()
     w.setContentType(servletResponse.getContentType())
     w.setContainer(servletResponse.getContainer())
     servletResponse.setWriter(w)
     writer=servletResponse.getWriter()
     writer.write("<!doctype html>")
     writer.write("<html lang='en'>")
     writer.write("<head>")
     writer.write("<link href='https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@600;900&display=swap' rel='stylesheet'>")
     writer.write("<script src='https://kit.fontawesome.com/4b9ba14b0f.js' crossorigin='anonymous'></script>")
     writer.write("<style>")
     writer.write("body {background-color: #95c2de;}")
     writer.write(".mainbox {background-color: #95c2de;margin: auto;height: 600px;width: 600px;position: relative;}")
     writer.write(".err{color: #ffffff;font-family: 'Nunito Sans', sans-serif;font-size: 11rem;position:absolute;left: 20%;top: 8%;}")
     writer.write(".far {position: absolute;font-size: 8.5rem;left: 42%;top: 15%;color: #ffffff;}")
     writer.write(" .err2 {color: #ffffff;font-family: 'Nunito Sans', sans-serif;font-size: 11rem;position:absolute;left: 68%;top: 8%;}")
     writer.write(".msg {text-align: center;font-family: 'Nunito Sans', sans-serif;font-size: 1.6rem;position:absolute;left: 16%;top: 45%;width: 75%;}")
     writer.write("a {text-decoration: none;color: white;}")
     writer.write("a:hover {text-decoration: underline;}")
     writer.write("</style>")
     writer.write("</head>")
     writer.write("<body>")
     writer.write("<div class='mainbox'>")
     writer.write("<div class='err'>4</div>")
     writer.write("<i class='far fa-question-circle fa-spin'></i>")
     writer.write("<div class='err2'>4</div>")
     writer.write("<div class='msg'><p>Sorry but the url ("+path+") you are trying to reach does not exist &#128373;</p>")
     writer.write("</div>")
     writer.write("</div>")
     writer.write("</body>")
     writer.write("</html>")
     writer.send()

## Base SheepHTTPRequestHandler class
class SheepHTTPRequestHandler(BaseHTTPRequestHandler):
 contextName=""
 queryDict={}
 webApps=getWebApplicationsList()
 def do_GET(self):
  ptth=self.path
  url=populateServerConfiguration().getHost()+":"+str(populateServerConfiguration().getPortNumber())+ptth
  queryDict=dict(parse.parse_qsl(parse.urlsplit(url).query))
  isDictEmpty=not bool(queryDict)
  if(isDictEmpty==False):
    i=self.path.find("?")
    if i!=-1: self.path=self.path[0:i]
    self.path=searchAbsolutePath(self.path)
  else:
    self.path=searchAbsolutePath(self.path)
  if os.path.exists(self.path)==False and isServlet(self.path)==False and isUrlPattern(self.path)==False:
   self.path="Root/error.html"
  try:
   sendReply=False
   if self.path=="Root/error.html":
     serveCustomError(ptth,self)
     return

   if self.path.endswith(".html"):
    mimetype='text/html'
    sendReply=True
    f=open(self.path,'rb')
    self.send_response(200)
    self.send_header('Content-type',mimetype)
    self.end_headers()
    self.wfile.write(f.read())
    f.close()
    return

   if self.path.endswith(extension):
    processPSPContent(self)
    return

   if self.path.endswith(".css"):
    mimetype='text/css'
    sendReply=True
    f=open(self.path,'rb')
    self.send_response(200)
    self.send_header('Content-type',mimetype)
    self.end_headers()
    self.wfile.write(f.read())
    f.close()
    return
    
   if self.path.endswith(".txt"):
    mimetype='text/plain'
    sendReply=True
    f=open(self.path,'rb')
    self.send_response(200)
    self.send_header('Content-type',mimetype)
    self.end_headers()
    self.wfile.write(f.read())
    f.close()
    return

   if self.path.endswith(".jpg"):
    mimetype='image/jpg'
    sendReply=True
    f=open(self.path,'rb')
    self.send_response(200)
    self.send_header('Content-type',mimetype)
    self.end_headers()
    self.wfile.write(f.read())
    f.close()
    return

   if self.path.endswith(".png"):
    mimetype='image/png'
    sendReply=True
    f=open(self.path,'rb')
    self.send_response(200)
    self.send_header('Content-type',mimetype)
    self.end_headers()
    self.wfile.write(f.read())
    f.close()
    return

   if self.path.endswith(".js"):
    mimetype='application/javascript'
    sendReply=True
    f=open(self.path,'rb')
    self.send_response(200)
    self.send_header('Content-type',mimetype)
    self.end_headers()
    self.wfile.write(f.read())
    f.close()
    return

   if self.path.endswith(".gif"):
    mimetype='image/gif'
    sendReply=True
    f=open(self.path,'rb')
    self.send_response(200)
    self.send_header('Content-type',mimetype)
    self.end_headers()
    self.wfile.write(f.read())
    f.close()
    return

   if self.path.endswith(".mp4"):
     mimetype="video/mp4"
     sendReply=True
     f=open(self.path,'rb')
     self.send_response(200)
     self.send_header('Content-type',mimetype)
     self.end_headers()
     self.wfile.write(f.read())
     f.close()
     return

   if self.path.endswith(".pdf"):
     mimetype="application/pdf"
     sendReply=True
     f=open(self.path,'rb')
     self.send_response(200)
     self.send_header('Content-type',mimetype)
     self.end_headers()
     self.wfile.write(f.read())
     f.close()
     return

   if self.path.endswith(".mp3"):
    mimetype='audio/mpeg'
    sendReply=True
    f=open(self.path,'rb')
    self.send_response(200)
    self.send_header('Content-type',mimetype)
    self.end_headers()
    self.wfile.write(f.read())
    f.close()
    return

   if isUrlPattern(self.path):
    pth=self.path.split("/")
    mimetype=getMimeTypeByPath(self.path)
    pthh=pth[0]+"/"+pth[1]+"/"+getValueMappedWithUrl(self.path)
    f=open(pthh,'rb')
    self.send_response(200)
    self.send_header('Content-type',mimetype)
    self.end_headers()
    self.wfile.write(f.read())
    f.close()
    return


   if isServlet(self.path):
     servletResponse=sRes.ServletResponse()
     servletRequest=sReq.ServletRequest()
     servletRequest.setRequestParamDict(queryDict) ##Access to User should be disable
     servletRequest.setHttpRequestWrapper(httpRequest) ## Should be Private
     servletResponse.setContainer(self) ##Access to User should be disable
     w=Writer()
     w.setContentType(servletResponse.getContentType())
     w.setContainer(servletResponse.getContainer())
     servletResponse.setWriter(w)
     pth=self.path.split("/")
     package=pth[0]+"."+pth[1]+"."+getServletPath(self.path)
     module=importlib.import_module(package)
     Test=getattr(module,getClassName(self.path))
     try:
       test=Test()
     except Exception as e:
       raise Exception("Invalid Constructor Type can't instantiate it")
     if isinstance(test,HttpService):
       pass
     if not isinstance(test,HttpService):
       raise Exception("Class "+getClassName(self.path)+" is not an instance of HttpService")
     if methodExist(test,"doGet"):
       test.doGet(servletRequest,servletResponse)
     else:
       raise Exception("No such Method doGet Exists")
     return
  except IOError:
    self.send_response(404)
    self.send_error(404,'Path Not Found ' )

def do_POST(self):
 print("do_POST got invoked")

try:
 PORT_NUMBER=populateServerConfiguration().getPortNumber()
 host=populateServerConfiguration().getHost()
 server=HTTPServer((host,PORT_NUMBER),SheepHTTPRequestHandler)
 pattern = figlet_format("Sheep Server")
 print(pattern)
 print("Started on Port Number "+str(PORT_NUMBER))
 time.sleep(1.5)
 print("***Scanning Folder Structures***")
 time.sleep(2.0)
 apps=getWebApplicationsList()
 for i in range(0,len(apps)):
  print(apps[i].getContextName())
 server.serve_forever()
except KeyboardInterrupt:
 print("Interrupt recieve shutting down the web server")
 server.socket.close()
