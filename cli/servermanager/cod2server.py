"""Classes for Cod2 servers"""

import codserver

class Cod2Server(codserver.CodServer):
  "Call of duty 2 server"
  path = None
  org_binary = None
  pb_binary = None
  nick = 'cod2'
  
  def __init__(self):
    codserver.CodServer.__init__(self)
    

