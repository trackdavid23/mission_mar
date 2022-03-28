# Import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Create new Flask instance
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create main Flask route
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Create new Flask route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_many({}, {"$set":mars_data}, upsert=True) # pymongo 4.0.1
   # mars.update({}, mars_data, upsert=True) # pymongo 3.12.3
   return redirect('/', code=302)
 
# Define main behavior
if __name__ == "__main__":
   app.run()