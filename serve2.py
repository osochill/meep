import socket
import time

from meep_example_app import MeepExampleApp, initialize

headers_to_environ = {
    'host' : 'HTTP_HOST',
    'connection' : 'HTTP_CONNECTION',
    'user-agent' : 'HTTP_USER_AGENT',
    'accept' : 'HTTP_ACCEPT',
    'referer': 'HTTP_REFERER',
    'accept-encoding': 'HTTP_ACCEPT_ENCODING',
    'accept-language': 'HTTP_ACCEPT_LANGUAGE',
    'accept-charset': 'HTTP_ACCEPT_CHARSET',
    'cookie': 'HTTP_COOKIE'
}

class serve():
    def __init__(self,connection, address):
        self.connection = connection
        self.address = address
   
    def start_response(self,status,header):
        self.status = status
        self.header = header

    def respond(self, body):
        response=[]

        response.append('HTTP/1.0 '+self.status)
        response.extend([x+': '+y for x,y in self.header])
        response.append('Date: ' + time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime()))
        response.append('Server: WSGIServer/0.1 Python/2.7')
        response.append('\r\n')
        response.extend(body)

        self.connection.send('\r\n'.join(response))


def process_request(request):
    environ = {}
    for line in request:
        line = line.strip()
        print (line,)
        if line == '':
            continue
        if line.startswith('get') or line.startswith('post'):
            line = line.split()
            environ['REQUEST_METHOD'] = line[0]
            environ['PATH_INFO'] = line[1]
        else:
            line = line.split(':', 1)
            try:
                environ[headers_to_environ[line[0]]] = line[1].strip()
            except KeyError:
                pass

    return environ



def main():
    HOST = ''
    PORT = 8000

    initialize()
    app = MeepExampleApp()


    app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app_socket.bind((HOST, PORT))
    app_socket.listen(1)

    print "entering while"

    while 1:
        connection, address = app_socket.accept()
        print 'Connected by', address

        data = connection.recv(4096)
        if data:
            print (data,)
            environ = process_request(data.lower().split('\r\n'))
            responder = serve(connection, address)
            responder.respond(app(environ, responder.start_response))

    conn.close()


if __name__ == "__main__":
    main()