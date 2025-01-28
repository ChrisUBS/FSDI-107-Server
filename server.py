from flask import Flask
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
    return "This is another endpoint"

# This is a JSON implementation
@app.get("/api/about")
def about():
    name = {
        "name" : "Chris",
        "last_name" : "Bonilla"
    }
    return json.dumps(name)

app.run(debug = True)
