from flask import Blueprint, request, jsonify

from controllers import categories_controller

categories = Blueprint('categories', __name__)


@categories.route('/categories', methods=['POST'])
def create_category():
    return categories_controller.create_category()

@categories.route('/categories/all_categories', methods=['GET'])
def get_all_categories():
    return categories_controller.get_all_categories()

@categories.route('/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    return categories_controller.update_category(category_id)

@categories.route('/categories/<category_id>', methods=['GET'])
def get_category_by_id(category_id):
    return categories_controller.get_category_by_id(category_id)