# coding: utf-8
import sys
import argparse
import asyncio

from aiohttp import web
import uvloop

_RESP_CACHE = {}

def abort(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def aiohttp_server(loop, addr):
    async def handle(request):
        payload_size = int(request.match_info.get('size', 1024))
        resp = _RESP_CACHE.get(payload_size)
        if resp is None:
            resp = b'X' * payload_size
            _RESP_CACHE[payload_size] = resp
        return web.Response(body=resp)

    app = web.Application(loop=loop)
    app.router.add_route('GET', '/{size}', handle)
    app.router.add_route('GET', '/', handle)
    handler = app.make_handler()
    server = loop.create_server(handler, *addr)
    return server

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='asyncio+aiohttp', action='store')
    parser.add_argument('--addr', default='127.0.0.1:8080', type=str)
    args = parser.parse_args()
    if args.type:
        parts = args.type.split('+')
        if len(parts) > 1:
            loop_type = parts[0]
            server_type = parts[1]
        else:
            server_type = args.type

        if server_type in {'aiohttp', 'httptools'}:
            if not loop_type:
                loop_type = 'asyncio'
        else:
            loop_type = None

        if loop_type not in {'asyncio', 'uvloop'}:
            abort('unrecognized loop type: {}'.format(loop_type))

        if server_type not in {'aiohttp', 'httptools'}:
            abort('unrecognized server type: {}'.format(server_type))

        if loop_type:
            loop = globals()[loop_type].new_event_loop()
        else:
            loop = None

        print('using {} loop: {!r}'.format(loop_type, loop))
        print('using {} HTTP server'.format(server_type))

    if loop:
        asyncio.set_event_loop(loop)
        loop.set_debug(False)

    unix = False
    if args.addr.startswith('file:'):
        unix = True
        addr = args.addr[5:]
    else:
        addr = args.addr.split(':')
        addr[1] = int(addr[1])
        addr = tuple(addr)

    server_factory = globals()['{}_server'.format(server_type)]

    print('serving on: {}'.format(addr))

    if loop:
        server = loop.run_until_complete(server_factory(loop, addr))
        try:
            loop.run_forever()
        finally:
            server.close()
            loop.close()
