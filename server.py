import socket
from log import log
import traceback
from main import lock


home_page = '''
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    Hello! <br />
    <p>
        Instructions: <br/><br/>
        1. Press Initialize,
        this will create audio tracks for each MIDI track and copy over all VSTs on the MIDI track that isn't an instrument to the audio track created for it.<br/> <br />
        2. Proceed to flatten and freeze these the MIDI tracks (Needs to be done manually as Ableton does not provide an API for it.) <br /><br/>
        3. Press Revert,
        this will copy over all the VSTs back to the MIDI tracks and delete the audio track.
    </p>
    <button id="init"> Initialize </button>
    <button id="revert" disabled> Revert </button>

    <script>
        init = document.getElementById('init')
        init.onclick = function () {
            init.setAttribute("disabled", "disabled");
            fetch('/initialize', {method: 'POST'}).then(() => {
            revert.removeAttribute("disabled");
            alert('Done Initializing');
            })
        }
        revert = document.getElementById('revert')
        revert.onclick = function () {
            revert.setAttribute("disabled", "disabled");
            fetch('/revert', {method: 'POST'}).then(() => alert('Done Reverting'))
        }
    </script>
  </body>
</html>
'''
class Server(object):
    def __init__(self, ctrl_surface):
        self._ctrl_surface = ctrl_surface

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
                # Wait for client connections
                client_connection, client_address = self._socket.accept()
                # Get the client request
                request = client_connection.recv(9086).decode()
                if 'POST /initialize' in str(request):
                    with lock:
                        self._ctrl_surface.handle_initialize()
                if 'POST /revert' in str(request):
                    with lock:
                        self._ctrl_surface.handle_revert()
                # Send HTTP response
                response = 'HTTP/1.0 200 OK\n\n%s' % home_page
                client_connection.sendall(response.encode())
                client_connection.close()
        except Exception as e:
            log('Error %s' % str(e))
            log(traceback.format_exc())
