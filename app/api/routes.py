from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Bike, bike_schema, bikes_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/data')
def getdata():
    return {'some': 'value'}

@api.route('/bikes', methods = ['POST'])
@token_required
def create_bike(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    max_speed = request.json['max_speed']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    bike = Bike(name,description,price, max_speed, user_token = user_token )

    db.session.add(bike)
    db.session.commit()

    response = bike_schema.dump(bike)
    return jsonify(response)


@api.route('/bikes', methods = ['GET'])
@token_required
def get_bike(current_user_token):
    a_bike = current_user_token.token
    bikes = Bike.query.filter_by(user_token = a_bike).all()
    response = bikes_schema.dump(bikes)
    return jsonify(response)


@api.route('/bikes/<id>', methods = ['GET'])
@token_required
def get_one_bike(current_user_token, id):
    bike = Bike.query.get(id)
    response = bike_schema.dump(bike)
    return jsonify(response)
  
 
@api.route('/bikes/<id>', methods = ['POST','PUT'])
@token_required
def update_bike(current_user_token,id):
    bike = Bike.query.get(id)
    bike.name = request.json['name']
    bike.description = request.json['description']
    bike.price = request.json['price']
    bike.max_speed = request.json['max_speed']
    bike.user_token = current_user_token.token

    db.session.commit()
    response = bike_schema.dump(bike)
    return jsonify(response)


@api.route('/bikes/<id>', methods = ['DELETE'])
@token_required
def delete_bike(current_user_token, id):
    bike = Bike.query.get(id)
    db.session.delete(bike)
    db.session.commit()
    response = bike_schema.dump(bike)
    return jsonify(response)