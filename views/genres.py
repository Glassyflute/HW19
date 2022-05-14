from flask_restx import Resource, Namespace
from flask import request
from utils import auth_required, admin_required
from container import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        return genre_service.get_all(), 200

    @admin_required
    def post(self):
        new_data = request.json
        genre_service.create(new_data)
        return "", 201


# item_id
@genre_ns.route('/<int:item_id>')
class GenreView(Resource):
    @auth_required
    def get(self, item_id):
        return genre_service.get_one(item_id), 200

    @admin_required
    def put(self, item_id):
        new_data = request.json
        new_data["id"] = item_id

        genre_service.update(new_data)
        return "", 204

    @admin_required
    def delete(self, item_id):
        genre_service.delete(item_id)
        return "", 204

