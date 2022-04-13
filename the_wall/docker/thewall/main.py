import os
import time
import random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from flask import Flask, render_template, redirect, request, jsonify, make_response, escape
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from db import DB
from db_admin import DB_admin

app = Flask(__name__)
SERVER_PORT = os.getenv('SERVER_PORT', '8081')
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
MONGODB_STRING = os.getenv('MONGODB_STRING', 'mongodb://root:password@localhost:27017/?authMechanism=DEFAULT')
JWT_SECRET = b64encode(bytes([random.randint(0,255) for i in range(16)])).decode()


while True:
    try:
        database_admin = DB_admin(MONGODB_STRING, JWT_SECRET)
        break
    except:
        print('Mongo is not started yet. Wait for 2s and reconnect...')
        time.sleep(2)

db_user, db_pass = database_admin.create_low_user()
database = DB(f'mongodb://{db_user}:{db_pass}@mongo:27017/?authMechanism=DEFAULT&authSource=thewall')
app.config["JWT_SECRET_KEY"] = database.get_jwt_key()
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 10000
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
jwt = JWTManager(app)

secrets_folder = 'secrets/'

os.makedirs(secrets_folder, exist_ok=True)

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def create_key_if_not_exists(id_):
    if os.path.exists(secrets_folder+str(id_)):
        return
    bricks_key = b64encode(bytes([random.randint(0,255) for i in range(32)])).decode()
    with open(secrets_folder+str(id_), 'w') as f:
        f.write(bricks_key)

def read_key(path):
    key = None
    with open(path, 'r') as f:
        key = f.read()
    key = b64decode(key)
    return key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('login')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            return render_template('register.html', error='Passwords doesn\'t match')
        id_ = database.add_data(username, password1)
        if id_ == False:
            return render_template('register.html', error='User already exists')
        
        create_key_if_not_exists(id_)
        return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        id_ = database.check_user(username, password)
        if id_ == False:
            return render_template('login.html', error='Wrong username or password')
       
        create_key_if_not_exists(id_)
        add_claims = {'bricks_key_path':secrets_folder+str(id_)}
        token = create_access_token(username, additional_claims=add_claims)
        resp = make_response(redirect('/home'))
        set_access_cookies(resp, token)
        return resp
    else:
        return render_template('login.html')

@app.route('/home', methods=['GET'])
@jwt_required()
def home():
    username = get_jwt_identity()
    key = read_key(get_jwt()['bricks_key_path'])
    bricks = database.getBricks(username)

    for i in bricks:
        try:
            data = i['text'][16:]
            iv = i['text'][:16]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(data))
            i['text'] = str(escape(decrypted.decode()))
        except:
            i['text'] = 'error'

    html = ''
    for i in range(len(bricks)):
        if i % 7 < 4:
            if i % 7 == 0:
                html += '<button type="button" class="brick inline-block" style="width:10%"></button>'
            html += '<button type="button" class="brick inline-block">'+bricks[i]['text']+'</button>'
            if i % 7 == 3:
                html += '<button type="button" class="brick inline-block" style="width:10%"></button>'
        else:
            if i % 7 == 4:
                html += '<button type="button" class="brick inline-block"></button>'
            html += '<button type="button" class="brick inline-block">'+bricks[i]['text']+'</button>'
            if i % 7 == 6:
                html += '<button type="button" class="brick inline-block"></button>'
    if len(bricks) % 7 != 0:
        if len(bricks) % 7 < 4:
            c = len(bricks) % 7
            while c != 4:
                html += '<button type="button" class="brick inline-block"></button>'
                c += 1
            html += '<button type="button" class="brick inline-block" style="width:10%"></button>'
        else:
            c = len(bricks) % 7
            while c != 7:
                html += '<button type="button" class="brick inline-block"></button>'
                c += 1
            html += '<button type="button" class="brick inline-block"></button>'
    return render_template('home.html', username=username, bricks=html)

@app.route('/createBrick', methods=['POST'])
@jwt_required()
def createBrick():
    username = get_jwt_identity()
    key = read_key(get_jwt()['bricks_key_path'])
    text = request.json['text']

    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(text).encode())
    iv = cipher.iv
    ciphertext = iv + ciphertext

    database.createBrick(username, ciphertext)
    return jsonify()

def recurse_check_username(kwargs):
    for k in kwargs:
        if k == 'username':
            return True
        if type(k) in [str, int, float] and (type(kwargs[k]) == dict or type(kwargs[k]) == list):
            return recurse_check_username(kwargs[k])
        if type(k) == dict or type(k) == list:
            return recurse_check_username(k)
    return False

@app.route('/clearBricks', methods=['POST'])
@jwt_required()
def clear():
    username = get_jwt_identity()
    data = request.json
    args = data['args']
    kwargs = data['kwargs']
    #if not recurse_check_username(kwargs):
    #    return jsonify(db_response_length=0, error='username isn\'t specified'), 400
    response = None
    try:
        response = database.clearBricks(args, kwargs)
    except Exception as e:
        return jsonify(db_response_length=0, exception=str(e))
    return jsonify(db_response_length=len(str(response)))

if __name__ == '__main__':
    try:
        app.run(host=SERVER_HOST, port=int(SERVER_PORT), debug=False)
    except KeyboardInterrupt:
        os._exit(0)

