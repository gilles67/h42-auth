import click
from uuid import uuid4
from tinydb import TinyDB, Query
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from h42auth import app, tydb, login

SO_USER = 1

class SecurityObject:
    uid = None
    tio = None
    __new = False
    def __init__(self,data=None):
        if data:
            self.load(data)
        else:
            self.__new = True
            self.uid = str(uuid4())

    def view(self):
        print(self.__dict__)

    def save(self):
        data = dict()
        data['uid'] = self.uid
        data['tio'] = self.tio
        if self.tio == SO_USER:
            data['username'] = self.username
            data['domain'] = self.domain
            data['password'] = self.password
        if self.__new:
            tydb.insert(data)
            self.__new = False
        else:
            q = Query()
            tydb.update(data,(q.uid == self.uid) & (q.tio == self.tio))

    def load(self, data):
        self.__new = False
        self.uid = data['uid']
        self.tio = data['tio']
        if self.tio == SO_USER:
            self.username = data['username']
            self.domain = data['domain']
            self.password = data['password']

class User(UserMixin, SecurityObject):
    username = None
    domain = None
    password = None

    def __init__(self,data=None):
        super(User, self).__init__(data)
        self.tio = SO_USER
        self.domain = app.config['SO_DOMAIN']

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha512', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.uid

    @classmethod
    def findUser(cls, id):
        q = Query()
        data = tydb.get((q.uid == id) & (q.tio == SO_USER))
        if data:
            return User(data)
        return None

    def findUserByName(name, domain=app.config['SO_DOMAIN']):
        q = Query()
        data = tydb.get((q.username == name) & (q.domain == domain) & (q.tio == SO_USER))
        if data:
            return User(data)
        return None

@login.user_loader
def load_user(id):
    return User.findUser(id)


@app.cli.command("create-user")
@click.argument("name")
def create_user(name):
    q = Query()
    user = User.findUserByName(name)
    if user:
        user.view()
    else:
        user = User()
        user.username = name
        user.set_password('linux');
        user.save()
        user.view()
