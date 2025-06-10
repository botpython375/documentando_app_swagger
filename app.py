from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/")
def home():
    return jsonify({"message": "API está funcionando"})


@app.route("/items/<int:item_id>")
def get_item(item_id):
    """
    Obter item pelo ID
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID do item
      - name: q
        in: query
        type: string
        required: false
        description: Filtro opcional
    responses:
      200:
        description: Sucesso
        schema:
          type: object
          properties:
            item_id:
              type: integer
            q:
              type: string
    """
    q = request.args.get("q")
    return jsonify({"item_id": item_id, "q": q})
