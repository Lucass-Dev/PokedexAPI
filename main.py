import os

from flask import Flask, make_response, request

import pymongo

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_users():
    client = pymongo.MongoClient("mongodb+srv://poke1:passwordpoke1@clusterpokedex.irn89.mongodb.net/ApiDB?retryWrites=true&w=majority")
    db = client.ApiDB
    collection = db.Pokemon

    return make_response(str(collection.find_one({"Name": "Salamèche"})), 200)


@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json()
    data = body["fname"] + '\n' + body["lname"]
    file = open(f'users/{request.args["id"]}.txt', 'a')
    file.write(f'{data}')
    file.close()
    return make_response(body, 200)


@app.route('/users', methods=['PATCH'])
def change_user():
    body = request.get_json()
    data = body["fname"] + '\n' + body["lname"]
    file = open(f'users/{request.args["id"]}.txt', 'w')
    file.write(f'{data}')
    file.close()
    return make_response(body, 200)


@app.route('/users', methods=['DELETE'])
def delete_user():
    body = "User deleted!"
    os.remove(f'users/{request.args["id"]}.txt')
    return make_response(body, 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)