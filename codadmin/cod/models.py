
from django.db import models
import subprocess, shlex, os, time

from util import get_ip_address

# Linux user who will run the game server
class SysUser(models.Model):

    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


# Game class with path to game file
class Game(models.Model):
    name = models.CharField(max_length=64)
    path = models.CharField(max_length=255)
    # Optional field , null and blank have to be set and db altered
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    binary = models.CharField(max_length=64)
    nick = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

# A server instance 
class Server(models.Model):
    name = models.CharField(max_length=64)
    game = models.ForeignKey(Game)
    user = models.ForeignKey(SysUser)
    ip = models.IPAddressField(null=True, blank=True)
    port  = models.IntegerField(null=True, blank=True)
    config_file = models.CharField(max_length=64)
    fs_game = models.CharField(max_length=64, null=True, blank=True)
    onboot = models.BooleanField()
    protected = models.BooleanField()
    pid = models.PositiveSmallIntegerField(null=True, blank=True)
    password = models.CharField(max_length=64, null=True, blank=True)
    rcon_password = models.CharField(max_length=64, null=True, blank=True)

    screen_path = '/usr/bin/screen'

    def __unicode__(self):
        return self.game.name + " : " + self.name

    def get_ip(self):
        if self.ip == '':
            return get_ip_address()
        else:
            return self.ip

    # Get pid of running server and check if server is still running
    def getpid(self, out = False):
        if self.pid == 0:
            return None

        try:
            # We send a 0 signal to the process to check if he is still running
            # This will fail if the process is not running or we cannot send signal to it.
            os.kill(self.pid, 0)
        except OSError:
            # The process doesn't exists anymore
            self.write_pid(0)
            return None

        return self.pid
      
    def write_pid(self, pid):
        if pid == None:
            pid = 0
        self.pid = pid
        self.save()

    # Start a server inside a screen
    def start(self):
        if self.getpid() != None:
            print "Server already running"
            return False
        else:
            
            cmd = ""
            # Run the command with sudo for the user.
            # -H is to set home of the target user.
            cmd += "sudo -H -u " + self.user.name
            cmd += " " 
            cmd += self.game.path + '/'
            cmd += self.game.binary + " "
            
            # dedicated 1 = LAN, 2 = internet
            cmd += "+set dedicated 1 "
            if self.fs_game != "":
                cmd += "+set fs_game 'Mods/"+ str(self.fs_game) + "' "
            
            cmd += "+exec config/" + str(self.config_file) + " "
            cmd += "+set net_ip " + str(self.get_ip() )+ " "
            cmd += "+set net_port " + str(self.port) + " "
            url = 'http://' + str(self.get_ip()) + "/dl/" + self.game.nick
            cmd += "+seta sv_wwwbaseurl " + '\\\"' + url + '\\\"' + " "
            cmd += "+map_rotate"
            
            cmd = self.screen_path + " -DmS " + self.game.nick + '_' + str(self.id) + " " + cmd
            
            print cmd
            split_cmd = shlex.split(str(cmd))
            print str(split_cmd)
            self.run_and_exit(split_cmd, self.game.path)
            return "Server Started"

    # Fork and run the screen process so it can detach from our main process.
    # This is for daemonizing the screen process.
    def run_and_exit(self, cmd, path):
        try:
            pid = os.fork()
        except OSError , e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)
        
        if pid == 0:
            # We are the first child
            os.setsid()
            
            p = subprocess.Popen(cmd, cwd = path)
            self.write_pid(p.pid)

            os._exit(0)

        else:
            #We are the parent
            # Wait for the child to save pid to db and exit
            os.wait()
            self.pid = Server.objects.get(id=self.id).pid
            return self.pid
            

    def resume(self):
        pid = self.getpid()
        if pid != None:
            cmd = ""
            cmd += self.screen_path +" -dr "
            cmd += pid
            
            os.execvp(self.screen_path, shlex.split(cmd));
        else:
            print(self.name + " is not running")
    
    def setuser(self):
        uid = pwd.getpwnam(self.getUser())[2]
        
        os.setuid(uid)
        
    
    def stop(self):
        pid = self.getpid()
        if pid == None:
            return False
        else:
            cmd = ""
            cmd += self.screen_path +" -S "
            cmd += str(pid) + " "
            cmd += "-p 0 -X stuff "
            
            screen_cmd = """
quit
"""
            final_cmd = shlex.split(cmd)
            final_cmd.append(screen_cmd)
            p = subprocess.Popen(final_cmd, universal_newlines=True)
            p.wait()
            return True
         
    def restart(self):
        retry = 5
        sleep = 2
        self.stop()
        while( (retry > 0) and    (self.start() == False) ):
            time.sleep(sleep)
            retry -= 1
            
