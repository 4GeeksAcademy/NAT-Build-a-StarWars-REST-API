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
from models import db, User
from models import Favorite
from models import Planets
from models import People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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
@app.route('/')
def sitemap():
    return generate_sitemap(app)


""" USERS """
@app.route('/user', methods=['GET'])
def users():
    user = User.query.all()
    user_list = []
    for item in user:
        user_list.append(item.serialize())
    return jsonify(user_list), 200

@app.route('/user/favorites/<int:theid>', methods=['GET'])
def get_user_favorites(theid=None):
    if theid is None:
        return jsonify({"Menssage":"User not found"}), 404

    favorites = Favorite.query.filter_by(user_id=theid).all()
    if favorites is None:
        return jsonify({"Menssage":"no hay favoritos"})
    favorites_list = []
    for item in favorites:
        favorites_list.append(item.serialize())
    return jsonify(favorites_list), 200

""" PLANETS   """  

@app.route('/planets', methods=['GET'])
def planets_list():
    planet = Planets.query.all()
    planet_list = []
    for item in planet:
        planet_list.append(item.serialize())
    return jsonify(planet_list), 200

@app.route('/planets/<int:theid>', methods=['GET'])
def planet_by_id(theid=None):
    planet = Planets.query.get(theid)
    if planet is None:
        return jsonify({"Menssage":"Planet no existe"}), 404
    else:
        return jsonify(planet.serialize()), 200
    
""" PEOPLE """

@app.route('/people', methods=['GET'])
def list_characters():
    people = People.query.all()
    people_list = []
    for item in people:
        people_list.append(item.serialize())
    return jsonify(people_list), 200

@app.route('/people/<int:theid>', methods=['GET'])
def characters_by_id(theid=None):
    people = People.query.get(theid)
    if people is None:
        return jsonify({"Menssage":"people no existe"}), 404
    
    return jsonify(people.serialize(), 200)

""" FAVORITES """

@app.route('/favorites/planets/<int:planets_id>/<int:user_id>', methods=['POST'])
def add_planets_favorites(planets_id, user_id): 
    favorite = Favorite.query.filter_by(planets_id = planets_id, user_id = user_id).first()

    user = User.query.get(user_id)

    if user is None:
        return jsonify({"Menssage":"User inexistente"})
    if favorite is not None:
        return jsonify({"Menssage":"This favorite already exist"})

    add_favorite = Favorite(user_id = user_id, planets_id = planets_id)
    db.session.add(add_favorite)
    

    try:
        db.session.commit()
        return jsonify({"Menssage":"favorite egregado"}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"Menssage":f"{error}"})
    
@app.route('/favorites/people/<int:people_id>/<int:user_id>', methods=['POST'])
def add_people_favorites(people_id, user_id):
    favorite = Favorite.query.filter_by(user_id = user_id, people_id = people_id).first()

    user = User.query.get(user_id)

    if user is None:
        return jsonify({"Menssage":"User not exist"})
    if favorite is not None:
        return jsonify({"Menssage":"favorite ya existe"})
    
    add_favorite = Favorite(user_id = user_id, people_id = people_id)
    db.session.add(add_favorite)

    try:
        db.session.commit()
        return jsonify({"Menssage":"Favorito agregado"})
    except Exception as error:
        db.session.rollback()
        return jsonify({"Menssage":f"{error}"}), 500

@app.route('/favorites/planets/<int:planets_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite(planets_id, user_id):
    favorite = Favorite.query.filter_by(user_id = user_id, planets_id = planets_id).first()

    if favorite is None:
        return jsonify({"Menssage":"Favorite no existe"}), 404
    try:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"Menssage":"favorito eliminado"}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({{error}}), 500
    
@app.route('/favorites/people/<int:people_id>/<int:user_id>', methods=['DELETE'])
def delete_people_favorite(people_id, user_id):
    favorite = Favorite.query.filter_by(user_id = user_id, people_id = people_id).first()

    if favorite is None:
        return jsonify({"Menssage":"Favorite no existe"}), 404
    try:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"Menssage":"This favorite eliminado"}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"Menssage":f"error"}, 500)
   




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
