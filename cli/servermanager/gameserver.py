"""Games Server with ip and port"""

import abstractserver

from util import get_ip_address

class GameServer(abstractserver.AbstractServer):
  
  def __init__(self, name = None, ip = None, port = None):
    abstractserver.AbstractServer.__init__(self, name)
    #self.ip = ip
    self.ip = get_ip_address('eth0')
    self.port = port

  def print_self(self):
    abstractserver.AbstractServer.print_self(self)
    print("\tIP \t\t: "+ self.ip)
    print("\tport \t\t: "+ str( self.port))
    
