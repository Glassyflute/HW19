from flask_restx import Resource, Namespace
from flask import request, abort
from models import User, UserSchema
from setup_db import db
from utils import get_hash, generate_tokens, decode_token

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = db.session.query(User).all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None in [username, password]:
            abort(400)

        # заменяем пароль в словаре по пользователю на хэш пароля.
        req_json["password"] = get_hash(password)

        user_ = UserSchema().load(req_json)
        new_user = User(**user_)
        with db.session.begin():
            db.session.add(new_user)
        return "", 201
        # ставим при проверке закрывающий слэш в Postman


@user_ns.route('/auth/')
class UsersView(Resource):
    def post(self):
        req_json = request.json

        # проверяем, что оба поля (логин-пароль) не пустые.
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None in [username, password]:
            abort(400)

        # проверяем, что пользователь существует в Базе.
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        # получаем хэш пароля пользователя.
        req_json["password"] = get_hash(password)
        password_hash = req_json["password"]

        # проверяем, что хэши пароля пользователя из базы и при авторизации совпадают.
        if password_hash != user.password:
            return {"error": "Неверные учётные данные"}, 401

        # генерируем токены.
        data = {
            "username": user.username,
            "role": user.role
        }

        return generate_tokens(data), 201


@user_ns.route('/<int:user_id>')
class UserView(Resource):
    def get(self, user_id):
        r = db.session.query(User).get(user_id)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def put(self, user_id):
        user_selected = db.session.query(User).filter(User.id == user_id)
        user_first = user_selected.first()

        if user_first is None:
            return "", 404

        req_json = request.json

        if "password" in req_json:
            # заменяем пароль в словаре по пользователю на хэш пароля.
            req_json["password"] = get_hash(req_json["password"])

        user_selected.update(req_json)
        db.session.commit()
        return "", 204

    def delete(self, user_id):
        user_selected = db.session.query(User).filter(User.id == user_id)
        user_first = user_selected.first()

        if user_first is None:
            return "", 404

        rows_deleted = user_selected.delete()
        # если произошло удаление более 1 строки, то указываем на наличие проблемы.
        if rows_deleted != 1:
            return "", 400

        db.session.commit()
        return "", 204


@user_ns.route('/auth/')
class UserView(Resource):
    def put(self):
        req_json = request.json

        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        decoded_token = decode_token(refresh_token)

        username = decoded_token["username"]
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        data = {
            "username": user.username,
            "role": user.role
        }

        return generate_tokens(data), 201
