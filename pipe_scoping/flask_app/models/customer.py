import re

from flask import flash

from flask_bcrypt import Bcrypt

from flask_app import app

from flask_app.config.mysqlconnection import connectToMySQL

bcrypt = Bcrypt (app)

class Customer:
    
    def __init__(self, data):
        self.id = data ['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data ['email']
        self.password = data ['password']
        self.phone = data ['phone']
        self.address = data ['address']
        self.apt_number = data ['apt_number']
        self.city = data ['city']
        self.state = data ['state']
        self.zip = data ['zip']
        self.requestor_type = data ['requestor_type']
        self.location_type = data ['location_type']
        self.year_built =  data ['year_built']
        self.num_of_rooms =  data ['num_of_rooms']
        self.num_of_stories =  data ['num_of_stories']
        self.cleanout_pipes =  data ['cleanout_pipes']
        self.created_at = data ['created_at']
        self.udpated_at = data ['updated_at']

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM customers;"
        results = connectToMySQL("scoping").query_db(query, data)

        customers = []
        for row in results:
            customers.append(Customer(row))

        return Customer


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM customers WHERE email = %(email)s;"
        results = connectToMySQL("scoping").query_db(query, data)

        if len(results) < 1:
            return False

        return Customer(results[0])


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM customers WHERE id = %(id)s;"
        results = connectToMySQL("scoping").query_db(query, data)

        if len(results) < 1:
            return False

        return Customer(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE customers SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, phone = %(phone)s, address = %(address)s, apt_number = %(apt_number)s, city = %(city)s, state = %(state)s, zip = %(zip)s, requestor_type = %(requestor_type)s, location_type = %(location_type)s, year_built = %(year_built)s, num_of_rooms = %(num_of_rooms)s, num_of_stories = %(num_of_stories)s, cleanout_pipes = %(cleanout_pipes)s, created_at = NOW(), updated_at = NOW() VALUES WHERE id = %(id)s;"

        return connectToMySQL("scoping").query_db(query, data)


    @classmethod
    def delete(cls,data):
        query = "DELETE FROM customers WHERE id = %(id)s;"
        
        connectToMySQL("scoping").query_db(query, data)


    @classmethod
    def create(cls, data):
        query = "INSERT INTO customers (first_name, last_name, email, password, phone, address, apt_number, city, state, zip, requestor_type, location_type, year_built, num_of_rooms, num_of_stories, cleanout_pipes, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, %(address)s, %(apt_number)s, %(city)s, %(state)s,  %(zip)s, %(requestor_type)s, %(location_type)s, %(year_built)s, %(num_of_rooms)s, %(num_of_stories)s, %(cleanout_pipes)s, NOW(), NOW())"

        return connectToMySQL("scoping").query_db(query, data)


    @staticmethod
    def register_validator(post_data):
        is_valid = True

        if len(post_data["first_name"]) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False

        if len(post_data["last_name"]) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']): 
            flash("Invalid Email")
            is_valid = False
        else:
            customer = Customer.get_by_email({"email": post_data['email']})
            if customer:
                flash("Email is already in use!")
                is_valid = False

        if len(post_data["password"]) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False

        if post_data["password"] != post_data['confirm_password']:
            flash("Password and Confirm password must match.")
            is_valid = False

        return is_valid


    @staticmethod
    def login_validator(post_data):
        customer = Customer.get_by_email({"email": post_data['email']})

        if not customer:
            flash("Invalid Credentials")
            return False

        if not bcrypt.check_password_hash(customer.password, post_data["password"]):
            flash("Invalid Credentials")
            return False

        return True