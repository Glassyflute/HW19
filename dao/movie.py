from dao.model.movie import Movie
from flask import request


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, item_id):
        item = self.session.query(Movie).filter(Movie.id == item_id).one_or_none()
        return item

    def get_all(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        year_selected = request.args.get("year")

        items_temp = self.session.query(Movie)

        if director_id:
            items_temp = items_temp.filter(Movie.director_id == director_id)

        if genre_id:
            items_temp = items_temp.filter(Movie.genre_id == genre_id)

        if year_selected:
            items_temp = items_temp.filter(Movie.year == year_selected)

        status = request.args.get("status")
        print(f"Status in request is indicated as {status}")
        if status == "new":
            items_temp = items_temp.order_by(Movie.year.desc())

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
        new_data = Movie(**item_data)
        self.session.add(new_data)
        self.session.commit()
        return new_data

    def update(self, new_data):
        item_id = new_data.get("id")
        item = self.session.query(Movie).filter(Movie.id == item_id).update(new_data)
        self.session.commit()

    def delete(self, item_id):
        item = self.get_one(item_id)
        self.session.delete(item)
        self.session.commit()
        
