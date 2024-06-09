from flask import Flask
from utils import factorial1, factorial2
import json

app = Flask(__name__)
CACHE_LOADED = False

def save(filename, cache):
  with open(filename, "w") as f:
    json.dump(cache, f)

def load(filename):
    with open(filename, "r") as f:
      return json.load(f)

@app.route("/")
def home():
    return "<p>Yo!</p>"

@app.route("/info")
def about_author():
    return "<p>Author: Amira Zouhir 1.2</p>"

@app.route("/calculate/<string:func>/<int:number>")
def compute_factorial(func, number):
    global CACHE_LOADED
    if number < 0:
        return "Factorial is not defined for negative numbers!!!!", 400
    if func == 'f1':
        result = str(factorial1(number))
        return f'Factorial of {number} is {result}'
    elif func == 'f2':
        result = str(factorial2(number))
        return f'Factorial of {number} is {result}'
    else:
        return "Invalid function name", 400

@app.route("/load_cache")
def load_cache():
    global CACHE_LOADED
    CACHE_LOADED = True
    cache_data = load('cache.json')
    factorial1.cache = cache_data
    factorial2.cache = cache_data
    return f'Cache loaded: {cache_data}'

@app.route("/save_cache")
def save_cache():
    global CACHE_LOADED
    if not CACHE_LOADED:
        load_cache()
    cache_data = {**factorial1.cache, **factorial2.cache}
    save('cache.json', cache_data)
    return f'Cache saved: {cache_data}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
