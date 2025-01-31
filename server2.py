from flask import Flask, render_template, request
from http import HTTPStatus
import json
from config import db

app = Flask(__name__)

# Home page
@app.get("/")
def home():
    return render_template("home.html")

### Endpoints ###

# Fix the id from MongoDB
def fix_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj

# GET /api/catalog
@app.get("/api/catalog")
def get_catalog():
    products_db = []
    cursor = db.products.find({})
    for product in cursor:
        products_db.append(fix_id(product))
    return json.dumps(products_db), HTTPStatus.OK

# POST /api/catalog
@app.post("/api/catalog")
def save_product():
    product = request.get_json()
    db.products.insert_one(product)
    return "Product saved", HTTPStatus.CREATED

# GET /api/reports/total
@app.get("/api/reports/total")
def get_total():
    total_products = db.products.count_documents({})
    return json.dumps({"total": total_products}), HTTPStatus.OK

# GET /api/catalog/<category>
@app.get("/api/catalog/<category>")
def get_catalog_category(category):
    products_db = []
    cursor = db.products.find({})
    for product in cursor:
        if(product["category"] == category):
            products_db.append(fix_id(product))
    if len(products_db) == 0:
        return "Category not found", HTTPStatus.NOT_FOUND
    return json.dumps(products_db), HTTPStatus.OK

app.run(debug = True)
