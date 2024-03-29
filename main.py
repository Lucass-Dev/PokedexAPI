import os
import re
import copy
import datetime
import werkzeug
import pymongo
import json
from bson.objectid import ObjectId
from werkzeug.exceptions import HTTPException
from flask import Flask, make_response, request, json

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://poke1:passwordpoke1@clusterpokedex.irn89.mongodb.net/ApiDB?retryWrites"
                             "=true&w=majority")
db = client.ApiDB
collection = db.Pokemon

@app.route('/')
def home():
    return '<h1>This is our home page</h1>'


@app.route('/get_all', methods=['GET'])
def get_all_pokemon():
    """
    Calling our database to get all pokemons inside the collection.
    :return: a list that contains all pokemons
    """
    test = []
    body = ""
    if request.args["sortBy"] == "name":
        for x in collection.find().sort("Name"):
            test.append(x)
            body = f'{body}\n\n{x["_id"]} \n {x["Name"]} \n {x["Type"]} \n {x["Stat"]} \n {x["Date"]} \n {x["Description"]}'
    elif request.args["sortBy"] == "vie":
        for x in collection.find().sort("Stat.Vie"):
            test.append(x)
            body = f'{body}\n\n{x["_id"]} \n {x["Name"]} \n {x["Type"]} \n {x["Stat"]} \n {x["Date"]} \n {x["Description"]}'
    elif request.args["sortBy"] == "atk":
        for x in collection.find().sort("Stat.ATK"):
            test.append(x)
            body = f'{body}\n\n{x["_id"]} \n {x["Name"]} \n {x["Type"]} \n {x["Stat"]} \n {x["Date"]} \n {x["Description"]}'
    elif request.args["sortBy"] == "def":
        for x in collection.find().sort("Stat.DEF"):
            test.append(x)
            body = f'{body}\n\n{x["_id"]} \n {x["Name"]} \n {x["Type"]} \n {x["Stat"]} \n {x["Date"]} \n {x["Description"]}'
    elif request.args["sortBy"] == "vitesse":
        for x in collection.find().sort("Stat.Vitesse"):
            test.append(x)
            body = f'{body}\n\n{x["_id"]} \n {x["Name"]} \n {x["Type"]} \n {x["Stat"]} \n {x["Date"]} \n {x["Description"]}'
    elif request.args["sortBy"] == "":
        for x in collection.find():
            test.append(x)
            body = f'{body}\n\n{x["_id"]} \n {x["Name"]} \n {x["Type"]} \n {x["Stat"]} \n {x["Date"]} \n {x["Description"]}'
    return make_response(body, 200)


@app.route('/get_by_type', methods=['GET'])
def get_pokemon_by_type():
    """
    Calling our database to get all pokemons that matches with the given argument
    :return: a list that contains all pokemons
    """
    test = []
    body = ""
    for x in collection.find({"Type": {'$regex': re.compile(request.args["type"], re.IGNORECASE)}}).sort('Name'):
        test.append(x)
        body = f'{body}\n\n{x["_id"]} \n {x["Name"]} \n {x["Type"]} \n {x["Stat"]} \n {x["Date"]} \n {x["Description"]}'
    if body == "":
        body = "No pokemon found with that name"
    return make_response(body, 200)


@app.route('/get_by_name', methods=['GET'])
def get_pokemon_by_name():
    """
    Calling our database to get all pokemons that matches with the given argument
    :return: a list that contains all pokemons
    """
    test = []
    body = ""
    for x in collection.find({"Name": {'$regex': re.compile(request.args["name"], re.IGNORECASE)}}).sort('Name'):
        test.append(x)
        body = f'{body}\n\n{x["_id"]} \n {x["Name"]} \n {x["Type"]} \n {x["Stat"]} \n {x["Date"]} \n {x["Description"]}'
    if body == "":
        body = "No pokemon found with that name"
    return make_response(body, 200)


@app.route('/create_pokemon', methods=['POST'])
def create_pokemon():
    """
    Method to insert pokemon inside our database using JSON object.
    :return: The added pokemon
    """
    post = request.get_json()
    x = datetime.datetime.now()
    date = x.strftime("%d") + '/' + x.strftime("%m") + '/' + x.strftime("%Y") + ' > ' + x.strftime(
        "%H") + ':' + x.strftime("%M")
    post["Date"] = date
    test = copy.copy(post)
    collection.insert_one(test)
    body = "Pokemon created: " + post
    return make_response(body, 200)


@app.route('/change_pokemon', methods=['PATCH'])
def change_pokemon():
    """
    Method to edit a pokemon in the database using is name as argument to identify wich one to edit
    :return: the edited pokemon
    """
    post = request.get_json()
    x = datetime.datetime.now()
    date = x.strftime("%w") + '/' + x.strftime("%m") + '/' + x.strftime("%Y") + ' > ' + x.strftime(
        "%H") + ':' + x.strftime("%M")
    post["Date"] = date
    if collection.find_one({"Name": request.args["name"]}) == None:
        return f'No such pokemon with that name : {request.args["name"]}'
    collection.find_one_and_replace({"Name": request.args["name"]}, post)
    body = "Pokemon edited: " + post
    return make_response(body, 200)


@app.route('/delete_pokemon', methods=['DELETE'])
def delete_pokemon():
    """
    Method to delete a pokemon from our database, using his name as argument to identify wich one we have to delete
    :return: a sentence with the deleted pokemon's name
    """
    pok_ID = request.args["id"]
    body = "Pokemon deleted: " + f'{pok_ID}'
    collection.find_one_and_delete({"_id": ObjectId(pok_ID)})
    return make_response(body, 200)


@app.errorhandler(KeyError)
@app.errorhandler(TypeError)
@app.errorhandler(ValueError)
@app.errorhandler(Exception)
def basic_error(e):
    """
    basic method that return a message in case of error
    :param e: the current error
    :return: message in case of error
    """
    return "Erreur rencontrée: " + str(e)


@app.errorhandler(HTTPException)
def http_error(e):
    """
    method that return a message in case of error
    :param e: the current error
    :return: message in case of error
    """
    return 'Erreur rencontrée : ' + str(e)


@app.errorhandler(werkzeug.exceptions.BadRequestKeyError)
def req_key_error(e):
    """
    basic method that return a message in case of error
    :param e: the current error
    :return: message in case of error
    """
    return 'Il manque un argument : ' + str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
