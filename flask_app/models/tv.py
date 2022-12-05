from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# create a regular expression object that we'll use later   
class Tv:
    db_name='exam2'
    def __init__(self,data):
        self.id = data['id'],
        self.title = data['title'],
        self.network = data['network'],
        self.date = data['date'],
        self.description = data['description'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at'],
        self.user_id = data['user_id']
    @classmethod
    def create_tv(cls,data):
        query = 'INSERT INTO tvs (title, network, date, description, user_id) VALUES ( %(title)s, %(network)s,%(date)s, %(description)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getAllTv(cls):
        query= 'SELECT * FROM tvs LEFT JOIN users ON tvs.user_id = users.id;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        tvs= []
        if results:
            for row in results:
                tvs.append(row)
            return tvs
        return tvs
    @classmethod
    def get_tv_by_id(cls, data):
        query= 'SELECT * FROM tvs WHERE tvs.id = %(tv_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]
        
    @classmethod
    def get_user_by_email(cls, data):
        query= 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]
        

    @classmethod
    def get_all_user_info(cls, data):
        query= 'SELECT * FROM users LEFT JOIN tvs on tvs.user_id = users.id WHERE users.id = %(user_id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        tvs = []
        if results:
            for row in results:
                tvs.append(row)
            return tvs
        return tvs
    
    @classmethod
    def update_tv(cls,data):
        query = 'UPDATE tvs SET title=%(title)s,network=%(network)s , date=%(date)s,description=%(description)s , user_id = %(user_id)s WHERE tvs.id = %(tv_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    @staticmethod
    def validate_tv(tv):
        is_valid = True
        if len(tv['title']) < 2:
            flash("Title must be at least 3 characters.", 'title')
            is_valid = False
        if len(tv['description']) < 3:
            flash("TV description be at least 3 characters.", 'description')
            is_valid = False
        if tv['date'] == '':
            flash("Date of Tv is required", 'date')
            is_valid = False
        if len(tv['network']) < 2:
            flash("Network Tv must be at least 2 charaters.", 'network')
            is_valid = False
        return is_valid
        
    
