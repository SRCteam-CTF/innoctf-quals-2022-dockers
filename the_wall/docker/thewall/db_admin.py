import pymongo

class DB_admin:
    def __init__(self, connection_string, jwt_secret):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client['thewall']
        self.coll = self.db['jwt_secret']
        try:
            self.coll.find()[0]
        except IndexError:
            self.coll.insert_one({'secret': jwt_secret})

    def create_low_user(self):
        try:
            self.db.command("createRole", "lowUser", privileges=[
                {
                    "resource": {"db":"thewall", "collection":""}, "actions": ["find", "dbStats", "collStats"]
                }, {
                    "resource": {"db":"thewall", "collection":"jwt_secret"}, "actions": ["find"]
                }, {
                    "resource": {"db":"thewall", "collection":"users"}, "actions": ["find", "insert"]
                }, {
                    "resource": {"db":"thewall", "collection":"bricks"}, "actions": ["find", "insert"]
                }], roles=["read"])
        except pymongo.errors.OperationFailure as e:
            print(e)
        password = 'wgmrqsfcKQKjGIqxjPun2YyEi1J0zT2KMk0IXrAzMNM='
        username = 'low'
        try:
            self.db.command('createUser', username, pwd=password, roles=[{'role':'lowUser', 'db':'thewall'}])
        except pymongo.errors.OperationFailure as e:
            print(e)
        return username, password
