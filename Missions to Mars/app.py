from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.mission_to_mars

@app.route("/")
def index():
    mars_data = list(db.collection.find())[0]
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
    db.collection.remove({})
    mars_data = scraped_data.scrape()
    db.collection.insert_one(mars_data)
    return render_template("scraped_data.html")



if __name__ == "__main__":
    app.run(debug=True)