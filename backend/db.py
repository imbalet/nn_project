import psycopg2
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


def connect():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"), 
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return connection

    except Exception as e:
        raise Exception(f"Failed to connect to DB: {e}")


def create_tables(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            '''\
CREATE TABLE IF NOT EXISTS brands(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS models(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    brand_id INT REFERENCES brands(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS gens(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    model_id INT REFERENCES models(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS transmissions (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS engines (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS years (
    id SERIAL PRIMARY KEY,
    year INT NOT NULL,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS body_types (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS model_details (
    id SERIAL PRIMARY KEY,
    model_id INT REFERENCES models(id) ON DELETE CASCADE,
    transmission_id INT REFERENCES transmissions(id) ON DELETE CASCADE,
    engine_id INT REFERENCES engines(id) ON DELETE CASCADE,
    year_id INT REFERENCES years(id) ON DELETE CASCADE,
    body_type_id INT REFERENCES body_types(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS colors (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS gear_type (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS steering_wheel (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS region (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS owners (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);
'''
            )
        conn.commit()


def drop_tables(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            '''\
DROP TABLE IF EXISTS model_details CASCADE;
DROP TABLE IF EXISTS colors CASCADE;
DROP TABLE IF EXISTS gear_type CASCADE;
DROP TABLE IF EXISTS steering_wheel CASCADE;
DROP TABLE IF EXISTS region CASCADE;
DROP TABLE IF EXISTS owners CASCADE;
DROP TABLE IF EXISTS body_types CASCADE;
DROP TABLE IF EXISTS years CASCADE;
DROP TABLE IF EXISTS engines CASCADE;
DROP TABLE IF EXISTS transmissions CASCADE;
DROP TABLE IF EXISTS gens CASCADE;
DROP TABLE IF EXISTS models CASCADE;
DROP TABLE IF EXISTS brands CASCADE;
'''
        )
        conn.commit()

def insert_brand(conn, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO brands (name) VALUES (%s) RETURNING id;", (name,))
        conn.commit()
        return cursor.fetchone()[0]  # Возвращаем id вставленной записи


def insert_model(conn, name, brand_id):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO models (name, brand_id) VALUES (%s, %s) RETURNING id;", (name, brand_id))
        conn.commit()
        return cursor.fetchone()[0]


def insert_gen(conn, name, model_id):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO gens (name, model_id) VALUES (%s, %s) RETURNING id;", (name, model_id))
        conn.commit()
        return cursor.fetchone()[0]


def insert_transmission(conn, type, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO transmissions (type, name) VALUES (%s, %s) RETURNING id;", (type, name))
        conn.commit()
        return cursor.fetchone()[0]


def insert_engine(conn, type, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO engines (type, name) VALUES (%s, %s) RETURNING id;", (type, name))
        conn.commit()
        return cursor.fetchone()[0]


def insert_year(conn, year, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO years (year, name) VALUES (%s, %s) RETURNING id;", (year, name))
        conn.commit()
        return cursor.fetchone()[0]


def insert_body_type(conn, type, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO body_types (type, name) VALUES (%s, %s) RETURNING id;", (type, name))
        conn.commit()
        return cursor.fetchone()[0]


def insert_color(conn, type, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO colors (type, name) VALUES (%s, %s) RETURNING id;", (type, name))
        conn.commit()
        return cursor.fetchone()[0]


def insert_gear_type(conn, type, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO gear_type (type, name) VALUES (%s, %s) RETURNING id;", (type, name))
        conn.commit()
        return cursor.fetchone()[0]


def insert_steering_wheel(conn, type, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO steering_wheel (type, name) VALUES (%s, %s) RETURNING id;", (type, name))
        conn.commit()
        return cursor.fetchone()[0]


def insert_region(conn, type, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO region (type, name) VALUES (%s, %s) RETURNING id;", (type, name))
        conn.commit()
        return cursor.fetchone()[0]


def insert_owner(conn, type, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO owners (type, name) VALUES (%s, %s) RETURNING id;", (type, name))
        conn.commit()
        return cursor.fetchone()[0]


def insert_model_detail(conn, model_id, transmission_id, engine_id, year_id, body_type_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO model_details (model_id, transmission_id, engine_id, year_id, body_type_id) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """, (model_id, transmission_id, engine_id, year_id, body_type_id))
        conn.commit()
        return cursor.fetchone()[0]


if __name__ == "__main__":
    import json
    conn = connect()
    create_tables(conn)
    with open("backend/variants.json") as f:
        data = json.load(f)
    
    for i in data["owners"]:
        insert_owner(conn, i, i if i != '4' else '4+')
    
    for i in data["region"]:
        insert_region(conn, i, i)
    
    for i in data["steering_wheel"]:
        insert_steering_wheel(conn, i, "Справа" if i == "RIGHT" else "Слева")
    
    for i in data["gear_type"]:
        
