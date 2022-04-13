from flask import *

from os import system
from time import time
import json

app = Flask(__name__)
users_db = json.loads(open("users_db.json", "r").read())


def username_by_id(id):
    for u in users_db:
        if u["id"] == id:
            return u["name"]


@app.route("/", methods=["GET", "POST"])
def download_file():
    if request.method == 'POST':
        print(request.data)
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/users")
def users():
    return render_template("users.html", users=users_db)


@app.route("/generate_qr", methods=["GET", "POST"])
def generate_qr():
    if request.method == 'POST':
        ids = request.get_json()
        cmd = ""
        for id in ids:
            cmd += f"qrencode -o uploads/{username_by_id(id)} {int(time())}-{id[:7]};\n"
        print(cmd, end="\n\n")
        system(cmd)
    return json.dumps({'success': True}), 200


@app.route("/get_qr")
def get_qr():
    uname = request.args.get("uname")
    with open("uploads/" + uname, "rb") as f:
        cnt = f.read()
    response = make_response(cnt)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'attachment', filename=uname)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
