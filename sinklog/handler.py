from logging.handlers import SysLogHandler


__all__ = ('SinklogHandler',)


class SinklogHandler(SysLogHandler):

    DEFAULT_HOST = "sinklog.com"
    DEFAULT_PORT = 514

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('address', (self.DEFAULT_HOST, self.DEFAULT_PORT))
        self.logkey = kwargs.pop('logkey', None)
        super(SinklogHandler, self).__init__(*args, **kwargs)

    def format(self, record):
        record = super(SinklogHandler, self).format(record)
        return "{}: {}".format(self.logkey, record)

    def handle(self, record):
        if not self.logkey:
            import logging
            logging.getLogger().warn(
                "SinklogHandler called without a logkey.  Messages are ignored.")
            return False

        return super(SinklogHandler, self).handle(record)