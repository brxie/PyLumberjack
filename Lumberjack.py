import socket
import ssl
from struct import pack
import zlib


        
class Lumberjack(object):
    
    def __init__(self, port, address, sslCert, sslEnabled=True):
        self.opts = {
            'port' : port,
            'address' : address,
            'sslCert' : sslCert,
            'sslEnabled' : sslEnabled
        }
        self.host = self.opts['address']

    def connect(self):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((self.opts['address'], self.opts['port']))
        
        if not self.opts['sslEnabled']:
            self.socket = tcp_socket
        else:
            sslSocket = ssl.wrap_socket(sock=tcp_socket, ca_certs=self.opts['sslCert'], cert_reqs=ssl.CERT_REQUIRED)
            self.socket = sslSocket
            
    def write(self, elements):
        self.__sendWindowSize()
        payload = self.__encode(elements)
        payload = self.__compress(payload)
        self.socket.write(payload)
        
    def __encode(self, elements):
        frame = [0x31, 0x44, 0x00]
        packParam = '>BBi'
        frame.append( len(elements) )
        packParam += 'i'
        
        for key, value in elements.iteritems():
            keyLen = len(key)
            valLen = len(value)
            frame.append(keyLen)
            packParam += 'i'
            frame.append(key)
            packParam += str(keyLen) + 's'
            frame.append(valLen)
            packParam += 'i'
            frame.append(value)
            packParam += str(valLen) + 's'
            
        payload = pack(packParam, *frame)
        return payload
        
    def __sendWindowSize(self):
        winSize = pack('>BBi', 0x31, 0x57, 0x01)
        self.socket.write(winSize)
        
    def __compress(self, payload):
        compPayld = zlib.compress(payload)
        compSize = ( len(compPayld) )
        compress = pack('>BBi%ss' % compSize, 0x31, 0x43, compSize, compPayld)
        return compress
        
    

if __name__ == '__main__':
    l = Lumberjack(port = 8662,
               address = '127.0.0.1',
               sslCert = '/certs/cert.crt'
            )
    l.connect()
    l.write({"line":"foobar"})
