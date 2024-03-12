import os
import psycopg2
from flask import Flask, request, jsonify

database_name = os.getenv("DATABASE_NAME")

conn = psycopg2.connect(f'dbname={database_name}')
cursor = conn.cursor()


def create_product():
    data = request.form if request.form else request.json

    product_name = data.get("product_name")
    description = data.get("description")
    price = data.get("price")
    active = data.get("active", True)
    company_id = data.get("company_id")
    category_id = data.get("category_id")

    if not product_name or not company_id or not category_id:
        return jsonify({"message": "product name, company id, and category ids are required fields"}), 400

    cursor.execute("SELECT * FROM companies WHERE company_id = %s;", [company_id])
    company = cursor.fetchone()
    if not company:
        return jsonify({"message": f"no company found with company id {company_id}"}), 400

    cursor.execute("""
        INSERT INTO products (product_name, description, price, active, company_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (product_name, description, price, active, company_id))

    cursor.execute("""
        INSERT INTO productcategoriesxref (product_id, category_id)
        VALUES (LASTVAL(), %s)
    """, [category_id])

    conn.commit()

    return jsonify({"message": f'product {product_name} has been added to the db'}), 201


def get_all_products():
    cursor.execute("""
            SELECT p.product_id, p.product_name, p.description, p.price, p.active, p.company_id, pc.category_id
            FROM products p
            LEFT JOIN productcategoriesxref pc ON p.product_id = pc.product_id
            GROUP BY p.product_id, p.product_name, p.description, p.price, p.active, p.company_id, pc.category_id;
    """)
    products = cursor.fetchall()

    products_list = []
    for product in products:
        product_data = {
            'product_id': product[0],
            'product_name': product[1],
            'description': product[2],
            'price': product[3],
            'active': product[4],
            'company_id': product[5],
            'category_id': product[6],
        }
        products_list.append(product_data)

    return jsonify({'products': products_list}), 200


def get_active_products():
    cursor.execute("SELECT product_id, product_name FROM products WHERE active=true;")
    active_products = cursor.fetchall()

    product_list = [
        {'product_id': product[0], 'product_name': product[1]}
        for product in active_products
    ]

    return jsonify({'active products': product_list}), 200


def get_product_by_id(product_id):
    cursor.execute("""
        SELECT
            products.product_id,
            products.product_name,
            products.description,
            products.price,
            products.active,
            products.company_id,
            array_agg(categories.category_name) AS categories
        FROM
            products
        LEFT JOIN
            productcategoriesxref ON products.product_id = productcategoriesxref.product_id
        LEFT JOIN
            (SELECT category_id, category_name FROM categories) AS categories ON productcategoriesxref.category_id = categories.category_id
        WHERE
            products.product_id = %s
        GROUP BY
            products.product_id;
    """, [product_id])

    product = cursor.fetchone()

    if not product:
        return jsonify({"message": f"no product found with product id {product_id}"}), 404

    product_data = {
        'product_id': product[0],
        'product_name': product[1],
        'description': product[2],
        'price': product[3],
        'active': product[4],
        'company_id': product[5],
        'category_id': product[6],
    }

    return jsonify({'product': product_data}), 200


def update_product(product_id):
    data = request.form if request.form else request.get_json()

    cursor.execute("SELECT * FROM products WHERE product_id = %s;", [product_id])
    product = cursor.fetchone()

    if not product:
        return jsonify({"message": f"no product found with product id {product_id}"}), 404

    if 'product_name' in data:
        new_product_name = data['product_name']

        cursor.execute("SELECT * FROM products WHERE product_name = %s AND product_id != %s;", (new_product_name, product_id))
        existing_product_name = cursor.fetchone()
        if existing_product_name:
            return jsonify({"message": f"product name {new_product_name} is already used by another product"}), 400

        cursor.execute("UPDATE products SET product_name = %s WHERE product_id = %s;", (new_product_name, product_id))

    if 'description' in data:
        description = data['description']
        cursor.execute("UPDATE products SET description = %s WHERE product_id = %s;", (description, product_id))

    if 'price' in data:
        price = data['price']
        cursor.execute("UPDATE products SET price = %s WHERE product_id = %s;", (price, product_id))

    if 'active' in data:
        active = data['active']
        cursor.execute("UPDATE products SET active = %s WHERE product_id = %s;", (active, product_id))

    if 'company_id' in data:
        new_company_id = data['company_id']

        cursor.execute("SELECT * FROM companies WHERE company_id = %s;", [new_company_id])
        company = cursor.fetchone()
        if not company:
            return jsonify({"message": f"no company found with that company id {new_company_id}"}), 400

        if 'product_id' in data:
            new_product_id = data['product_id']
            cursor.execute("SELECT * FROM products WHERE product_id = %s AND product_id != %s;", (new_product_id, product_id))
            existing_product_id = cursor.fetchone()
            if existing_product_id:
                return jsonify({"message": f"product id {new_product_id} is already used by another product"}), 400

        cursor.execute("UPDATE products SET company_id = %s WHERE product_id = %s;", (new_company_id, product_id))

    conn.commit()

    return jsonify({"message": f'product with product id {product_id} has been updated'}), 200


def get_products_by_company_id(company_id):

    cursor.execute("SELECT * FROM products WHERE company_id = %s;", [company_id])
    products = cursor.fetchall()

    if not products:
        return jsonify({"message": f"no products found for company id {company_id}"}), 404

    products_list = []
    for product in products:
        product_data = {
            'product_id': product[0],
            'product_name': product[1],
            'description': product[2],
            'price': product[3],
            'active': product[4],
            'company_id': product[5],
        }
        products_list.append(product_data)

    return jsonify({'products': products_list}), 200


def delete_product(product_id):
    try:
        cursor.execute("DELETE FROM products WHERE product_id = %s", [product_id])
        conn.commit()
        return jsonify({'message': 'product with product id {product_id} has been deleted'}), 200
    except:
        conn.rollback()
        return jsonify({'message': 'failed to delete product'}), 400
