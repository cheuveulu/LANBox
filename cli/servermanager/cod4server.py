import codserver

class Cod4Server(codserver.CodServer):
  
  path = None
  org_binary = None
  pb_binary = None
  nick = 'cod4'


  def __init__(self):
    codserver.CodServer.__init__(self)
