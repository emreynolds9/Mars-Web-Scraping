import scrape_mars
from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo
import os
import json
from bson import json_util

app = Flask(__name__)

# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

# Create root/index route to query mongoDB and pass mars data to HTML template to display data
@app.route('/')
def index():
    # mars_data = mongo.db.collection.find_one()
    with open('result.json') as json_file:
        test123 = json.load(json_file)
        print(test123)
    return render_template('index.html', mars_data=test123)

# Create route called /scrape
@app.route('/scrape')
def scrape():
    #run the scrape function
    mars_dict = scrape_mars.scrape()

    with open('result.json', 'w') as fp:
        json.dump(mars_dict, fp, default=json_util.default)

    #update the mongo database using update and upsert=True
    # mongo.db.collection.update({}, mars_dict, upsert=True)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
