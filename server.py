from flask import Flask, request
from http import HTTPStatus
import json

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

products = []

# GET
@app.get("/api/products")
def get_products():
    return json.dumps(products), HTTPStatus.OK

# POST
@app.post("/api/products")
def save_product():
    product = request.get_json()
    print(f"product {product}")
    products.append(product)
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
        deletect_product = products.pop(index)
        return json.dumps(deletect_product), HTTPStatus.OK
    else:
        return "Product not found", HTTPStatus.NOT_FOUND

app.run(debug = True)
