import socket
from log import log
import traceback
from utils import get_dir


class Server(object):

    def stop(self):
        self._socket.close()

    def start(self):
        log('Starting server')
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._local_addr = ('127.0.0.1', 5010)
        try:
            self._socket.bind(self._local_addr)
            self._socket.listen(1)
            log('Binding to 127.0.0.1:5010')
            while True:
                client_connection, client_address = self._socket.accept()
                request = client_connection.recv(9086).decode()
                if 'POST /initialize' in str(request):
                    with self.lock:
                        self.handle_initialize()
                if 'POST /revert' in str(request):
                    with self.lock:
                        self.handle_revert()
                with open('%s/index.html' % get_dir(), 'r') as html:
                    response = 'HTTP/1.0 200 OK\n\n%s' % html.read()
                    client_connection.sendall(response.encode())
                    client_connection.close()
        except Exception as e:
            log('Error %s' % str(e))
            log(traceback.format_exc())
