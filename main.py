from flask import Flask, make_response
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://poke1:passwordpoke1@clusterpokedex.irn89.mongodb.net/ApiDB?retryWrites=true&w=majority")
db = client.ApiDB
collection = db.Pokemon

@app.route('/')
def test():
    return make_response(str(collection.find_one({"Name": "Salamèche"})), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)