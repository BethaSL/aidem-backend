"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/organizaciones')
def orgs():
  return 'Organizaciones'

@app.route('/organizaciones/<int:org_id>', methods=['PUT', 'GET'])
def org(id):
    return 'Organizacion org_name'

@app.route('/nosotros')
def nosotros():
    return 'Mision y Vision'

@app.route('/colaboracion', methods=['PUT', 'GET'])
def colab():
    return 'Menu de colaboraciones'

@app.route('/casashogar', methods=['GET'])
def casahogar():
    return 'Casas Hogares'

@app.route('/ancianatos', methods=['GET'])
def ancianato():
    return 'Ancianatos'

@app.route('/otras', methods=['GET'])
def otrasOrg():
    return 'Otras Organizaciones'

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
