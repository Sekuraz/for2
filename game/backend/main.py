import json
import os

from flask import Flask, send_from_directory, request
from couchdb import Server, ResourceNotFound

app = Flask(__name__, static_folder='../frontend')
db_server = Server("http://admin:password@127.0.0.1:5984")

try:
    db = db_server["maze"]
except ResourceNotFound:
    db = db_server.create("maze")

# Serve Maze App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print(path)
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route("/upload", methods=["POST", "PUT"])
def upload():
    data = request.get_json()
    db.save(data)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
