import time
import json
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import logging

logging.basicConfig(format='%(asctime)-15s %(threadName)s %(message)s',
                    level=logging.INFO)
log = logging.getLogger()


class BadHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        log.info("Servicing request %s", self.path)
        if self.path == '/busted':
            self.server.busted = not self.server.busted
        self.server.req_count += 1
        if self.server.busted and \
           self.server.req_count % (200 + random.randint(-50, 50)) == 0:
            print("*** OH SHIT ITS BUSTED!***")
            time.sleep(24*60*60)
        time.sleep(0.2)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(bytes(
            json.dumps({'busted': self.server.busted,
                        'count': self.server.req_count}), 'utf-8'))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.req_count = 0
        self.busted = False
        self.daemon_threads = True

server = ThreadedHTTPServer(('localhost', 9999), BadHandler)
server.serve_forever()

