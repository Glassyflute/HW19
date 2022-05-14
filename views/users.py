from flask_restx import Resource, Namespace
from flask import request, abort
from container import user_service
from utils import auth_required, admin_required

user_ns = Namespace('users')


# all views can be accessed/modified by admin
# admin is able to:
# see all users data and data on single user (via get)
# add new users (via post)
# update user's profile (via put)
# delete user (via delete)

@user_ns.route('/')
class UsersView(Resource):
    @admin_required
    def get(self):
        return user_service.get_all(), 200

    @admin_required
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
    @admin_required
    def get(self, item_id):
        return user_service.get_one(item_id), 200

    @admin_required
    def put(self, item_id):
        new_data = request.json

        user_service.hash_password(new_data)
        new_data["id"] = item_id

        user_service.update(new_data)
        return "", 204

    @admin_required
    def delete(self, item_id):
        user_service.delete(item_id)
        return "", 204

