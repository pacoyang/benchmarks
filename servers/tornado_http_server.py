# coding: utf-8
from tornado import ioloop, web, gen

_RESP_CACHE = {}

class MainHandler(web.RequestHandler):
    @gen.coroutine
    def get(self, size):
        if size:
            payload_size = int(size)
        else:
            payload_size = 1024
        resp = _RESP_CACHE.get(payload_size)
        if resp is None:
            resp = b'X' * payload_size
            _RESP_CACHE[payload_size] = resp
        self.write(resp)

def make_app():
    return web.Application([
        (r'/(.*)', MainHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    ioloop.IOLoop.current().start()
