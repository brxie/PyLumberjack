# PyLumberjack
Lumberjack protocol implementation for Python



#### About protocol
Protocol details is available [here](https://github.com/elastic/logstash-forwarder/blob/master/PROTOCOL.md)

#### Usage

```python
import Lumberjack

lumberjack = Lumberjack.Client(address = '146.185.185.187',
                            port = 8662,
                            sslCert = '/certs/host.crt'
                            )
lumberjack.connect()
lumberjack.write({"line":"hello"})
```

#### License
PyLumberjack is licensed under the Apache License 2.0.