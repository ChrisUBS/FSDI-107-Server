from flask import Flask, render_template, request
from http import HTTPStatus
import json
from config import db

app = Flask(__name__)

### Endpoints

# This is a JSON implementation
@app.get("/test")
def test():
    return "This is another endpoint", 200

# Home page
@app.get("/")
def home():
    return "<h1>Hello from flask, this is the home page</h1>", HTTPStatus.OK

# About page
@app.get("/about")
def about():
    return "<h1>This is the about page</h1>", HTTPStatus.OK

# @app.post("/")
# @app.put("/")
# @app.patch("/")
# @app.delete("/")
# if I don't have some method, than means that method is not valid

# About me page
@app.get("/about-me")
def about_me():
    # return "<h1>This is the about me page</h1>", HTTPStatus.OK
    user_name = "Chris"
    return render_template("about-me.html", name = user_name)

products = []

# Fix the id from MongoDB
def fix_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj

# GET
@app.get("/api/products")
def get_products():
    products_db = []
    cursor = db.products.find({})
    for product in cursor:
        products_db.append(fix_id(product))
    return json.dumps(products_db), HTTPStatus.OK

# POST
@app.post("/api/products")
def save_product():
    product = request.get_json()
    print(f"product {product}")
    # products.append(product)
    db.products.insert_one(product)
    return "Product saved", 201

# PUT
@app.put("/api/products/<int:index>")
def update_product(index):
    updated_product = request.get_json()
    print(f"Update {index} with {updated_product}")

    if 0 <= index < len(products):
        products[index] = updated_product
        return json.dumps(updated_product), HTTPStatus.OK
    else:
        return "Product not found", HTTPStatus.NOT_FOUND

# DELETE
@app.delete("/api/products/<int:index>")
def delete_product(index):
    print(f"Delete {index}")

    if index >= 0 and index < len(products):
        # deletect_product = products.pop(index)
        # return json.dumps(deletect_product), HTTPStatus.OK
        db.products.delete_one({"_id": products[index]["_id"]})
    else:
        return "Product not found", HTTPStatus.NOT_FOUND
    
# Count the number of products
@app.get("/api/products/count")
def count_products():
    product_count = db.products.count_documents({})
    return json.dumps({"total": product_count}), HTTPStatus.OK

app.run(debug = True)
