import os
import psycopg2
from flask import Flask, request, jsonify

database_name = os.getenv("DATABASE_NAME")

conn = psycopg2.connect(f'dbname={database_name}')
cursor = conn.cursor()


def add_company():
    data = request.form if request.form else request.get_json()
    company_name = data.get("company_name")

    if not company_name:
        return jsonify({"message": "name is required for creating company."}), 400

    cursor.execute("SELECT * FROM companies WHERE company_name=%s", [company_name])
    result = cursor.fetchone()

    cursor.execute("INSERT INTO companies (company_name) VALUES (%s)", (company_name,))
    conn.commit()

    return jsonify({"message": f'company {company_name} has been added to the db'}), 201


def get_all_companies():
    cursor.execute("SELECT * FROM companies;")
    companies = cursor.fetchall()

    company_list = []
    for company in companies:
        company_data = {
            'company_id': company[0],
            'company_name': company[1]
        }
        company_list.append(company_data)
    return jsonify({'companies': company_list}), 200


def update_company(company_id):
    data = request.form if request.form else request.get_json()

    cursor.execute("SELECT * FROM companies WHERE company_id = %s;", [company_id])
    company = cursor.fetchone()

    if not company:
        return jsonify({"message": f"no company found with company id {company_id}"}), 404

    if 'company_name' in data:
        new_company_name = data['company_name']

        cursor.execute("SELECT * FROM companies WHERE company_name = %s AND company_id != %s;", (new_company_name, company_id))
        existing_company_name = cursor.fetchone()
        if existing_company_name:
            return jsonify({"message": f"company name {new_company_name} is already used by another company"}), 400

        cursor.execute("UPDATE companies SET company_name = %s WHERE company_id = %s;", (new_company_name, company_id,))

    conn.commit()

    return jsonify({"message": f'company with company id {company_id} has been updated'}), 200


def get_company_by_id(company_id):

    cursor.execute("SELECT * FROM companies WHERE company_id = %s;", [company_id])
    company = cursor.fetchone()

    if not company:
        return jsonify({"message": f"no company found with company id {company_id}"}), 404

    company_data = {
        'company_id': company[0],
        'company_name': company[1],
    }

    return jsonify({'company': company_data}), 200


def delete_company(company_id):
    try:
        cursor.execute("DELETE FROM product_categories WHERE product_id IN (SELECT product_id FROM products WHERE company_id = %s)", [company_id])
        cursor.execute("DELETE FROM products WHERE company_id = %s", [company_id])
        cursor.execute("DELETE FROM companies WHERE company_id = %s", [company_id])
        conn.commit()
        return jsonify({"message": f'company with company id {company_id} and associated products have been deleted'}), 200
    except:
        conn.rollback()
        return jsonify({'message': 'failed to delete company'}), 400
