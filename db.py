from flask import Flask, jsonify, request
import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def create_tables():
    database_name = os.environ.get('DATABASE_NAME')
    conn = psycopg2.connect(f"dbname={database_name}")
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR NOT NULL UNIQUE
        );
    """)
    conn.commit()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR NOT NULL UNIQUE
        );
    """)
    conn.commit()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR NOT NULL UNIQUE,
            description VARCHAR,
            price FLOAT,
            active BOOLEAN DEFAULT true,
            company_id INTEGER REFERENCES companies(company_id)
        );
    """)
    conn.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productcategoriesxref (
            product_id SERIAL REFERENCES products(product_id),
            category_id SERIAL REFERENCES categories(category_id),
            PRIMARY KEY (product_id, category_id)
            -- Add other fields as needed
        );
    """)
    conn.commit()

    print("Tables created")

if __name__ == "__main__":
    create_tables()


