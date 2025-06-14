import json
import os

from flask import Flask, send_from_directory, request, url_for
from couchdb import Server, ResourceNotFound

from data.data_classes import Maze

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
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route("/upload", methods=["POST", "PUT"])
def upload():
    data = request.get_json()
    for i in range(len(data["borders"])):
        if data["borders"][i:i+1] == "xx":
            print("error " + data["borders"])
    Maze.from_database(**data)
    db.save(data)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/development.js")
def development_variables():
    script = f"""
    r_reload = true;
    uploadUrl = "{url_for('upload')}";
    uploadEarly = true;
    autoreload = true;
    function settings_init() {{
        document.getElementById("mazeHeight").value = 5
        document.getElementById("mazeWidth").value = 5
    }}
    """
    return script
