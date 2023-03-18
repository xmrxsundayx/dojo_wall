from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

class Users:
    DB = "dojo_wall"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts =[]

# *****Create*****

    @classmethod
    def save(cls, data ):
        query ="""
                    INSERT INTO
                    users(first_name, last_name, email, password)
                    VALUES
                    (%(first_name)s,%(last_name)s,%(email)s,%(password)s)
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        # print(result)
        return result

# *****Read*****

    @classmethod
    def get_user_by_id(cls,data):
        query ="""
                    SELECT * FROM
                    users
                    WHERE
                    id = %(id)s
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_user_by_email(cls,data):
        query ="""
                    SELECT * FROM
                    users
                    WHERE
                    email = %(email)s
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])

# *****Users and Posts*****
    # @classmethod
    # def all_users_posts(cls, data ):
    #     query ="""
    #                 SELECT * FROM 
    #                 users 
    #                 LEFT JOIN 
    #                 posts 
    #                 ON users.id = posts.users_id WHERE 
    #                 users.id = %(id)s
    #                 ;"""
    #     results = connectToMySQL(cls.DB).query_db(query,data)
    #     users = cls(results[0])
    #     print(results)
    #     for row in results:
    #         post_info = {
    #             'id': row['post.id'],
    #             'user_id': row['user_id'], 
    #             'content': row['content'],
    #             'created_at': row['created_at'],
    #             'updated_at': row['updated_at']
    #         }
    #         users.posts.append(Posts(post_info))
    #     return users


# *****Update*****



# *****Delete*****



# *****Validate*****
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name'])< 3:
            flash('First name must be at least 1 character.','reg')
            is_valid = False
        if len(user['last_name'])< 3:
            flash('Last name must be at least 1 character','reg')
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email','reg')
            is_valid=False
        password = user['password']
        if len(password) < 8:
            flash('Password must be at least 8 characters long.','reg')
            is_valid = False
        else:
            missing_reqs = []
            if not re.search(r"[a-z]", password):
                missing_reqs.append("lowercase letter")
            if not re.search(r"[A-Z]", password):
                missing_reqs.append("uppercase letter")
            if not re.search(r"[0-9]", password):
                missing_reqs.append("digit")
            if missing_reqs:
                flash(f"Password is missing the following required character types: {', '.join(missing_reqs)}",'reg')
                is_valid = False
        if user['confirm_password'] != user['password']:
            flash('Passwords do not match','reg')
            is_valid=False
        return is_valid
