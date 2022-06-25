from HttpService import HttpService
class rabbit(HttpService):
    def __init__(self):
        self.servletResponse=None
    def doGet(self,servletRequest,servletResponse):
             servletResponse.setContentType("text/html")
             servletRequest.setAttribute("name",servletRequest.getParameter("name"))
             writer=servletResponse.getWriter()
             writer.write("<!Doctype html>")
             writer.write("<html>")
             writer.write("<head>")
             writer.write("<title>Demo</title>")
             writer.write("</head>")
             writer.write("<body>")
             writer.write("<h1>Rabbit</h1>")
             writer.write("<h2>"+servletRequest.getAttribute("name")+"</h2>")
             writer.write("</body>")
             writer.write("</html>")
             writer.send()
