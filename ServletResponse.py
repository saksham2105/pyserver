class ServletResponse():
  def __init__(self):
    self.writer=None
    self.contentType=""
    self.container=""
  def setContainer(self,container):
    self.container=container
  def getContainer(self):
    return self.container
  def getWriter(self):
    return self.writer
  def setWriter(self,writer):
    self.writer=writer
  def setContentType(self,contentType):
    self.contentType=contentType
  def getContentType(self):
    return self.contentType
