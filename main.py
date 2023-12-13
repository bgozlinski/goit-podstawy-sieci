import json
import mimetypes
import pathlib
import threading
import urllib.parse
import socket
import os
from datetime import datetime
from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler
)


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path in ['/', '/index']:
            self.send_html_file('front-init/index.html')
        elif pr_url.path == '/message':
            self.send_html_file('front-init/message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static_file()
            else:
                self.send_html_file('front-init/error.html', 404)

    def do_POST(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.handle_message(post_data)
            self.send_response(302)
            self.send_header('Location', '/index')
            self.end_headers()
        else:
            self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static_file(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()

        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def handle_message(self, post_data):
        message = urllib.parse.parse_qs(post_data.decode('utf-8'))
        username = message['username'][0]
        message_text = message['message'][0]
        data = json.dumps({"username": username, "message": message_text})
        self.send_to_udp_server(data)

    @staticmethod
    def send_to_udp_server(data):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(data.encode(), ('localhost', 5000))


def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('localhost', 5000))
        while True:
            data, addr = s.recvfrom(1024)
            message = json.loads(data.decode())
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            save_message(timestamp, message)


def save_message(timestamp, message):
    if not os.path.exists('storage'):
        os.makedirs('storage')
    data_file = 'storage/data.json'
    data = {}
    if os.path.isfile(data_file):
        with open(data_file, 'r') as file:
            data = json.load(file)
    data[timestamp] = message
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)


def run_servers():
    httpd = HTTPServer(('', 3000), HttpHandler)
    http_thread = threading.Thread(target=httpd.serve_forever)
    udp_thread = threading.Thread(target=udp_server)
    http_thread.daemon = True
    udp_thread.daemon = True

    http_thread.start()
    udp_thread.start()

    try:
        http_thread.join()
        udp_thread.join()
    except KeyboardInterrupt:
        print("Servers are shutting down")
        httpd.server_close()


if __name__ == '__main__':
    run_servers()
