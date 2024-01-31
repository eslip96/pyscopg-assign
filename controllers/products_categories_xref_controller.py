import os
import psycopg2
from flask import Flask, request, jsonify

database_name = os.getenv("DATABASE_NAME")

conn = psycopg2.connect(f'dbname={database_name}')
cursor = conn.cursor()


def get_categories_for_product(product_id):
    cursor.execute("""
        SELECT
            categories.category_id,
            categories.category_name
        FROM
            productcategoriesxref
        INNER JOIN
            categories ON productcategoriesxref.category_id = categories.category_id
        WHERE
            productcategoriesxref.product_id = %s;
    """, [product_id])
    categories = cursor.fetchall()

    categories_list = []
    for category in categories:
        category_data = {
            'category_id': category[0],
            'category_name': category[1],
        }
        categories_list.append(category_data)

    return jsonify({'categories': categories_list})