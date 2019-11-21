import os

from http.server import BaseHTTPRequestHandler

from routes.main import routes

from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from response.waitHandler import WaitHandler
import asyncio


class Server(BaseHTTPRequestHandler):
    
    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]
        print("Nav to: ", self.path)
        if self.path == '/wait':
            print('executing wait hander')
            handler = WaitHandler()
            loop = asyncio.new_event_loop()
            task = loop.create_task(handler.wait())
            loop.run_until_complete(task)
        elif request_extension == "" or request_extension == ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()
        else:
            handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)