#!/usr/bin/env python
import socket
import ssl
from struct import pack, unpack
import zlib


class ConnectionException(Exception):
    pass

class Client(object):
    
    def __init__(self, port, address, sslCert, ackEnabled=True, sslEnabled=True):
        self.opts = {
            'port' : port,
            'address' : address,
            'sslCert' : sslCert,
            'ackEnabled' : ackEnabled,
            'sslEnabled' : sslEnabled
        }
        self.host = self.opts['address']
        self.WINDOW_SIZE = 500
        self.SEQUENCE_MAX = 0x3FFFFFFFFFFFFFFF
        self.sequence = 0
        self.lastAck = 0


    def connect(self):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((self.opts['address'], self.opts['port']))
        
        if not self.opts['sslEnabled']:
            self.socket = tcp_socket
        else:
            sslSocket = ssl.wrap_socket(sock=tcp_socket,
                                        ca_certs=self.opts['sslCert'],
                                        ssl_version=ssl.PROTOCOL_TLSv1,
                                        cert_reqs=ssl.CERT_REQUIRED
                                        )
            self.socket = sslSocket
        self.__sendWindowSize()

    def write(self, elements):
        self.__incSeq()

        payload = self.__encode(elements)
        compPayld = self.__compress(payload)

        # SSL and TLS channels must be segmented into records of no more than 16Kb
        chunker = lambda pack, segSize=8192 : [pack[i:i+segSize] for i in range(0, len(pack), segSize)]
        for segment in chunker(compPayld):
            self.socket.write(segment)

        if self.opts['ackEnabled']:
            while (self.sequence - (self.lastAck + 1)) >= self.WINDOW_SIZE:
                self.__ack()

    def __incSeq(self):
        self.sequence += 1
        if self.sequence > self.SEQUENCE_MAX:
            self.sequence  = 0

    def __encode(self, elements):
        frame = [0x31, 0x44, self.sequence]
        packParam = '>BBI'
        frame.append( len(elements) )
        packParam += 'I'
        
        for key, value in elements.iteritems():
            keyLen = len(key)
            valLen = len(value)
            frame.append(keyLen)
            packParam += 'I'
            frame.append(key)
            packParam += str(keyLen) + 's'
            frame.append(valLen)
            packParam += 'I'
            frame.append(value)
            packParam += str(valLen) + 's'
            
        payload = pack(packParam, *frame)
        return payload

    def __sendWindowSize(self):
        winSize = pack('>BBI', 0x31, 0x57, self.WINDOW_SIZE)
        self.socket.write(winSize)

    def __compress(self, payload):
        compPayld = zlib.compress(payload)
        compSize = ( len(compPayld) )
        compress = pack('>BBI%ss' % compSize, 0x31, 0x43, compSize, compPayld)
        return compress

    def __ack(self):
        self.socket.recv(1) # version. Must be received before ACK type
        atype = self.socket.recv(1)
        ackOK = lambda x=None : False if not atype or unpack('B', atype)[0] != 0x41 else True
        if not ackOK():
            raise ConnectionException('ACK not recived')
        lastAck = self.socket.recv(4)
        self.lastAck, = unpack('>I', lastAck)


if __name__ == '__main__':
    l = Client(port = 8662,
               address = '127.0.0.1',
               sslCert = '/certs/cert.crt'
            )
    l.connect()
    l.write({"line":"foobar"})
