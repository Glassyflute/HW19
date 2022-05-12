from dao.genre import GenreDAO
from dao.model.genre import GenreSchema


# логика проверок на ИД, наличие полей и др
# CRUD
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

    # def post(self):
    #     new_data = request.json
    #
    #     director_ = DirectorSchema().load(new_data)
    #     new_director = Director(**director_)
    #     with db.session.begin():
    #         db.session.add(new_director)
    #
    #     return "", 201
    # ставим при проверке закрывающий слэш в Postman

    def update(self, new_data):
        self.dao.update(new_data)
        return self.dao

    # genre_selected = db.session.query(Genre).filter(Genre.id == gid)
    # genre_first = genre_selected.first()
    #
    # if genre_first is None:
    #     return "", 404
    #
    # genre_selected.update(new_data)
    # db.session.commit()


    def delete(self, item_id):
        self.dao.delete(item_id)


#     def create(self, genre_d):
#         return self.dao.create(genre_d)
#
#     def update(self, genre_d):
#         self.dao.update(genre_d)
#         return self.dao
#

