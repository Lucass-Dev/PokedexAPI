import os
import copy
import datetime

from werkzeug.exceptions import HTTPException
from flask import Flask, make_response, request, json

import pymongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://poke1:passwordpoke1@clusterpokedex.irn89.mongodb.net/ApiDB?retryWrites=true&w=majority")
db = client.ApiDB
collection = db.Pokemon

@app.route('/', methods=['GET'])
def get_pokemon():


    test = []
    body = ""
    for x in collection.find():
        test.append(x)
        body = f'{body} {x["Name"], x["Type"], x["Stat"], x["Date"], x["Description"]}'

    return make_response(body, 200)


@app.route('/pokemon', methods=['POST'])
def create_pokemon():
    post = request.get_json()
    x = datetime.datetime.now()
    date = x.strftime("%w") + '/' + x.strftime("%m") + '/' + x.strftime("%Y") + ' > ' + x.strftime(
        "%H") + ':' + x.strftime("%M")
    post["Date"] = date
    test = copy.copy(post)
    collection.insert_one(test)
    return make_response(post, 200)


@app.route('/pokemon', methods=['PATCH'])
def change_pokemon():
    post = request.get_json()
    x = datetime.datetime.now()
    date = x.strftime("%w") + '/' + x.strftime("%m") + '/' + x.strftime("%Y") + ' > ' + x.strftime(
        "%H") + ':' + x.strftime("%M")
    post["Date"] = date

    if collection.find_one({"Name": request.args["name"]}) == None:
        return f'No such pokemon with that name : {request.args["name"]}'

    collection.find_one_and_replace({"Name": request.args["name"]}, post)
    return make_response(post, 200)


@app.route('/pokemon', methods=['DELETE'])
def delete_pokemon():
    pok_name = request.args["name"]
    body = "User deleted: " + f'{pok_name}'
    collection.find_one_and_delete({"Name": pok_name})
    return make_response(body, 200)



@app.errorhandler(Exception)
def basic_error(e):
    return "Erreur rencontrée: " + str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)