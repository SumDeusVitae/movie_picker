from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Movie:
    db_name = 'movie_users'
    def __init__(self,data):
        self.id = data['id']
        self.movie_name= data['movie_name']
        self.img_src = data['img_src']
        self.description = data['plot']
        self.year = data['year']
        self.imdb_id = data['imdb_id']
        self.imdb_rating = data['imdb_rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    

    @classmethod
    def save(cls, data):
        query ="insert into movies (movie_name,img_src,description,year,imdb_id, imdb_rating, created_at,updated_at) values(%(movie_name)s,%(img_src)s,%(description)s,%(year)s,%(imdb_id)s,%(imdb_rating)s,now(),now());"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def check_existence(cls,data):
        query ="select * from movies where imdb_id = %(imdb_id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    

    @classmethod
    def insert_to_seen(cls,data):
        query ="insert into movie_user (movies_id, users_id, type) values(%(movies_id)s,%(users_id)s,%(type)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    @classmethod
    def replace_in_seen(cls,data):
        query ="update movie_user set type=%(type)s where movies_id = %(movie_id)s and users_id= %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def unsee(cls,data):
        query ="update movie_user set type=%(type)s where movies_id = %(movie_id)s and users_id= %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def search_by_imdb_id(cls,data):
        query ="select * from movies where imdb_id = %(imdb_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    


    @staticmethod
    def validate_movie(movie):
        new_movie = True
        if (Movie.check_existence(movie)):    
            new_movie = False
        return new_movie


