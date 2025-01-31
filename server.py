from flask import Flask, render_template, request
from http import HTTPStatus
import json
from config import db

app = Flask(__name__)

@app.get("/")
def home():
    return "Hello from flask"

# @app.post("/")
# @app.put("/")
# @app.patch("/")
# @app.delete("/")
# if I don't have some method, than means that method is not valid

@app.get("/test")
def test():
    return "This is another endpoint", 200

# This is a JSON implementation
@app.get("/api/about")
def about():
    name = {
        "name" : "Chris",
        "last_name" : "Bonilla"
    }
    return json.dumps(name), HTTPStatus.OK

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

app.run(debug = True)
