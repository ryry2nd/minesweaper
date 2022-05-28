"""
gets the local ip
"""
#imports socket
import socket

#the main function
def getLocalIp():
    # makes a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # connects it to 8.8.8.8
    s.connect(("8.8.8.8", 80))
    # gets the ip address
    name = s.getsockname()[0]
    # closes the socket
    s.close()
    # returns the name
    return name