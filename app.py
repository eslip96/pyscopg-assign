import os
from flask import Flask

from routes.companies_routes import companies
from routes.categories_routes import categories
from routes.products_routes import products
from routes.products_categories_xref_routes import products_cat_xref
# from db import create_all

app = Flask(__name__)
app_host = os.getenv('APP_HOST')
app_port = os.getenv('APP_PORT')

app.register_blueprint(companies)
app.register_blueprint(categories)
app.register_blueprint(products)
app.register_blueprint(products_cat_xref)




if __name__ == '__main__':
    # create_all()
    app.run(host=app_host, port=app_port)