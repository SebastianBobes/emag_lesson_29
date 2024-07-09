import json
import psycopg2 as ps

def read_from_database(sql_query: str,config: dict):
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                response = cursor.fetchall()
                columns = [item.name for item in cursor.description]
                new_data = []
                for employee in response:
                    new_data.append(dict(zip(columns, employee)))
                return new_data
    except Exception as e:
        print(f"Failure on reading from database. Error: {e}")

def execute_query(sql_query: str, config: dict):
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                return cursor.statusmessage
    except Exception as e:
        print(f"Failure on reading from database. Error: {e}")
        return False

def read_config(path: str = "config.json"):
    with open(path, "r") as f:
        config = json.loads(f.read())

    return config


def read_admins(config: dict, table: str = "emag.emag_admin"):

    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            sql_query = f"select * from {table}"
            cursor.execute(sql_query)
            users = cursor.fetchone()
            return users

def hire_employee(config: dict, list_of_values: list):
    with (ps.connect(**config) as conn):
        with conn.cursor() as cursor:
            sql_query = ("INSERT into emag.employees (first_name, last_name, department, salary, starting_year)"
            f"values('{list_of_values[0]}', '{list_of_values[1]}', '{list_of_values[2]}', {list_of_values[3]}, {list_of_values[4]})")
            cursor.execute(sql_query, config)
            return {"MESSAGE": "s a realiza"}

def change_budget_of_project(config:dict):
    with (ps.connect(**config) as conn):
        with conn.cursor() as cursor:
            sql_query = ("select id,project_name from emag.project")
            cursor.execute(sql_query, config)
            print(cursor.fetchall())
            sql_query = ("select id from emag.project")
            cursor.execute(sql_query,config)
            id_from_db = cursor.fetchall()
            project_id = input("Dati id -ul proiectului la care sa fie modificat bugetul: ")
            id_list = [row[0] for row in id_from_db]
            if int(project_id) in id_list:
                new_budget = input("Dati un nou buget:")
                sql_query = (f"update emag.project set budget = {new_budget} where id = {project_id} ")
                cursor.execute(sql_query, config)
                return True
            else:
                return False

def get_average_budget_for_all_projects(config:dict):
    with (ps.connect(**config) as conn):
        with conn.cursor() as cursor:
            sql_query = ("select avg(budget) from emag.project")
            cursor.execute(sql_query, config)
            return (cursor.fetchone()[0])

def read_products(config: dict, table: str = "emag.products"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            sql_query = f"select name, store, price from {table}"
            cursor.execute(sql_query)
            products = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            products_list = []
            for item in products:
                products_list.append(dict(zip(columns, item)))

            return products_list
def add_product_in_db(config: dict, my_dict: dict):
    with (ps.connect(**config) as conn):
        with conn.cursor() as cursor:
            sql_query = ("INSERT into emag.products (name, store, price)"
                         f"values('{my_dict['name']}', '{my_dict['store']}', {my_dict['price']})")
            cursor.execute(sql_query, config)
            




if __name__ == '__main__':
    config = read_config()
    admins = read_admins(config)
    products = read_products(config)

    my_dict = {}
    my_dict['name'] = input("Dati numele produsului: ")
    my_dict['store'] = input("Dati magazinul de unde este achizitionat produsul: ")
    my_dict['price'] = input("Dati pretul produsului: ")
    add_product_in_db(config, my_dict)