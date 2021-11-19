import os

from flask import render_template, redirect, request, session

from flask_app import app

from flask_app.models.customer import Customer

from types import MethodDescriptorType
import re
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)

# ====================display========================

@app.route("/")
def index():
    # if "uuid" in session:
    #     return redirect("/customer_details")

    return render_template("index.html")


@app.route("/registration")
def registration_form():
    return render_template("registration.html")


@app.route("/customer_details")
def view_customer_details():
    return render_template("customer_details.html", customer = Customer.get_by_id({"id": session['uuid']}))


@app.route("/edit_details") 
def edit_details():
    return render_template("edit_details.html", customer = Customer.get_by_id({"id": session['uuid']}))




# ====================action========================


@app.route("/registration_form", methods = ["POST"])
def register():
    if not Customer.register_validator(request.form):
        return redirect("/registration")

    hash_browns = bcrypt.generate_password_hash(request.form['password'])
    data ={
        **request.form,
        "password": hash_browns
    }
    customer_id = Customer.create(data)
    session["uuid"] = customer_id
    return redirect("/customer_details")


@app.route("/edit_details", methods = ["POST"])
def edit():
    if not Customer.register_validator(request.form):
        return redirect("/customer_details")

    hash_browns = bcrypt.generate_password_hash(request.form['password'])
    data ={
        **request.form,
        "password": hash_browns,
        "id": session['uuid']
    }

    customer_id = Customer.update(data)
    session["uuid"] = customer_id
    return redirect("/customer_details")


@app.route("/customer_details", methods = ["POST"])
def upload():
    if request.method=="POST":
        file = request.files["file"]
        file.save(os.path.join("uploads", file.filename))
    return render_template("index.html", message="Success")


@app.route("/login", methods = ["POST"])
def login():
    if not Customer.login_validator(request.form):
        return redirect ("/")

    customer = Customer.get_by_email({"email": request.form["email"]})
    session["uuid"] = customer.id
    return redirect ("/customer_details")


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")

@app.route("/customer_details/delete")
def delete_customer():
    Customer.delete({"id": session['uuid']})
    return redirect("/")