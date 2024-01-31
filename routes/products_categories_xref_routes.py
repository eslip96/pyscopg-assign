from flask import Blueprint, request, jsonify

from controllers import products_categories_xref_controller

products_cat_xref= Blueprint('products_cat_xref', __name__)

@products_cat_xref.route('/product_categories/<product_id>', methods=['GET'])
def get_categories_for_product(product_id):
    return products_categories_xref_controller.get_categories_for_product(product_id)