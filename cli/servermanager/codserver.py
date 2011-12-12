"""Classes for Cod servers"""
import os,pwd,subprocess,shlex,sys,time

import gameserver

class CodServer(gameserver.GameServer):
  "Call of duty 2 server"
 
  org_user = None
  pb_user = None
 
  def __init__(self):
    gameserver.GameServer.__init__(self)
    self.config = None
    self.fsgame = None
    self.pb = None

  def getUser(self):
    if self.pb :
      return self.pb_user 
    else: 
      return self.org_user

  def print_self(self):
    gameserver.GameServer.print_self(self)
    print("\tconfig \t\t: "+ self.config)
    print("\tfsgame \t\t: "+ self.fsgame)
    print("\tpb\t\t: "+ str( self.pb))

    
  
  def start(self):
    if self.getpid() != None:
      print "Server already running"
      return False
    else:
      cmd = ""
      cmd += "su " + self.getUser() 
      cmd += " -c '"
      cmd += self.path
      if self.pb:
        cmd += self.pb_binary + " "
      else:
        cmd += str(self.org_binary) + " "
      
      cmd += "+set dedicated 1 "
      if self.fsgame != "":
        cmd += "+set fs_game "+ str(self.fsgame) + " "
      
      cmd += "+exec " + str(self.config) + " "
      cmd += "+set net_ip " + str(self.ip )+ " "
      cmd += "+set net_port " + str(self.port) + " "
      url = 'http://' + str(self.ip) + "/" + self.nick
      cmd += "+seta sv_wwwbaseurl " + '\\\"' + url + '\\\"' + " "
      cmd += "+map_rotate'"
      
      print("Starting "+ str(self.name))
      
      print(cmd)
      
      #self.setuser()
      #print("UID = " + str(os.getuid()))
      
      cmd = self.screen_path + " -DmS " + str(self.name) + " " + cmd
      #print(cmd)
      
      #cmd = "/usr/bin/env"
      p = subprocess.Popen(shlex.split(cmd), cwd = self.path)
      self.write_pid(p.pid)
      return True


  def resume(self):
    pid = self.getpid()
    if pid != None:
      cmd = ""
      cmd += self.screen_path +" -dr "
#      cmd += self.getUser() + "/"
      cmd += pid
      
      #print cmd
      os.execvp(self.screen_path, shlex.split(cmd));
    else:
      print(self.name + " is not running")
  
  def setuser(self):
    uid = pwd.getpwnam(self.getUser())[2]
    
    os.setuid(uid)
    
  
  def stop(self):
    pid = self.getpid()
    if pid == None:
      print("Server "+ self.name+ " is not running")
      return False
    else:
      print("Stopping server : "+ self.name)
      cmd = ""
      cmd += self.screen_path +" -S "
      #cmd += self.getUser() + "/"
      cmd += pid + " "
      cmd += "-p 0 -X stuff "
      
      screen_cmd = """
quit
"""
      #print (cmd)
      final_cmd = shlex.split(cmd)
      final_cmd.append(screen_cmd)
      p = subprocess.Popen(final_cmd, universal_newlines=True)
      return True
     
  def restart(self):
    retry = 5
    sleep = 2
    self.stop()
    while( (retry > 0) and  (self.start() == False) ):
      print "Waiting for server to close"
      time.sleep(sleep)
      retry -= 1
      
    
    
