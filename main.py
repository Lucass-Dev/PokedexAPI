import os

from werkzeug.exceptions import HTTPException
from flask import Flask, make_response, request, json

import pymongo

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_pokemon():
    client = pymongo.MongoClient("mongodb+srv://poke1:passwordpoke1@clusterpokedex.irn89.mongodb.net/ApiDB?retryWrites=true&w=majority")
    db = client.ApiDB
    collection = db.Pokemon

    test = []
    body = ""
    for x in collection.find():
        test.append(x)
        body = f'{body} {x["Name"], x["Type"], x["Stat"], x["Date"], x["Description"]}'

    return make_response(body, 200)


@app.route('/pokemon', methods=['POST'])
def create_pokemon():
    body = request.get_json()
    data = body["fname"] + '\n' + body["lname"]
    file = open(f'pokemon/{request.args["id"]}.txt', 'a')
    file.write(f'{data}')
    file.close()
    return make_response(body, 200)


@app.route('/pokemon', methods=['PATCH'])
def change_pokemon():
    body = request.get_json()
    data = body["fname"] + '\n' + body["lname"]
    file = open(f'pokemon/{request.args["id"]}.txt', 'w')
    file.write(f'{data}')
    file.close()
    return make_response(body, 200)


@app.route('/pokemon', methods=['DELETE'])
def delete_pokemon():
    body = "User deleted!"
    os.remove(f'pokemon/{request.args["id"]}.txt')
    return make_response(body, 200)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """
    Return a JSON object with error details.
    """
    response = e.get_response()
    response.data = json.dumps({
        "Code d'erreur": e.code,
        "Nom de l'erreur": e.name,
        "Description de l'erreur": e.description,
    })
    response.content_type = "application/json"
    return make_response(response, 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)