from dao.director import DirectorDAO
from dao.model.director import DirectorSchema


class DirectorsService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, item_id):
        item_db = self.dao.get_one(item_id)
        item_serialized = DirectorSchema().dump(item_db)
        return item_serialized

    def get_all(self):
        items_db = self.dao.get_all()
        items_serialized = DirectorSchema(many=True).dump(items_db)
        return items_serialized

    def create(self, item_data):
        item_in_schema = DirectorSchema().load(item_data)
        item_db = self.dao.create(item_in_schema)

    def update(self, new_data):
        self.dao.update(new_data)
        return self.dao

    def delete(self, item_id):
        self.dao.delete(item_id)

    