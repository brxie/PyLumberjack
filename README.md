[![Build Status](https://travis-ci.org/Marcin1700/PyLumberjack.svg?branch=master)](https://travis-ci.org/Marcin1700/PyLumberjack)

# PyLumberjack
Lumberjack protocol implementation for Python



#### About protocol
Protocol details is available [here](https://github.com/elastic/logstash-forwarder/blob/master/PROTOCOL.md)

#### Usage

```python
import Lumberjack

lumberjack = Lumberjack.Client(address = '127.0.0.1',
                            port = 8662,
                            sslCert = '/certs/host.crt'
                            )
lumberjack.connect()
lumberjack.write({"line":"hello"})
```

#### License
PyLumberjack is licensed under the Apache License 2.0.
