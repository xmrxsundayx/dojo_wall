from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import users
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

class Posts:
    DB = "dojo_wall"
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save(cls,data):
        # print('unused data passed into create METHOD:',data)
        # data = {
        #     'content': "testing with hard coding",
        #     'user_id': 4
        # }
        query ="""
                    INSERT INTO
                    posts(user_id, content)
                    VALUES
                    (%(user_id)s, %(content)s)
                    ;"""
        result= connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_all_posts(cls):
        query="""
                    SELECT * FROM
                    posts
                    LEFT JOIN
                    users
                    ON
                    posts.user_id = users.id
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query)
        all_posts =[]
        for row in result: 
            posting_user = users.Users({
                'id': row['user_id'],
                'email': row['email'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
                'password': row['password']
        })
            new_post = Posts({
                'id': row['id'],
                'content': row['content'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': posting_user.id
        })
            new_post.user = posting_user
            all_posts.append(new_post)
        return all_posts

    @classmethod
    def delete(cls, post_id):
        query="""
                    DELETE FROM 
                    posts
                    WHERE
                    posts.id =%(id)s
                    ;"""
        data = { 'id': post_id}
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @staticmethod
    def verify_post(post_data):
        errors = []
        if len(post_data['content'])<1:
            errors.append('Post content is required')
        if len(errors) >0:
            for error in errors:
                flash(error, "post_error")
            return False
        else:
            return True
