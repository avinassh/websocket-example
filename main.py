import random

import tornado.ioloop
import tornado.web
import tornado.websocket

server = None
sockect_connections = set()


def WSSendData(message):
    for ws in sockect_connections:
        ws.write_message(message)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        server.add_callback(WSSendData, str(random.randint(1, 10)))
        self.render('index.html')


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        global sockect_connections
        sockect_connections.add(self)
        print('WebSocket opened :)')

    def on_message(self, message):
        print('I received: ', message)

    def on_close(self):
        global sockect_connections
        sockect_connections.remove(self)
        print('WebSocket closed :/')


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/ws', WSHandler),
    ])


def main():
    global server
    app = make_app()
    app.listen(8888)
    server = tornado.ioloop.IOLoop.current()
    server.start()


if __name__ == "__main__":
    main()
