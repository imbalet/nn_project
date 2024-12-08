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
    type VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS models(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    brand_id INT REFERENCES brands(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS complectations(
    id SERIAL PRIMARY KEY NOT NULL,
    model_id INT REFERENCES models(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS gens(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    model_id INT REFERENCES models(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS transmissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS engines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS years (
    id SERIAL PRIMARY KEY,
    year INT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS body_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS model_details (
    id SERIAL PRIMARY KEY,
    complectation_id INT REFERENCES complectations(id) ON DELETE CASCADE,
    gen_id INT REFERENCES gens(id) ON DELETE CASCADE,
    transmission_id INT REFERENCES transmissions(id) ON DELETE CASCADE,
    engine_id INT REFERENCES engines(id) ON DELETE CASCADE,
    year_id INT REFERENCES years(id) ON DELETE CASCADE,
    body_type_id INT REFERENCES body_types(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS colors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS gear_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS steering_wheel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS region (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS owners (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL UNIQUE
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
DROP TABLE IF EXISTS complectations CASCADE;
'''
        )
        conn.commit()


def insert_brand(conn, type, name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO brands (type, name) VALUES (%s, %s) RETURNING id;", (type, name))
        conn.commit()
        return cursor.fetchone()[0]  # Возвращаем id вставленной записи


def insert_model(conn, name, type, brand_id):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO models (name, type, brand_id) VALUES (%s, %s, %s) RETURNING id;", (name, type, brand_id))
        conn.commit()
        return cursor.fetchone()[0]


def insert_gen(conn, name, type, model_id):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO gens (name, type, model_id) VALUES (%s, %s, %s) RETURNING id;", (name, type, model_id))
        conn.commit()
        return cursor.fetchone()[0]


def insert_transmission(conn, name, type):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO transmissions (name, type) VALUES (%s, %s) RETURNING id;", (name, type))
        conn.commit()
        return cursor.fetchone()[0]


def insert_engine(conn, name, type):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO engines (name, type) VALUES (%s, %s) RETURNING id;", (name, type))
        conn.commit()
        return cursor.fetchone()[0]


def insert_year(conn, year, year_name):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO years (year) VALUES (%s) RETURNING id;", (year, ))
        conn.commit()
        return cursor.fetchone()[0]


def insert_body_type(conn, name, type):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO body_types (name, type) VALUES (%s, %s) RETURNING id;", (name, type))
        conn.commit()
        return cursor.fetchone()[0]


def insert_color(conn, name, type):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO colors (name, type) VALUES (%s, %s) RETURNING id;", (name, type))
        conn.commit()
        return cursor.fetchone()[0]


def insert_gear_type(conn, name, type):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO gear_type (name, type) VALUES (%s, %s) RETURNING id;", (name, type))
        conn.commit()
        return cursor.fetchone()[0]


def insert_steering_wheel(conn, name, type):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO steering_wheel (name, type) VALUES (%s, %s) RETURNING id;", (name, type))
        conn.commit()
        return cursor.fetchone()[0]


def insert_region(conn, name, type):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO region (name, type) VALUES (%s, %s) RETURNING id;", (name, type))
        conn.commit()
        return cursor.fetchone()[0]


def insert_owner(conn, name, type):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO owners (name, type) VALUES (%s, %s) RETURNING id;", (name, type))
        conn.commit()
        return cursor.fetchone()[0]


def insert_complectation(conn, name, type, model_id):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO complectations (name, type, model_id) VALUES (%s, %s, %s) RETURNING id;", (name, type, model_id))
        conn.commit()
        return cursor.fetchone()[0]


def insert_model_details(conn, model_details):
    with conn.cursor() as cursor:
        for detail in model_details:
            cursor.execute("""
                INSERT INTO model_details (complectation_id, gen_id, transmission_id, engine_id, year_id, body_type_id) 
                VALUES (%s, %s, %s, %s, %s, %s);
            """, detail)
        conn.commit()


if __name__ == "__main__":
    import json
    conn = connect()
    drop_tables(conn)
    create_tables(conn)

    with open("training/d.json") as f:
        data = json.load(f)

    with open("training/labels.json") as f:
        labels = json.load(f)

    owns_ids = {}
    year_ids = {}
    region_ids = {}
    brand_ids = {}
    steering_wheel_ids = {}
    gear_type_ids = {}
    engine_ids = {}
    transmission_ids = {}
    color_ids = {}
    body_type_ids = {}

    for i in labels["owners"]:
        id = insert_owner(conn, i[1], i[0])
        owns_ids[i[0]] = id

    for i in labels["year"]:
        id = insert_year(conn, i)
        year_ids[i] = id

    for i in labels["region"]:
        id = insert_region(conn, i[1], i[0])
        region_ids[i[0]] = id

    for i in labels["mark"]:
        id = insert_brand(conn, i[1], i[0])
        brand_ids[i[0]] = id

    for i in labels["steering_wheel"]:
        id = insert_steering_wheel(conn, i[1], i[0])
        steering_wheel_ids[i[0]] = id

    for i in labels["gear_type"]:
        id = insert_gear_type(conn, i[1], i[0])
        gear_type_ids[i[0]] = id

    for i in labels["engine"]:
        id = insert_engine(conn, i[1], i[0])
        engine_ids[i[0]] = id

    for i in labels["transmission"]:
        id = insert_transmission(conn, i[1], i[0])
        transmission_ids[i[0]] = id

    for i in labels["color"]:
        id = insert_color(conn, i[1], i[0])
        color_ids[i[0]] = id

    for i in labels["body_type_type"]:
        id = insert_body_type(conn, i[1], i[0])
        body_type_ids[i[0]] = id

    model_ids = {}

    for mark in data:
        for model in data[mark]:
            gen_ids = {}
            m_id = insert_model(conn, model, model, brand_ids[mark])
            model_ids[model] = m_id
            for gen in data[mark][model]:
                g_id = insert_gen(conn, gen, gen, m_id)
                gen_ids[gen] = g_id
                