import os
import psycopg2
from flask import Flask, request, jsonify

database_name = os.getenv("DATABASE_NAME")

conn = psycopg2.connect(f'dbname={database_name}')
cursor = conn.cursor()

def create_category():
    data = request.form if request.form else request.get_json()
    category_name = data.get("category_name")

    if not category_name:
        return jsonify({"message": "category name is required for creating a category."}), 400

    cursor.execute("SELECT * FROM categories WHERE category_name=%s", [category_name])
    if cursor.fetchone():
        return jsonify({"message": "category already exists"}), 400

    cursor.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING category_id", (category_name,))
    category_id = cursor.fetchone()[0]
    conn.commit()

    return jsonify({"message": f'category {category_name} with ID {category_id} has been added to the database'}), 201


def get_all_categories():
    cursor.execute("SELECT * FROM categories;")
    categories = cursor.fetchall()

    category_list = []
    for category in categories:
        category_data = {
            'category_id': category[0],
            'category_name': category[1]
        }
        category_list.append(category_data)

    return jsonify({'categories': category_list})

def update_category(category_id):
    data = request.form if request.form else request.get_json()


    cursor.execute("SELECT * FROM categories WHERE category_id = %s;", [category_id])
    category = cursor.fetchone()

    if not category:
        return jsonify({"message": f"no category found with category_id {category_id}"}), 404

    if 'category_name' in data:
        category_name = data['category_name']
        cursor.execute("UPDATE categories SET category_name = %s WHERE category_id = %s;", (category_name, category_id))

    if 'new_category_id' in data:
        new_category_id = data['new_category_id']

        cursor.execute("SELECT * FROM categories WHERE category_id = %s;", [new_category_id])
        existing_category = cursor.fetchone()

        if existing_category:
            return jsonify({"message": f"category with category_id {new_category_id} already exists."}), 400

        cursor.execute("UPDATE categories SET category_id = %s WHERE category_id = %s;", (new_category_id, category_id))

    conn.commit()

    return jsonify({"message": f'category with category_id {category_id} has been updated'}), 200

def get_category_by_id(category_id):
    cursor.execute("SELECT * FROM categories WHERE category_id = %s;", [category_id])
    category = cursor.fetchone()

    if not category:
        return jsonify({"message": f"no category found with category_id {category_id}"}), 404

    category_data = {
        'category_id': category[0],
        'category_name': category[1],
    }

    return jsonify({'category': category_data})