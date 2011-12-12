"""Class for reading config and create an array of game servers"""

import ConfigParser
import cod2server
import cod4server
import codserver

class ConfigReader:
  
  
  def __init__(self):
    self.config = ConfigParser.SafeConfigParser()
    
    
  def parse(self,fname = "/etc/servermanager.cfg"):
    self.config.read(fname)
    sections = self.config.sections()
    servers = []
    
    
    for section in sections:
      #If section is a game configuration
      #print(section)
      if section[:5].lower() == "game_":

        if section[5:].lower() == "cod2":
          cod2server.Cod2Server.path = self.config.get(section, "path")
          cod2server.Cod2Server.org_binary = self.config.get(section, "org_binary")
          cod2server.Cod2Server.pb_binary = self.config.get(section, "pb_binary")
          
        elif section[5:].lower() == "cod4":
          cod4server.Cod4Server.path = self.config.get(section, "path")
          cod4server.Cod4Server.org_binary = self.config.get(section, "org_binary")
          cod4server.Cod4Server.pb_binary = self.config.get(section, "pb_binary")
      
      elif section.lower() == "users":
        codserver.CodServer.org_user = self.config.get(section, "org")
        codserver.CodServer.pb_user = self.config.get(section, "pb")
      
      #Else we can assume it's a server configuration
      else:
        servers.insert(0,self.__get_servers(section))
        
    #End for section in sections
    return servers
  
  
  def __get_servers(self, serv):
  
    game = self.config.get(serv, "game").lower()
    #print(serv)
    if game == "cod2":
      cod = cod2server.Cod2Server()
    elif game == "cod4":
      cod = cod4server.Cod4Server()
    else:
      print("Error unknown game : "+game)
      cod = None
      
    if cod != None:
      cod.name = serv
      #cod.ip = self.config.get(serv, "ip")
      cod.port = self.config.getint(serv, "port")
      cod.config = self.config.get(serv, "config")
      cod.fsgame = self.config.get(serv, "fsgame")
      cod.pb = self.config.getboolean(serv, "pb")
      cod.onboot = self.config.getboolean(serv, "onboot")
      cod.protected = self.config.getboolean(serv, "protected")
      #cod.print_self()
    
    
    return cod
