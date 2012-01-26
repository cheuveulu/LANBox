# Create your views here.
import time, json
from django.http import HttpResponse

from cod.models import Server

from django.shortcuts import render_to_response

class Message(json.JSONEncoder):
    status = 'INFO'
    message = ''
    
    ''' Encode Message class to json object for javascript '''
    def default(self, obj):
        if isinstance (obj, Message):
            return {'status': self.status, 'message': self.message}
        return json.JSONEncoder.default(self, obj)

    ''' Dump itself to json object '''
    def toJSON(self):
        return self.encode(self)

    ''' return a new message obj'''
    @staticmethod
    def get_new_msg(status, message):
        msg = Message()
        msg.status = status
        msg.message = message
        return msg
    
    @staticmethod
    def err(message):
        return Message.get_new_msg('ERROR', message)
    
    @staticmethod
    def info(message):
        return Message.get_new_msg('INFO', message)
    
    @staticmethod
    def warn(message):
        return Message.get_new_msg('WARNING', message)
        


def home(request):
    servers_list = Server.objects.all()
    return render_to_response('cod/server.html', {'servers_list' :servers_list})


# Server action from interface
def server_ajax_command(request, pk, action):
    try:
        server = Server.objects.get(pk=pk)
        if action == 'start':
            result = server.start()
        elif action == 'stop':
            result = server.stop()
        elif action == 'restart':
            result = server.restart()
        if result != False:
            msg = Message.info('pid = ' + str(server.pid) + "<br>" + str(result))
            return HttpResponse(msg.toJSON())
        else:
            msg = Message.err(str(result))
            return HttpResponse(msg.toJSON())
    except Server.DoesNotExist:
        msg = Message.err("Server not found")
        return HttpResponse(msg)

        
