from dao.genre import GenreDAO
from dao.model.genre import GenreSchema


class GenresService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, item_id):
        item_db = self.dao.get_one(item_id)
        item_serialized = GenreSchema().dump(item_db)
        return item_serialized

    def get_all(self):
        items_db = self.dao.get_all()
        items_serialized = GenreSchema(many=True).dump(items_db)
        return items_serialized

    def create(self, item_data):
        item_in_schema = GenreSchema().load(item_data)
        item_db = self.dao.create(item_in_schema)

    def update(self, new_data):
        self.dao.update(new_data)
        return self.dao

    # if genre_first is None:
    #     return "", 404

    def delete(self, item_id):
        self.dao.delete(item_id)

