from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from . import WebsiteAccessPoint
from flask_login import login_user, logout_user
from sqlalchemy import and_

access_point = Blueprint('access_point', __name__)

website = WebsiteAccessPoint()


@website.login_manager.user_loader
def load_user(user_id):
    return website.User.query.get(int(user_id))


@access_point.route('/login', methods=['POST'])
def login():
    request_json = request.get_json(force=True)
    email = request_json['email']
    password = request_json['password']
    user = website.User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            if login_user(user, remember=True):
                response = make_response(jsonify(result=True, id=user.id, first_name=user.first_name, last_name=user.last_name))
            else:
                response = make_response(jsonify(result=False, id=None))
        else:
            response = make_response(jsonify(result=False, id=None))
    else:
        response = make_response(jsonify(result=False, id=None))
    response.headers["Content-Type"] = "application/json"
    return response


@access_point.route('/logout', methods=['POST'])
def logout():
    res = logout_user()
    if res:
        response = make_response(jsonify(result=True))
    else:
        response = make_response(jsonify(result=False))
    response.headers["Content-Type"] = "application/json"
    return response


@access_point.route('/sign_up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        input_json = request.get_json(force=True)
        email = input_json['email']
        login = input_json['login']
        first_name = input_json['first_name']
        last_name = input_json['last_name']
        password = input_json['password']

        user_by_email = website.User.query.filter_by(email=email).first()
        user_by_login = website.User.query.filter_by(login=login).first()
        if user_by_email or user_by_login:
            response = make_response(jsonify(result=False, response='User already exists.'))
        else:
            new_user = website.User(email=email, login=login, first_name=first_name, last_name=last_name,
                                    password=generate_password_hash(password, method='sha256'))
            website.db.session.add(new_user)
            website.db.session.commit()
            login_user(new_user, remember=True)
            response = make_response(jsonify(result=True, user_id=new_user.get_id(), first_name=new_user.first_name, last_name=new_user.last_name))
        response.headers["Content-Type"] = "application/json"
        return response


@access_point.route('/load_user', methods=['POST'])
def load_user():
    if request.method == 'POST':
        input_json = request.get_json(force=True)
        user = website.User.query.get(int(input_json['id']))
        response = make_response(jsonify(user=user))
        response.headers["Content-Type"] = "application/json"
        return response


@access_point.route('/get-rooms', methods=['POST'])
def return_rooms():
    if request.method == 'POST':
        input_json = request.get_json(force=True)
        number_of_beds = input_json['no_of_beds'] if input_json['no_of_beds'] else 0
        price = input_json['price'] if input_json['price'] else 9999999
        rating_min = input_json['min_rating'] if input_json['min_rating'] else 0
        rating_max = input_json['max_rating'] if input_json['max_rating'] else 10
        city = input_json['city']
        rooms = website.Room.query.filter(and_(website.Room.city == city,
                                               website.Room.rating >= rating_min,
                                               website.Room.rating <= rating_max,
                                               website.Room.price <= price,
                                               # website.Room.additionals.in_(additionals),
                                               website.Room.number_of_beds >= number_of_beds)).all()
        res_table = []
        for room in rooms:
            res_table.append(room.return_table())

        response = make_response(jsonify(res=res_table))
        response.headers["Content-Type"] = "application/json"
        return response
