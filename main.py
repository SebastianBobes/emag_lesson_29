import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import psycopg2 as ps

import emag_db

app = Flask(__name__)
config = emag_db.read_config()
user_id, username, password = emag_db.read_admins(config)

users = {
    username: password
}

auth = HTTPBasicAuth()



@auth.verify_password
def verify_password(username, password):
    if username in users.keys():
        if password == users[username]:
            return True

    return False

@app.route("/")
def first_function():
    print("S a rulat cand apasam pe link")
    return render_template("login.html")


@app.route("/test")
def second_function():
    print("S a rulat cand apasam pe link")
    return render_template("test.html")


@app.route("/login", methods=["POST"])
def web_login():
    user = request.form['username']
    passwd = request.form['password']
    if user in users.keys():
        if passwd == users[user]:
            data = emag_db.read_products(config)
            return render_template("home.html", data=data)
        else:
            print("Nu sunt corecte credentialele!")
    product_to_delete = request.form['product_name']
    print(product_to_delete)

    # return render_template("login.html")
@app.route("/delete_product", methods=["post"])
def del_prod():
    product_name = request.form['product_name']
    with (ps.connect(**config) as conn):
        with conn.cursor() as cursor:
            sql_query = (f"delete from emag.products where name = '{product_name}' ")
            cursor.execute(sql_query, config)
            data = emag_db.read_products(config)
            return render_template("home.html", data=data)

@app.route("/modify_price", methods=["post"])
def update_price():
    product_name = request.form['product_name_to_modify']
    new_price = int(request.form['new_price'])
    with (ps.connect(**config) as conn):
        with conn.cursor() as cursor:
            sql_query = (f"UPDATE emag.products SET price = {new_price}  where name = '{product_name}' ")
            cursor.execute(sql_query, config)
            data = emag_db.read_products(config)
            return render_template("home.html", data=data)

@app.route("/show_expensive_prod", methods=["post"])
def show_expensive_prod():
    with (ps.connect(**config) as conn):
        with conn.cursor() as cursor:
            sql_query = ("select name, price from emag.products where price = (select max(price) from emag.products )")
            cursor.execute(sql_query,config)
            data = emag_db.read_products(config)
            x=cursor.fetchone()
            most_expensive_product = x[0]
            highest_price = x[1]
            return render_template("home.html", most_expensive_product=most_expensive_product, highest_price=highest_price, data = data)




@app.route(rule="/hire_employees", methods = ["POST"])
@auth.login_required()
def hire():
        new_employee = input("Dati datele noului angajet: prenume, nume, departament, salariu si anul in care a inceput!")
        new_employee = new_employee.split(" ")
        emag_db.hire_employee(config, new_employee)
        return {"MESSAGE": "s a realizat!"}

@app.route(rule="/see_departments", methods = ["GET"])
def get_departs():
    with (ps.connect(**config) as conn):
        with conn.cursor() as cursor:
            sql_query = ('select department from emag.employees e ')
            cursor.execute(sql_query, config)
            return {F"MSG": f"{set(cursor.fetchall())}"}

@app.route(rule="/see_emps_from_a_dep", methods = ["GET"])
def get_emps():
    with (ps.connect(**config) as conn):
        with conn.cursor() as cursor:
            dep = input("Dati un departament:")
            sql_query = (f"select last_name, first_name from emag.employees e where department = '{dep}'")
            cursor.execute(sql_query, config)
            return {f"Employees from {dep}": f"{(cursor.fetchall())}"}

@app.route(rule = "/change_budget" ,methods = ['PUT'])
@auth.login_required()
def change_budget():
    if emag_db.change_budget_of_project(config) == True:
        return{"MSG": "Budget has beem modified"}
    else:
        return{"MSG": "ID DOES NOT EXISTS!"}

@app.route(rule = "/avg_budget" ,methods = ['GET'])
def avg_budget():
    emag_db.get_average_budget_for_all_projects(config)
    return{"AVERAGE BUDGET FOR ALL PROJECTS:": F"{emag_db.get_average_budget_for_all_projects(config)}"}




if __name__ == '__main__':
    app.run()
