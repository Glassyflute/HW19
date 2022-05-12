from flask_restx import Resource, Namespace
from flask import request, abort
from container import user_service
from utils import get_hash

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        return user_service.get_all(), 200

    def post(self):
        new_data = request.json

        username = new_data.get("username", None)
        password = new_data.get("password", None)
        if None in [username, password]:
            abort(400)

        # заменяем пароль в словаре по пользователю на хэш пароля.
        user_service.hash_password(new_data)

        user_service.create(new_data)
        return "", 201


@user_ns.route('/<int:item_id>')
class UserView(Resource):
    def get(self, item_id):
        return user_service.get_one(item_id), 200

    def put(self, item_id):
        new_data = request.json

        user_service.hash_password(new_data)
        new_data["id"] = item_id

        user_service.update(new_data)
        return "", 204

    def delete(self, item_id):
        user_service.delete(item_id)
        return "", 204

