"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Aider, Organization, Aid, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('FLASK_APP_KEY')
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/signup", methods=["POST"])
def handle_login():

    if request.method == "POST":
        body = request.json
        new_user = User.create(body)
        if new_user is not None:
            return jsonify(new_user.serialize()), 201
        else:
            return jsonify({"message": "Email already in use"}), 401

    return jsonify({"message": "User not created"}), 405


@app.route('/signin', methods=['POST']) # Endpoint de autenticacion, retorna token.
def handle_signin():
    email=request.json.get("email", None)
    password=request.json.get("password", None)
    user = User.query.filter_by(email=email, password=password).one_or_none()
    user_serialize=user.serialize()
    #user.serialize()
    if user is not None:
        token = create_access_token(identity = user.id)
        return jsonify({
            "token": token,
            "user_id": user.id,
            "email": user.email, "user_type": user.user_type.value,
            "organization_name": user_serialize["organization_name"],
            "full_name": user_serialize["full_name"]
            }), 200
    else:
        return jsonify({"message": "Bad credentials"}), 401


#Ruta que trae todas las organizaciones
@app.route('/organizations', methods=['GET'])
def handle_organizations():
    all_organizations = Organization.query.all()
    all_serialize = []
    for organization in all_organizations:
        all_serialize.append(organization.serialize())
    response_body = {
        'status': 'ok',
        'results': all_serialize
    }
    return (response_body) , 200

#Ruta que trae todos los Aiders
@app.route('/aiders', methods=['GET'])
def handle_aiders():
    all_aiders = Aider.query.all()
    all_serialize = []
    for aider in all_aiders:
        all_serialize.append(aider.serialize())
    response_body = {
        'status': 'ok',
        'results': all_serialize
    }
    return (response_body) , 200


@app.route("/orgprofile", methods=["POST", "PUT"])
@jwt_required()
def handle_orgprofile():
    user_id = get_jwt_identity()
    if request.method == "POST":
        body = request.json
        body.update(user_info= user_id)
        orgprofile = Organization.create(body)

        if orgprofile is not None:
            return jsonify(orgprofile.serialize()), 201
                
        else:
            return jsonify({"message": "Please, fill all the fields"}), 401

    if request.method == "PUT":
        old_organization= Organization.query.filter_by(user_info=user_id).one_or_none()
        new_organization= old_organization.put(request.json)
        if new_organization:
           return jsonify(old_organization.serialize()), 200
        else:
            return jsonify("try again"), 500  

      


@app.route('/delprofile', methods= ['DELETE'])
@jwt_required()
def handleDeleteAccount():
    user = User.query.filter_by(id=get_jwt_identity()).one_or_none()
    user_to_delete = user.delete()
    if user_to_delete:
        return jsonify({"message": "Your org account was deleted"}) ,204
    else: 
        return jsonify({"message": "oh, oh"}), 400

    # if request.method == "PUT":
    #     body = request.json
    #     body.update(user_info= user_id)
    #     print(body)
    #     orgprofile = Organization.create(body)

    #     if orgprofile is not None:
    #         return jsonify(orgprofile.serialize()), 201
                
    #     else:
    #         return jsonify({"message": "Please, fill all the fields"}), 401

    # return jsonify({"message": "User not created"}), 405
    

@app.route("/aiderprofile", methods=["POST", "PUT"])
@jwt_required()
def handle_aiderprofile():
    user_id = get_jwt_identity()
    if request.method == "POST":
        body = request.json
        body.update(user_info= user_id)
        print(body)
        aiderprofile = Aider.create(body)

        if aiderprofile is not None:
            return jsonify(aiderprofile.serialize()), 201
                
        else:
            return jsonify({"message": "Please, fill all the fields"}), 401

    if request.method == "PUT":
        old_aider= Aider.query.filter_by(user_info=user_id).one_or_none()
        new_aider= old_aider.put(request.json)
        if new_aider:
            return jsonify(old_aider.serialize()), 200
        else:
             return jsonify("try again"), 500  


#Endpoint que trae las organizaciones por tipo
@app.route('/organizations/<string:organization_type>', methods=['GET'])
def handle_organization(organization_type):
    if organization_type == "children":
        children_organizations = Organization.query.filter_by(organization_type = organization_type).all()
        children_serialize = []
        for children_organization in children_organizations:
            children_serialize.append(children_organization.serialize())
        response_body = {
            'status': 'ok',
            'results': children_serialize
        }
    elif organization_type == "elderly":
        elderly_organizations = Organization.query.filter_by(organization_type = organization_type).all()
        elderly_serialize = []
        for elderly_organization in elderly_organizations:
            elderly_serialize.append(elderly_organization.serialize())
        response_body = {
            'status': 'ok',
            'results': elderly_serialize
        }
    else:
        others_organizations = Organization.query.filter_by(organization_type = organization_type).all()
        others_serialize = []
        for others_organization in others_organizations:
            others_serialize.append(others_organization.serialize())
        response_body = {
            'status': 'ok',
            'results': others_serialize
        } 
    return (response_body) , 200



@app.route('/organizations/<int:organization_id>', methods=['GET'])
def org_by_id(organization_id):
    one_org=[]
    one_org.append(Organization.query.filter_by(id=organization_id).first().serialize())
    response_body={
        'results': one_org
    }
    return (response_body) , 200



@app.route('/colaboracion', methods=['PUT', 'GET'])
def colab():
    return 'Menu de colaboraciones'

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
