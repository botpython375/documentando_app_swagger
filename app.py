from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def home():
    return jsonify({"message": "API está funcionando"})

@app.route('/items/<int:item_id>')
def get_item(item_id):
    q = request.args.get('q')
    return jsonify({"item_id": item_id, "q": q})
