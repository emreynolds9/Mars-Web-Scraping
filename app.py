import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Create flask app
app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

# Create root/index route to query mongoDB and pass mars data to HTML template to display data
@app.route('/')
def index():
    mars_data = mongo.db.collection.find_one()
    return render_template('index.html', mars_data=mars_data)

if __name__ == '__main__':
    app.run(debug=True)

# Create route called /scrape
@app.route('/scrape')
def scrape():
    #run the scrape function
    mars_dict = scrape_mars.scrape()

    #update the mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_dict, upsert=True)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
