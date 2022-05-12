from flask_restx import Resource, Namespace
from flask import request
# from models import Genre, GenreSchema
# from setup_db import db
# from utils import auth_required, admin_required

from container import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    # @auth_required
    def get(self):
        return genre_service.get_all(), 200

    # @admin_required
    def post(self):
        new_data = request.json
        genre_service.create(new_data)

        # genre_ = GenreSchema().load(new_data)
        # new_genre = Genre(**genre_)
        # with db.session.begin():
        #     db.session.add(new_genre)

        return "", 201


# item_id
@genre_ns.route('/<int:item_id>')
class GenreView(Resource):
    # @auth_required
    def get(self, item_id):
        return genre_service.get_one(item_id), 200

    # @admin_required ==== БД не обновляется, но ошибки нет
    def put(self, item_id):
        new_data = request.json
        new_data["id"] = item_id

        genre_service.update(new_data)

        # genre_selected = db.session.query(Genre).filter(Genre.id == gid)
        # genre_first = genre_selected.first()
        #
        # if genre_first is None:
        #     return "", 404
        #
        # genre_selected.update(new_data)
        # db.session.commit()

        return "", 204

    # @admin_required
    def delete(self, item_id):
        genre_service.delete(item_id)

        # genre_selected = db.session.query(Genre).filter(Genre.id == gid)
        # genre_first = genre_selected.first()
        #
        # if genre_first is None:
        #     return "", 404
        #
        # rows_deleted = genre_selected.delete()
        # # если произошло удаление более 1 строки, то указываем на наличие проблемы.
        # if rows_deleted != 1:
        #     return "", 400
        #
        # db.session.commit()
        return "", 204

