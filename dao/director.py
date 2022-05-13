from dao.model.director import Director
from flask import request


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, item_id):
        item = self.session.query(Director).filter(Director.id == item_id).one_or_none()
        return item

    def get_all(self):
        items_temp = self.session.query(Director)

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
        new_data = Director(**item_data)
        self.session.add(new_data)
        self.session.commit()
        return new_data

    def update(self, new_data):
        item_id = new_data.get("id")
        item = self.session.query(Director).filter(Director.id == item_id).update(new_data)
        self.session.commit()

    def delete(self, item_id):
        item = self.get_one(item_id)
        self.session.delete(item)
        self.session.commit()
        
