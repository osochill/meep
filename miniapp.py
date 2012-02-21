from meep_example_app import MeepExampleApp, initialize
import datetime
from collections import deque


def main():
    initialize()
    app = MeepExampleApp()
    environ = {}

    def custom_start_response(status, headers):
        print "HTTP/1.0", status
        print "Date:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print "Server: CustomServer/0.1 Python/2.7"
        for header in headers:
            print header[0] + ":", header[1]
    
    fileName = raw_input("Enter file name: ")
    print
    file = open(fileName)

    response = ''
    q = deque()
    for line in file:
        q.append(line)
    file.close()

    nl = queue.popleft()
    array = nl.split(" ")
    request_method = array[0]
    path_info_raw = array[1]
    server_protocol = array[2].strip("\n")
    
    #Get the query from the url_path
    path_list = path_info_raw.split("?")
    path_info = path_list[0]
    try:
        query_string = path_list[1]
        environ['QUERY_STRING'] = query_string
    except IndexError:
        pass
    
    environ['REQUEST_METHOD'] = request_method
    environ['PATH_INFO'] = path_info
    environ['SERVER_PROTOCOL'] = server_protocol
    
    while(True):
        try:
            new_line = queue.popleft().split(":")
            if new_line[0] == 'cookie':
                environ['HTTP_COOKIE'] = new_line[1]
        except IndexError:
            break
    

    data = app(environ, custom_start_response)
    print data
    
main()