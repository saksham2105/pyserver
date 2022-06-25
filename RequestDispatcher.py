import os
import json
class RequestDispatcher():
    def __init__(self):
        self.contextName=""
        self.servletRequest=None
        self.servletResponse=None
    def isServlet(self,path):
        try:
            pth=path.split("/")
            ctxName=""
            if path.startswith("application"):
                ctxName=pth[1]
            with open("applications/"+ctxName+"/secured/config.json") as f:
                config=json.loads(f)
            if 'mappings' not in config:
                return False
            else:
                mappings=config["mappings"]
                for i in range(0,len(mappings)):
                    k=mappings[i]
                    if k["path"]==pth[len(pth)-1] and k["isServlet"]==True:
                        ss=k["resource"].split(".")
                        p="applications/"+ctxName
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

    def setContextName(self,contextName):
        self.contextName=contextName
    def getContextName(self):
        return self.contextName
    def setServletResponse(self,servletResponse):
        self.servletResponse=servletResponse
    def getServletResponse(self):
        return self.servletResponse
    def setServletRequest(self,servletRequest):
        self.servletRequest=servletRequest
    def getServletRequest(self):
        return self.setServletRequest
    def forward(self,url):
        path="application/"+getContextName()+url
        if os.path.exists(path)==False:
            writer=self.servletResponse.getWriter()
            self.servletResponse.setContentType("text/html")
            writer.setContentType(self.servletResponse.getContentType())
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
            writer.write("<div class='msg'><p>Sorry but the url ("+url+") you are trying to reach does not exist &#128373;</p>")
            writer.write("</div>")
            writer.write("</div>")
            writer.write("</body>")
            writer.write("</html>")
            writer.send()


        if url.endswith(".html"):
            container=self.servletResponse.getContainer()
            mimetype='text/html'
            sendReply=True
            f=open(path,'rb')
            container.send_response(200)
            container.send_header('Content-type',mimetype)
            container.end_headers()
            container.wfile.write(f.read())
            container.close()
            return

        if url.endswith(".css"):
            container=self.servletResponse.getContainer()
            mimetype='text/css'
            sendReply=True
            f=open(path,'rb')
            container.send_response(200)
            container.send_header('Content-type',mimetype)
            container.end_headers()
            container.wfile.write(f.read())
            container.close()
            return

        if url.endswith(".txt"):
            container=self.servletResponse.getContainer()
            mimetype='text/plain'
            sendReply=True
            f=open(path,'rb')
            container.send_response(200)
            container.send_header('Content-type',mimetype)
            container.end_headers()
            container.wfile.write(f.read())
            container.close()
            return
        
        if url.endswith(".jpg"):
            container=self.servletResponse.getContainer()
            mimetype='image/jpg'
            sendReply=True
            f=open(path,'rb')
            container.send_response(200)
            container.send_header('Content-type',mimetype)
            container.end_headers()
            container.wfile.write(f.read())
            container.close()
            return

        if url.endswith(".png"):
            container=self.servletResponse.getContainer()
            mimetype='image/png'
            sendReply=True
            f=open(path,'rb')
            container.send_response(200)
            container.send_header('Content-type',mimetype)
            container.end_headers()
            container.wfile.write(f.read())
            container.close()
            return
        
        if url.endswith(".js"):
            container=self.servletResponse.getContainer()
            mimetype='application/javascript'
            sendReply=True
            f=open(path,'rb')
            container.send_response(200)
            container.send_header('Content-type',mimetype)
            container.end_headers()
            container.wfile.write(f.read())
            container.close()
            return
        
        if url.endswith(".gif"):
            container=self.servletResponse.getContainer()
            mimetype='image/gif'
            sendReply=True
            f=open(path,'rb')
            container.send_response(200)
            container.send_header('Content-type',mimetype)
            container.end_headers()
            container.wfile.write(f.read())
            container.close()
            return

        if url.endswith(".mp4"):
            container=self.servletResponse.getContainer()
            mimetype='video/mp4'
            sendReply=True
            f=open(path,'rb')
            container.send_response(200)
            container.send_header('Content-type',mimetype)
            container.end_headers()
            container.wfile.write(f.read())
            container.close()
            return

        if url.endswith(".pdf"):
            container=self.servletResponse.getContainer()
            mimetype='application/pdf'
            sendReply=True
            f=open(path,'rb')
            container.send_response(200)
            container.send_header('Content-type',mimetype)
            container.end_headers()
            container.wfile.write(f.read())
            container.close()
            return

        if url.endswith(".mp3"):
            container=self.servletResponse.getContainer()
            mimetype='audio/mp3'
            sendReply=True
            f=open(path,'rb')
            container.send_response(200)
            container.send_header('Content-type',mimetype)
            container.end_headers()
            container.wfile.write(f.read())
            container.close()
            return
        
        if isServlet(path):
            pass














        