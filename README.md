# PyLumberjack
Lumberjack protocol implementation for Python

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

#### About protocol
Protocol details is available [here](https://github.com/elastic/logstash-forwarder/blob/master/PROTOCOL.md)


#### License
PyLumberjack is licensed under the MIT Open Source license. http://opensource.org/licenses/MIT