import json
import base64
from uuid import uuid4
from urllib.parse import urlunparse

class ForwardAuth:
    server = None
    host = None
    method = None
    protocol = None
    port = None
    uri = None
    url = None
    token = None

    def __init__(self, **kw):
        pass

    def load(self, enum):
        for item in enum:
            self.__dict__[item] = enum[item]

    def generate_url(self):
        if (self.protocol == 'https') & (self.port == '443'):
            self.url = '%s://%s%s' % (str(self.protocol), str(self.host), str(self.uri))
        elif (self.protocol == 'http') & (self.port == '80'):
            self.url = '%s://%s%s' % (str(self.protocol), str(self.host), str(self.uri))
        else:
            self.url = '%s://%s:%s%s' % (self.protocol, self.host, self.port, self.uri)
        return self.url

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toUrl(self):
        return base64.urlsafe_b64encode(self.toJson().encode('utf-8'))

    @classmethod
    def create_from_headers(cls, headers):
        fa = cls()
        fa.token = str(uuid4())
        fa.server = headers['X-Forwarded-Server']
        if headers.has_key('X-Forwarded-Host'):
            fa.host = headers['X-Forwarded-Host']
        if headers.has_key('X-Forwarded-Method'):
            fa.method = headers['X-Forwarded-Method']
        if headers.has_key('X-Forwarded-Proto'):
            fa.protocol = headers['X-Forwarded-Proto']
        if headers.has_key('X-Forwarded-Port'):
            fa.port = headers['X-Forwarded-Port']
        if headers.has_key('X-Forwarded-Uri'):
            fa.uri = headers['X-Forwarded-Uri']
        fa.generate_url()
        return fa

    @classmethod
    def create_from_url(cls, data):
        return ForwardAuth.create_from_json(base64.urlsafe_b64decode(data))

    @classmethod
    def create_from_json(cls, data):
        fa = cls()
        j = json.loads(data)
        fa.load(j)
        return fa
