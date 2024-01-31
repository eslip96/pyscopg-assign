from flask import Blueprint, request, jsonify

from controllers import companies_controller

companies = Blueprint('companies', __name__)


@companies.route('/companies', methods=['POST'])
def add_company():
    return companies_controller.add_company()

@companies.route('/companies', methods=['GET'])
def get_all_companies():
    return companies_controller.get_all_companies()

@companies.route('/companies/<company_id>', methods=['PUT'])
def update_company(company_id):
    return companies_controller.update_company(company_id)

@companies.route('/companies/<company_id>', methods=['GET'])
def get_company_by_id(company_id):
    return companies_controller.get_company_by_id(company_id)