import pymongo
import bcrypt

class DB:
    def __init__(self, connection_string):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client['thewall']
        self.users = self.db['users']
        self.bricks = self.db['bricks']
        self.jwt = self.db['jwt_secret']
        self.salt = b'$2b$12$DxeJ487KzENHnyOlhvH4Xe'

    def add_data(self, username, password):
        hashed = bcrypt.hashpw(password.encode(), self.salt)
        try:
            u = self.users.find({"username":username, "password":hashed})[0]
            return False
        except IndexError:
            pass
        next_id = self.users.count_documents({}) + 1
        self.users.insert_one({"username":username, "password":hashed, "_id": next_id})
        return next_id

    def get_jwt_key(self):
        secrets = self.jwt.find()
        return secrets[0]['secret']

    def check_user(self, username, password):
        hashed = bcrypt.hashpw(password.encode(), self.salt)
        try:
            u = self.users.find({"username":username, "password":hashed})[0]
            return u['_id']
        except IndexError:
            return False

    def get_user_id(self, username):
        try:
            u = self.users.find({"username": username})[0]
            return u['_id']
        except IndexError:
            return False

    def createBrick(self, username, text):
        next_id = self.bricks.count_documents({"username": username})
        self.bricks.insert_one({"username": username, "brick_id": next_id, "text": text})

    def getBricks(self, username):
        bricks = []
        res = self.bricks.find({"username": username})
        for b in res:
            bricks.append(b)
        return bricks

    def clearBricks(self, args, kwargs):
        return self.db.command(*args, **kwargs)
