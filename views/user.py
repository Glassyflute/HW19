from flask_restx import Resource, Namespace
from flask import request, abort
from container import user_service
from utils import userdata_temp, generate_tokens, decode_token

user_profile_ns = Namespace('user')

# user is able to:
# see the user profile data (via get)
# update non-required fields of profile (via patch)
# change user's password (via put)
# user is unable to access data on other users, only admin is able to get access to other users' data.

# чтобы все ссылки корректно работали, их нужно обернуть в декоратор, в котором мы будем проверять переданный токен???
@user_profile_ns.route('/')
class UsersView(Resource):
    # @userdata_temp
    def get(self):
        """
        показывает информацию из профиля пользователя
        """
        # new_data = request.json
        # user has provided username & password at login step, so data on username would allow identifying
        # row with data on user in database
        # decorator would check user's token data, which contains username as well

        new_data = request.json
        access_token = new_data.get("access_token")
        if access_token is None:
            abort(400)
        decoded_token = decode_token(access_token)
        print(f"Decoded token - {decoded_token}")

        return user_service.get_one_by_username(decoded_token), 200

    def patch(self):
        """
        изменяет информацию пользователя (имя, фамилия, любимый жанр)
        """
        new_data = request.json
        # unknown user here if only Role is submitted. updates if Username is submitted.
        user_db = user_service.get_one_by_username(new_data)
        print(f"user_db - {user_db}")

        # # field by field
        # if "name" in new_data:
        #     user_db["name"] = new_data.get("name")
        # if "surname" in new_data:
        #     user_db["surname"] = new_data.get("surname")
        # if "favorite_genre" in new_data:
        #     user_db["favorite_genre"] = new_data.get("favorite_genre")

        # general update === prohibit indicating Role as admin by user -default user to be changed by admin only.
        # or use above to allow updating only 3 non-required fields, password is updated separately.
        user_service.update_by_username(new_data)

        return "", 204


@user_profile_ns.route('/password')
class UsersView(Resource):
    def put(self):
        """
        обновляет пароль пользователя
        """
        new_data = request.json
        # получаем 2 хэша старого и нового паролей пользователя
        user_service.hash_old_new_passwords(new_data)
        print(f"new_data with passwords - {new_data}")

        user_db = user_service.get_one_by_username(new_data)
        print(f"user_db - {user_db}")
        password_db = user_db["password"]

        if new_data["password_old"] != password_db:
            return {"error": "Неверные учётные данные"}, 401

        new_hashed_password = new_data["password_new"]
        user_db["password"] = new_hashed_password

        data_to_update = {
            "username": user_db["username"],
            "password": user_db["password"]
        }

        user_service.update_by_username(data_to_update)

        # генерируем токены.
        data = {
            "username": user_db["username"],
            "role": user_db["role"]
        }

        print(data)
        return generate_tokens(data), 201






