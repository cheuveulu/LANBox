
from django.db import models
import psutil, subprocess, shlex, os


# Linux user who will run the game server
class SysUser(models.Model):

    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


# Game class with path to game file
class Game(models.Model):
    name = models.CharField(max_length=64)
    path = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='icons/', null=True)
    binary = models.CharField(max_length=64)
    nick = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

# A server instance 
class Server(models.Model):
    name = models.CharField(max_length=64)
    game = models.ForeignKey(Game)
    user = models.ForeignKey(SysUser)
    ip = models.IPAddressField(null=True)
    port  = models.IntegerField()
    config_file = models.CharField(max_length=64)
    fs_game = models.CharField(max_length=64, null=True)
    onboot = models.BooleanField()
    protected = models.BooleanField()
    pid = models.PositiveSmallIntegerField(null=True)
    password = models.CharField(max_length=64, null=True)
    rcon_password = models.CharField(max_length=64, null=True)

    screen_path = '/usr/bin/screen'

    def __unicode__(self):
        return self.game.name + " : " + self.name


    # Get pid of running server and check if server is still running
    def getpid(self, out = False):
        if not psutil.pid_exists(self.pid) or self.pid == 0:
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
            cmd += "sudo -u " + self.user.name
            cmd += " " 
            cmd += self.game.path + '/'
            cmd += self.game.binary + " "
            
            cmd += "+set dedicated 1 "
            if self.fs_game != "":
                cmd += "+set fs_game 'Mods/"+ str(self.fs_game) + "' "
            
            cmd += "+exec " + str(self.config_file) + " "
            cmd += "+set net_ip " + str(self.ip )+ " "
            cmd += "+set net_port " + str(self.port) + " "
            url = 'http://' + str(self.ip) + "/" + self.game.nick
            cmd += "+seta sv_wwwbaseurl " + '\\\"' + url + '\\\"' + " "
            cmd += "+map_rotate"
            
            cmd = self.screen_path + " -DmS " + self.game.nick + '_' + str(self.id) + " " + cmd
            
            print cmd
            split_cmd = shlex.split(str(cmd))
            print str(split_cmd)
            os.chdir(self.game.path)
            p = subprocess.Popen(split_cmd, cwd = self.game.path)
            self.write_pid(p.pid)
            return "Server Started"


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
            return True
         
    def restart(self):
        retry = 5
        sleep = 2
        self.stop()
        while( (retry > 0) and    (self.start() == False) ):
            time.sleep(sleep)
            retry -= 1
            
