from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name = 'movie_users'
    def __init__(self,db_data):
        self.id=db_data['id']
        self.user_name = db_data['user_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        

    @classmethod
    def save(cls, data):
        query = "insert into users (user_name,email,password,created_at,updated_at) values(%(user_name)s,%(email)s,%(password)s,now(),now());"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    
    
    @classmethod
    def get_by_email(cls,data):
        query = "select * from users where email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def check_existence(cls,data):
        query = "select * from users where email = %(email)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def user_has_movies(cls,data):
        query = "select imdb_id from movies left join movie_user on movie_user.movies_id = movies.id left join users on movie_user.users_id = users.id where users.id = %(id)s and movie_user.type = 'seen';"
        results = connectToMySQL(cls.db_name).query_db( query, data )
        return results
        

    @classmethod
    def get_seen(cls,data):
        query = "select * from movies left join movie_user on movie_user.movies_id = movies.id left join users on movie_user.users_id = users.id where users.id = %(id)s and movie_user.type = %(type)s;"
        results = connectToMySQL(cls.db_name).query_db( query, data )
        return results

  

    @staticmethod
    def validate_user(user):
        is_valid = True
        
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address.","reg")
            is_valid = False
        print(user['email'])    
        if (User.check_existence({'email':user['email']})):    
            flash('Email already exists.','reg')
            is_valid = False
        if len(user['user_name']) < 3:
            flash('User name must be 3 or more letters','reg')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters!','reg')
            is_valid = False
        if user['password']  != user['confirm']:
            flash('Paswords not matching','reg')
            is_valid = False
        return is_valid

