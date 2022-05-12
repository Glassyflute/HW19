from dao.auth import AuthUserDAO
from dao.model.user import UserSchema
from utils import get_hash


# CRUD
class AuthUsersService:
    def __init__(self, dao: AuthUserDAO):
        self.dao = dao

    def get_one(self, item_id):
        item_db = self.dao.get_one(item_id)
        item_serialized = UserSchema().dump(item_db)
        return item_serialized

    def get_one_by_username(self, item_data):
        item_db = self.dao.get_one_by_username(item_data)
        item_serialized = UserSchema().dump(item_db)
        return item_serialized

    def get_all(self):
        items_db = self.dao.get_all()
        items_serialized = UserSchema(many=True).dump(items_db)
        return items_serialized

    def create(self, item_data):
        item_in_schema = UserSchema().load(item_data)
        item_db = self.dao.create(item_in_schema)

    def update(self, new_data):
        self.dao.update(new_data)
        return self.dao

    def delete(self, item_id):
        self.dao.delete(item_id)

    def hash_password(self, new_data):
        # заменяем пароль в словаре по пользователю на хэш пароля.
        if "password" in new_data:
            new_data["password"] = get_hash(new_data["password"])
            return new_data

