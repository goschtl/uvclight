# -*- coding: utf-8 -*-

import uwsgi

from gevent import spawn, wait
from gevent.event import Event
from gevent.queue import Queue
from gevent.select import select
from gevent.monkey import patch_all

# gevent patching
patch_all()

from flask.ext.uwsgi_websocket import (
    GeventWebSocketClient, WebSocketMiddleware)


class WebSocketHub(WebSocketMiddleware):
    client = GeventWebSocketClient

    timeout = 60

    def __init__(self, routes):
        self.routes = routes
        self.workers = {}

    def broadcast(self, message):
        for uid, worker in self.workers.items():
            worker.send(message)

    def register_worker(self, worker):
        if not worker.id in self.workers:
            self.workers[worker.id] = worker

    def unregister_worker(self, worker):
        if worker.id in self.workers:
            del self.workers[worker.id]

    def create_worker(
            self, environ, fd, send_event, send_queue, recv_event, recv_queue):
        client = self.client(
            environ, fd, send_event, send_queue, recv_event,
            recv_queue, self.timeout)
        client.__hub__ = self
        self.register_worker(client)
        return client

    def __call__(self, app):
        def websockets_wrapper(environ, start_response):
            handler = self.routes.get(environ['PATH_INFO'])

            if not handler:
                return app(environ, start_response)

            # do handshake
            uwsgi.websocket_handshake(
                environ['HTTP_SEC_WEBSOCKET_KEY'],
                environ.get('HTTP_ORIGIN', ''))

            # setup events
            send_event = Event()
            send_queue = Queue(maxsize=1)

            recv_event = Event()
            recv_queue = Queue(maxsize=1)

            # create websocket client
            wfd = uwsgi.connection_fd()
            client = self.create_worker(
                environ, wfd, send_event, send_queue, recv_event, recv_queue)

            # spawn handler
            handler = spawn(handler, client)

            # spawn recv listener
            def listener(client):
                ready = select([client.fd], [], [], client.timeout)
                recv_event.set()
            listening = spawn(listener, client)

            while True:
                if not client.connected:
                    recv_queue.put(None)
                    listening.kill()
                    handler.join(client.timeout)
                    return ''

                # wait for event to draw our attention
                ready = wait([handler, send_event, recv_event], None, 1)

                # handle send events
                if send_event.is_set():
                    try:
                        uwsgi.websocket_send(send_queue.get())
                        send_event.clear()
                    except IOError:
                        client.connected = False

                # handle receive events
                elif recv_event.is_set():
                    recv_event.clear()
                    try:
                        recv_queue.put(uwsgi.websocket_recv_nb())
                        listening = spawn(listener, client)
                    except IOError:
                        client.close()
                        self.unregister_worker(client)

                # handler done, we're outta here
                elif handler.ready():
                    listening.kill()
                    return ''
        return websockets_wrapper
