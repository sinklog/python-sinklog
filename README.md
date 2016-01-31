# Python Sinklog
Logging handler and CLI for Sinklog.com

## Install
```bash
$ pip install python-sinklog
```

## Usage
Obtain a log key from https://sinklog.com/

### CLI
```bash
usage: sinklog [-h] --key KEY [--host HOST] [--port PORT] [--format FORMAT]
               [--level {WARN,INFO,DEBUG,ERROR}] [--tee]
               [message]

A simple logger for sinklog.com

positional arguments:
  message               messages to log

optional arguments:
  -h, --help            show this help message and exit
  --key KEY, -k KEY     Sinklog.com log key
  --host HOST, -H HOST  Sinklog host
  --port PORT, -P PORT  Sinklog port
  --format FORMAT, -F FORMAT
                        Python log format
  --level {WARN,INFO,DEBUG,ERROR}, -l {WARN,INFO,DEBUG,ERROR}
                        Python log level
  --tee, -t             when reading from stdin, copy to stdout

    example usage:

    # log a message on the command line
    $ sinklog -k <log key> "my log message"

    # log from stdin
    $ tail -f /var/log/myapp.log | sinklog -k <log key>

    # usage in a pipeline
    $ tail -f /var/log/myapp.log | sinklog -k <log key> --tee | grep foo
```

### Python
Any Python script or app:

```python
import logging
from sinklog import SinklogHandler

sinklog = SinklogHandler(logkey="<log key>", transport="tls")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(sinklog)

# Just use the logger as you would normally and log
# messages will be forwarded to your Sinklog stream.
logger.info("Hello Sinklog!")
```

### Django
Add `SinklogHandler` to your Django logging config:

```python
'handlers': {
    'sinklog': {
        'level': "DEBUG",
        'class': "sinklog.SinklogHandler",
        'logkey': "<log key>",
        'transport': "tls"
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
from sinklog import SinklogHandler

sinklog = SinklogHandler(logkey="<log key>", transport="tcp")
app.logger.addHandler(sinklog)
```