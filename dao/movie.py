from dao.model.movie import Movie
from flask import request


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, item_id):
        item = self.session.query(Movie).filter(Movie.id == item_id).one_or_none()
        return item

    def get_all(self, status_is_new=False, page=0):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        year_selected = request.args.get("year")
        # status -- new -- would sort and show most recent items
        # page = is optional param = limit 12 per page == offset xxx ==

        items_temp = self.session.query(Movie)

        if director_id:
            items_temp = items_temp.filter(Movie.director_id == director_id)

        if genre_id:
            items_temp = items_temp.filter(Movie.genre_id == genre_id)

        if year_selected:
            items_temp = items_temp.filter(Movie.year == year_selected)

        if status_is_new:
            items_temp = items_temp.order_by(Movie.year.desc())

        if page >= 1:
            items_temp = items_temp.limit(12).offset(page)
        # int(page)
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
        
