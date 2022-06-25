from HttpService import HttpService

class User():
    def __init__(self):
        self.username = ""
        self.password = ""
    def setUserName(self,username):
        self.username = username
    def getUserName(self):
        return self.username
    def setPassword(self,password):
        self.password = password
    def getPassword(self):
        return self.password

class register(HttpService):
    def __init__(self):
        self.servletResponse=None
    def doGet(self,servletRequest,servletResponse):
             servletResponse.setContentType("text/html")
             writer=servletResponse.getWriter()
             username = servletRequest.getParameter("username")
             password = servletRequest.getParameter("password")
             user = User()
             user.setUserName(username)
             user.setPassword(password)
             servletRequest.setAttribute("user",user)
             writer.write("<!Doctype html>")
             writer.write("<html>")
             writer.write("<head>")
             writer.write("<title>App 1</title>")
             writer.write("</head>")
             writer.write("<body>")
             writer.write("<h1>User Registered successfully with username as "+username+"</h1>")
             writer.write("</body>")
             writer.write("</html>")
             writer.send()
