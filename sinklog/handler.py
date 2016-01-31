import logging
from logging.handlers import SysLogHandler
import socket
import ssl


__all__ = ('SinklogHandler',)


class SinklogHandler(SysLogHandler):

    DEFAULT_HOST = "sinklog.com"
    DEFAULT_PORT = 514
    TLS_PORT = 6514

    TRANSPORT_MAP = {
        'udp': socket.SOCK_DGRAM,
        'tcp': socket.SOCK_STREAM,
        'tls': socket.SOCK_STREAM
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('address', (self.DEFAULT_HOST, self.DEFAULT_PORT))
        self.logkey = kwargs.pop('logkey', None)

        transport = kwargs.pop('transport', 'udp')
        kwargs.setdefault('socktype', self.TRANSPORT_MAP[transport])
        super(SinklogHandler, self).__init__(*args, **kwargs)

        if transport == 'tls':
            self._setuptls()

    def _setuptls(self):
        # need to replace with an SSL socket
        host, _ = self.address
        self.socket.close()
        self.socket = ssl.wrap_socket(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM), cert_reqs=ssl.CERT_NONE)
        self.socket.connect((host, self.TLS_PORT))

    def format(self, record):
        record = super(SinklogHandler, self).format(record)
        return "{}: {}".format(self.logkey, record)

    def handle(self, record):
        if not self.logkey:
            clsname = self.__class__.__name__
            logging.getLogger().warn(
                "{} called without a logkey.  Messages are ignored.".format(clsname))
            return False

        return super(SinklogHandler, self).handle(record)
