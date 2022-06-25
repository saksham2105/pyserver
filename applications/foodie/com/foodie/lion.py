from HttpService import HttpService
class lion(HttpService):
    def __init__(self):
        self.servletResponse=None
    def doGet(self,servletRequest,servletResponse):
             servletResponse.setContentType("text/html")
             writer=servletResponse.getWriter()
             code = servletRequest.getParameter("code")
             name = servletRequest.getParameter("name")
             salary = servletRequest.getParameter("salary")
             servletRequest.setAttribute("code",code)
             servletRequest.setAttribute("name",name)
             servletRequest.setAttribute("salary",salary)
             writer.write("<!Doctype html>")
             writer.write("<html>")
             writer.write("<head>")
             writer.write("<title>Demo2</title>")
             writer.write("</head>")
             writer.write("<body>")
             writer.write("<h1>Lion</h1>")
             writer.write("<h2>Found "+code+name+salary+"</h2>")
             writer.write("</body>")
             writer.write("</html>")
             writer.send()
