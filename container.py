from dao.director import DirectorDAO
from dao.genre import GenreDAO
from dao.movie import MovieDAO
from dao.user import UserDAO
from dao.auth import AuthUserDAO

from services.directors_service import DirectorsService
from services.genres_service import GenresService
from services.movies_service import MoviesService
from services.users_service import UsersService
from services.auth_users_service import AuthUsersService

from setup_db import db

director_dao = DirectorDAO(session=db.session)
genre_dao = GenreDAO(session=db.session)
movie_dao = MovieDAO(session=db.session)
user_dao = UserDAO(session=db.session)
auth_user_dao = AuthUserDAO(session=db.session)

director_service = DirectorsService(dao=director_dao)
genre_service = GenresService(dao=genre_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UsersService(dao=user_dao)
auth_user_service = AuthUsersService(dao=auth_user_dao)
