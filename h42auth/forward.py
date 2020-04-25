import json
import base64
from datetime import datetime, timedelta
from uuid import uuid4
from urllib.parse import urlparse

from h42auth import app, mongo

class ForwardAuth:
    __user = None
    __new = False
    server = None
    host = None
    method = None
    protocol = None
    port = None
    uri = None
    url = None
    token = None
    user = None
    souid = None
    is_authenticated = False
    expires = None
    auth_expires = None

    def __init__(self, data=None):
        if data:
            self.load(data)
        else:
            self.__new = True
            self.token = str(uuid4())
            self.expires = datetime.utcnow() + timedelta(hours=2)
            self.auth_expires = datetime.utcnow() + timedelta(minutes=5)

    def generate_url(self):
        if (self.protocol == 'https') & (self.port == '443'):
            self.url = '%s://%s%s' % (str(self.protocol), str(self.host), str(self.uri))
        elif (self.protocol == 'http') & (self.port == '80'):
            self.url = '%s://%s%s' % (str(self.protocol), str(self.host), str(self.uri))
        else:
            self.url = '%s://%s:%s%s' % (self.protocol, self.host, self.port, self.uri)
        return self.url

    def set_user(self, user):
        self.is_authenticated = True
        self.__user = user
        self.user = user.username
        self.souid = user.uid
        self.auth_expires = datetime.utcnow() + timedelta(hours=2)

    def check_headers(self, headers):
        app.logger.info(str(headers))
        print (headers)
        if headers.has_key('X-Auth-Service') :
            self.url = 'https://{}/'.format(headers['X-Auth-Service'])
            self.host = headers['X-Auth-Service']
        elif headers.has_key('Referer'):
            url = urlparse(headers['Referer'])
            self.url = headers['Referer']
            if url.scheme:
                self.protocol = url.scheme
            if url.port:
                self.port = url.port
            if url.hostname:
                self.host = url.hostname
            if url.path:
                self.uri = url.path
            else:
                self.uri = "/"
        else:
            if headers.has_key('X-Forwarded-Host'):
                self.host = headers['X-Forwarded-Host']
            if headers.has_key('X-Forwarded-Proto'):
                self.protocol = headers['X-Forwarded-Proto']
            if headers.has_key('X-Forwarded-Port'):
                self.port = headers['X-Forwarded-Port']
            if headers.has_key('X-Forwarded-Uri'):
                self.uri = headers['X-Forwarded-Uri']
            else:
                self.uri = "/"
            self.generate_url()

        self.server = headers['X-Forwarded-Server']
        if headers.has_key('X-Forwarded-Method'):
            self.method = headers['X-Forwarded-Method']

    def save(self):
        data = dict()
        if self.__new:
            data['_id'] = self.token
            data['token'] = self.token
        data['server'] = self.server
        data['host'] = self.host
        data['method'] = self.method
        data['protocol'] = self.protocol
        data['port'] = self.port
        data['uri'] = self.uri
        data['url'] = self.url
        data['user'] = self.user
        data['is_authenticated'] = self.is_authenticated
        data['expires'] = self.expires
        data['auth_expires'] = self.auth_expires
        data['souid'] = self.souid
        if self.__new:
            mongo.cx.h42auth.forward_sessions.insert_one(data)
            self.__new = False
        else:
            mongo.cx.h42auth.forward_sessions.update_one({'_id': self.token},{'$set': data})

    def load(self, data):
        self.__new = False
        self.token  = data['token']
        self.server = data['server']
        self.host = data['host']
        self.method = data['method']
        self.protocol = data['protocol']
        self.port = data['port']
        self.uri = data['uri']
        self.url = data['url']
        self.user = data['user']
        self.is_authenticated = data['is_authenticated']
        self.expires = data['expires']
        if 'auth_expires' in data:
            self.auth_expires = data['auth_expires']
        else:
            self.auth_expires = self.expires
        self.souid = data['souid']

    def destroy(self):
        mongo.cx.h42auth.forward_sessions.delete_one({'_id':self.token})

    @classmethod
    def find_auth(cls, token):
        data = mongo.cx.h42auth.forward_sessions.find_one({'_id':token})
        if data:
            return ForwardAuth(data)
        return None

    @classmethod
    def user_logout(cls, user):
        mongo.cx.h42auth.forward_sessions.delete_many({'souid':user.uid})

    @classmethod
    def clean_session(cls):
        mongo.cx.h42auth.forward_sessions.delete_many({'expires':{'$lt':datetime.utcnow()}})
        mongo.cx.h42auth.forward_sessions.delete_many({'auth_expires':{'$lt':datetime.utcnow()}})

    @classmethod
    def terminate_session(cls, token):
        mongo.cx.h42auth.forward_sessions.delete_one({'_id':token})

    @classmethod
    def get_user_sessions(cls, user):
        fasess = mongo.cx.h42auth.forward_sessions.find({'souid':user.uid})
        if fasess:
            sessions = list()
            for sess in fasess:
                sessions.append(ForwardAuth(sess))
            return sessions
        return None
