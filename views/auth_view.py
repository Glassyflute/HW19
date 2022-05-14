from flask_restx import Resource, Namespace
from flask import request, abort
from container import auth_user_service
from utils import get_hash, generate_tokens, decode_token

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        new_data = request.json

        # # проверяем, что оба поля (логин-пароль) не пустые.
        # username = req_json.get("username", None)
        # password = req_json.get("password", None)
        # if None in [username, password]:
        #     abort(400)
        #
        # # проверяем, что пользователь существует в Базе.
        # user = db.session.query(User).filter(User.username == username).first()
        # if user is None:
        #     return {"error": "Неверные учётные данные"}, 401

        # получаем хэш пароля пользователя.
        auth_user_service.hash_password(new_data)
        password_new_data = new_data.get("password")
        print(password_new_data)

        # получаем хэшированный пароль пользователя из БД.
        user_db = auth_user_service.get_one_by_username(new_data)
        print(user_db)
        password_db = user_db["password"]

        # проверяем, что хэши пароля пользователя из базы и при авторизации совпадают.
        if password_new_data != password_db:
            return {"error": "Неверные учётные данные"}, 401

        # генерируем токены.
        data = {
            "username": user_db["username"],
            "role": user_db["role"]
        }

        print(data)
        return generate_tokens(data), 201

    def put(self):
        new_data = request.json

        refresh_token = new_data.get("refresh_token")
        if refresh_token is None:
            abort(400)

        access_token = new_data.get("access_token")
        if access_token is None:
            abort(400)

        decoded_token = decode_token(refresh_token)
        print(f"Decoded token - {decoded_token}")

        user_db = auth_user_service.get_one_by_username(decoded_token)
        print(user_db)
        # username = decoded_token.get("username")
        # user = db.session.query(User).filter(User.username == username).first()
        # if user is None:
        #     return {"error": "Неверные учётные данные"}, 401

        data = {
            "username": user_db["username"],
            "role": user_db["role"]
        }
        print(data)
        return generate_tokens(data), 201


@auth_ns.route('/register')
class AuthView(Resource):
    def post(self):
        new_data = request.json

        auth_user_service.hash_password(new_data)
        auth_user_service.create(new_data)

        return "", 201

