''' 
    This class provides transmitting pixel pairs via udp connection
    Made by Andrey Underoak(https://github.com/AndreyUnderoak) & Nancy Underoak(https://github.com/NancyUnderoak)
'''
import socket

class Transmitter():
    def __init__(self, address, port, max_px_pairs):
        #constants
        self.address = address
        self.port = port
        #set buffer size = size of int type * pair * max_px_pairs
        self.buffer_size = 4 * 5 * max_px_pairs
        #init socket
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def send(self, pairs):
        byte_pairs = self.array_to_bytes(pairs)
        # print(byte_pairs)
        # print(byte_pairs[0])
        # p_pairs = self.bytes_to_array(byte_pairs)
        # print(p_pairs)
        self.UDPClientSocket.sendto(bytes(byte_pairs), (self.address, self.port))

    #Big endian
    def array_to_bytes(self, array):
        res = []
        for a in array:
            res.append(a>>8 & 0xFF)
            res.append(a & 0xFF)
        return res
    
    def bytes_to_array(self, array):
        res = []
        for i in range(len(array)):
            if(i%2==0):
                res.append(array[i]<<8 | array[i+1])
        return res