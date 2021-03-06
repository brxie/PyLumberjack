#!/usr/bin/env python
import sys
sys.path.append('./lib/')
import Lumberjack
from uuid import uuid4
from time import sleep
import requests
import json
import unittest



class Base(unittest.TestCase):

    def setUp(self):
        self.testWorkerHost = '192.81.223.90'
        self.client = Lumberjack.Client(port = 8662,
                                    address = self.testWorkerHost,
                                    sslCert = './tests/host.crt',
                                    )
        self.client.connect()
        self.testId = str(uuid4())
        self.feedData(messagesQty=2000)

    def feedData(self, messagesQty):
        for i in range(messagesQty):
            self.client.write({"line":"%s" % i, 'testId': self.testId})

    def test_verifyOutcome(self):
        sleep(10)
        resp = requests.get("http://%s:55555/%s.txt" % (self.testWorkerHost, self.testId) ).text
        messages = resp.strip().split('\n')
        for key, msg in enumerate(messages):
            try:
                msg = json.loads(msg)['message']
            except:
                pass
            self.assertEqual(msg, str(key))


unittest.main()
