# Import dependencires MongoDB and Flask
from flask import Flask, render_template, url_for, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scraping

# Create flask object
app = Flask(__name__)

#Configure flask framework to mongo DB mars_app db
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# top-level hierarchy url registration
@app.route('/')
def index():
    # instantiate collection object in DB and get data
    mars = mongo.db.mars.find_one()
    # mars = mars.find()
    return render_template("index.html", mars=mars)

# Next page 
@app.route('/scrape')
def scrape():
    # instantiate collection object in DB 
    mars = mongo.db.mars
    # call scrape_all function and store results
    mars_data = scraping.scrape_all()
    # update collection without matching
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

# check if script is running at top hierarchy
if __name__ == "__main__":
    app.run(debug=True)