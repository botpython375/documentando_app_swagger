from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "chave-super-secreta"

swagger = Swagger(app)
jwt = JWTManager(app)


@app.route("/")
def home():
    """
    Página inicial
    ---
    responses:
      200:
        description: Retorna status da API
        schema:
          type: object
          properties:
            message:
              type: string
    """
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


@app.route("/login", methods=["POST"])
def login():
    """
    Login do usuário
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - senha
          properties:
            email:
              type: string
            senha:
              type: string
    responses:
      200:
        description: Token JWT gerado
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Credenciais inválidas
    """
    data = request.get_json()
    if data.get("email") == "user@example.com" and data.get("senha") == "1234":
        token = create_access_token(identity=data["email"])
        return jsonify(access_token=token)
    return jsonify({"msg": "Credenciais inválidas"}), 401


@app.route("/protegido")
@jwt_required()
def protegido():
    """
    Rota protegida com JWT
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: Acesso autorizado
        schema:
          type: object
          properties:
            msg:
              type: string
      401:
        description: Token ausente ou inválido
    """
    user = get_jwt_identity()
    return jsonify({"msg": f"Olá, {user}!"})
