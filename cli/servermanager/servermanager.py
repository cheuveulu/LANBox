"""Main class for control"""
import optparse,sys,os

import configreader
import cod2server,cod4server,codserver


class ServerManager:
  
  def __init__(self):
    self.config = configreader.ConfigReader()
    self.servers = self.config.parse()
#    self.servers = self.config.parse("servermanager.cfg")
    self.forced = False
    self.check_root()
    
  def print_conf(self, option=None, opt_str=None , value=None , parser=None, args=None, kwargs=None):
    print("### Games settings ###")
    print("Users : ")
    print("\torg \t\t: " + str(codserver.CodServer.org_user) )
    print("\tpb\t\t: " + str(codserver.CodServer.pb_user) )
    print("".rjust(96, "-") )
    form = '| {0:8.8} | {1:25.25} | {2:25.25} | {3:25.25} |'
    print form.format('Name', 'Path', 'Org Binary', 'PB Binary')
    print("".rjust(96, "-") )
    print form.format(
        'Cod2',
        str(cod2server.Cod2Server.path),
        str(cod2server.Cod2Server.org_binary),
        str(cod2server.Cod2Server.pb_binary))
    print form.format(
        'Cod4',
        str(cod4server.Cod4Server.path),
        str(cod4server.Cod4Server.org_binary),
        str(cod4server.Cod4Server.pb_binary))
    print("".rjust(96, "-") )

    print("")
    print("###Servers list###")
    width = 111
    print("".rjust(width, "-") )
    form = '| {0:13.13} | {5:1} | {6:1} | {7:2} | {1:15} | {2:5} | {3:25.25} | {4:25.25} |'
    print form.format('Name', 'IP', 'Port', 'fs_game', 'Config', 'B', 'P', 'PB')
    print("".rjust(width, "-") )
    for server in self.servers:
      print form.format(
        server.name,
        server.ip,
        server.port,
        server.fsgame,
        server.config,
        'X' if server.onboot else '-',
        'X' if server.protected else '-',
        'X' if server.pb else '-',
        )
       #server.print_self()
    print("".rjust(width, "-") )
    exit(0)

  def print_running(self, option=None, opt_str=None , value=None , parser=None, args=None, kwargs=None):
    print("### Running Servers ###");
    width = 74
    print("".rjust(width, "-") )
    header = ['Name', 'IP', 'Port', 'fs_game']
    print '| {0:^16} | {1:^15} | {2:^5} | {3:25.25} |'.format(*header)
    print("".rjust(width, "-") )
    form = '| {0:16.16} | {1:15} | {2:5} | {3:25.25} |'
    for server  in self.servers:
      if(server.getpid(False) != None):
        print form.format(server.name, server.ip, server.port, server.fsgame)
    print("".rjust(width, "-") )
    exit(0)


  def find_game(self, gamename):
    for server in self.servers:
      
      if server.name == gamename:
        return server
    
    print("Unknown game " + gamename)
    exit(1)

  def start_game(self, gamename):
    self.find_game(gamename).start()
        
  
  def stop_game(self, gamename):
    self.find_game(gamename).stop()
        
  
  def resume_game(self, gamename):
    self.find_game(gamename).resume()
        
  def restart_game(self, gamename):
    self.find_game(gamename).restart()
  
  def boot_start(self):
    print("Starting all servers")
    for server in self.servers:
      if server.onboot == True:
        server.start()

  def boot_stop(self):
    print("Stopping all servers")
    for server in self.servers:
      if server.onboot == True:
        server.stop()
    
  def boot_restart(self):
    print("Restarting all servers")
    for server in self.servers:
      if server.onboot == True:
        server.restart()
  
  def boot_parse(self, arg):
    if(arg == "start"):
      self.boot_start()
    elif(arg == "stop"):
      self.boot_stop()
    elif(arg == "restart"):
      self.boot_restart()
    exit(0)
  
  def parse_args(self):
    options = None
    args = None
      
    
    parser = optparse.OptionParser()
    parser.add_option('-l', '--list', help="List all configured servers and exit",  action="callback", callback=self.print_conf)
    parser.add_option('-r', '--running', help="List running servers and exit",  action="callback", callback=self.print_running)
    parser.add_option('-f', '--force', help="Force protected servers to be stopped", action="store_true", dest="forced")
    
    (options,args) = parser.parse_args()
    
    
    #print(str(options) + " " + str(args))
    
    #print(str(args[0]))

    if(options.forced == True):
      self.forced = True
    
    if(len(args )== 1):
      self.boot_parse(args[0])
     
    elif(len(args) == 2):
      if(args[1] == "start"):
        self.start_game(args[0])
      elif(args[1] == "stop"):
        self.stop_game(args[0])
      elif(args[1] == "resume"):
        self.resume_game(args[0])
      elif(args[1] == "restart"):
        self.restart_game(args[0])
      else:
        print("no action to do")
    else:
      print("Nothing to do")
        
  def check_root(self):
    if(os.getuid() != 0):
      print("You must be root to run this program")
      exit(1)
    
    
  
