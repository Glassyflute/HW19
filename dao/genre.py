from dao.model.genre import Genre
from flask import request


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, item_id):
        item = self.session.query(Genre).filter(Genre.id == item_id).one_or_none()
        return item

    def get_all(self):
        items_temp = self.session.query(Genre)

        page = request.args.get("page")
        print(f"Page in request is indicated as {page}")
        if page is not None:
            per_page_limit = 12
            page_int = int(page)
            items_paginated = items_temp.limit(per_page_limit).offset(page_int)
            return items_paginated
        else:
            items = items_temp.all()
            return items

    def create(self, item_data):
        new_data = Genre(**item_data)
        self.session.add(new_data)
        self.session.commit()
        return new_data

    # def update(self, item_data):
    #     item_id = item_data.get("id")
    #     item = self.get_one(item_id)
    #
    #     item.update(item_data)
    #
    #     self.session.add(item)
    #     self.session.commit()
    #     return item

    def update(self, new_data):
        item_id = new_data.get("id")
        item = self.session.query(Genre).filter(Genre.id == item_id).update(new_data)

        # item_id = item_data.get("id")
        # item = self.session.query(Genre).filter(Genre.id == item_id).update(item_data)

        # if item_id is None:
        #     abort(401, message="Indicate id in data submitted to proceed with updating.")

        # if item != 1:
        #     ...
        self.session.commit()

    # def put(self, did):
    #     director_selected = db.session.query(Director).filter(Director.id == did)
    #     director_first = director_selected.first()
    #
    #     if director_first is None:
    #         return "", 404
    #
    #     new_data = request.json
    #     director_selected.update(new_data)
    #     db.session.commit()
    #
    #     return "", 204

    def delete(self, item_id):
        item = self.get_one(item_id)
        self.session.delete(item)
        self.session.commit()

    # def delete(self, rid):
    #     genre = self.get_one(rid)
    #     self.session.delete(genre)
    #     self.session.commit()
    #

    # def update(self, genre_d):
    #     genre = self.get_one(genre_d.get("id"))
    #     genre.name = genre_d.get("name")
    #
    #     self.session.add(genre)
    #     self.session.commit()
