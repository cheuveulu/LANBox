""" Utils """



import socket
import fcntl
import struct

def get_ip_address_by_iface(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_ip_address():
    prefix = 'eth'
    retries = 10
    for i in range(retries):
        try:
            ip = get_ip_address_by_iface('eth' + str(i))
            return ip
        except:
            pass

    return None
