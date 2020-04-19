import click
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from h42auth import app, mongo, login

class User(UserMixin):
    __new = False
    uid = None
    username = None
    domain = None
    password = None

    def __init__(self,data=None):
        if data:
            self.load(data)
        else:
            self.__new = True
            self.uid = str(uuid4())
            self.domain = app.config['SO_DOMAIN']

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha512', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.uid

    def view(self):
        print(self.__dict__)

    def save(self):
        data = dict()
        if self.__new:
            data['_id'] = self.uid
            data['uid'] = self.uid
        data['username'] = self.username
        data['domain'] = self.domain
        data['password'] = self.password
        if self.__new:
            mongo.cx.h42auth.users.insert_one(data)
            self.__new = False
        else:
            mongo.cx.h42auth.users.update_one({'_id': self.uid}, { "$set" : data})

    def load(self, data):
        self.__new = False
        self.uid = data['uid']
        self.username = data['username']
        self.domain = data['domain']
        self.password = data['password']

    @classmethod
    def findUser(cls, id):
        data = mongo.cx.h42auth.users.find_one({'_id': id})
        if data:
            return User(data)
        return None

    def findUserByName(name, domain=app.config['SO_DOMAIN']):
        data = mongo.cx.h42auth.users.find_one({'username': name, 'domain': domain })
        if data:
            return User(data)
        return None

@login.user_loader
def load_user(id):
    return User.findUser(id)


@app.cli.command("create-user")
@click.argument("name")
def create_user(name):
    user = User.findUserByName(name)
    if user:
        user.view()
    else:
        user = User()
        user.username = name
        user.set_password('linux');
        user.save()
        user.view()
