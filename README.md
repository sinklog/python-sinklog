# sinklog-handler
Logging handler for Sinklog.com

## Usage
Obtain a log key from https://sinklog.com/

### Python
Any Python script or app:

```python
import logging
from sinklog_handler import SinklogHandler

sinklog = SinklogHandler(logkey="<log key>")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(sinklog)

# Just use the logger as you would normally and log
# messages will be forwarded to your sinklog stream.
logger.info("Hello Sinklog!")
```

### Django
Add `SinklogHandler` to your Django logging config:

```python
'handlers': {
    'sinklog': {
        'level': "DEBUG",
        'class': "sinklog_handler.SinklogHandler",
        'logkey': "<log key>"
    }
},
'loggers': {
    'django.db.backends': {
        'level': 'ERROR',
        'handlers': ['sinklog'],
        'propagate': False
    }
}
```

### Flask
Add `SinklogHandler` to Flask's root app logger:

```python
from sinklog_handler import SinklogHandler

sinklog = SinklogHandler(logkey="<log key>")
app.logger.addHandler(sinklog)
```