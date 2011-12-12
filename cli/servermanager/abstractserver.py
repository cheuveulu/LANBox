"""Classes for servers"""

import psutil,os.path

class AbstractServer:
  "Abstract class containing basic info"
  screen_path = "/usr/bin/screen"
  run_dir = "/var/run/servermanager"
  
  def __init__(self, name = None, onboot = False, protect=False):
    self.name = name
    self.onboot = onboot
    self.protected = protect
    
  def start(self):
    print("Starting " + str(self.name) )
  
  def stop(self):
    print ("Stopping " + str(self.name) )
  
  def resume(self):
    print ("Starting "+ str(self.name))
  
  def restart(self):
    self.stop()
    self.start()

  def print_self(self):
    print("\tName \t\t: "+self.name)
    print("\tOnboot \t\t: "+str(self.onboot))
    print("\tProtected \t: "+str(self.protected))
    
  def getpid(self, out = False):
    try:
      f = open(self.getpidfile(), "r")
      pid = f.read()
      f.close()
      if not psutil.pid_exists(int(pid)):
        if(out):
          print("The server dosen't seams to be running. Removing stale pid file")
        os.remove(self.getpidfile())
        return None
      return pid
    except IOError: 
      return None
      
  def getpidfile(self):
    return self.run_dir + "/" + self.name

  def write_pid(self, pid):
    if not os.path.exists(self.run_dir):
      os.mkdir(self.run_dir)
    try:
      f = open(self.getpidfile(), "w")
      f.write(str(pid))
      f.close()
    except IOError:
      print("Unable to write pid file")
