from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///locations.db"
db = SQLAlchemy(app)
GoogleMaps(app, key="AIzaSyBJP7ueb4OId5v5Mh4lzNH2k6zX9v6mcsA")


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data = db.Column(db.String(255), nullable=False)


@app.route("/add_location", methods=["POST"])
def add_location():
    data = request.get_json()
    latitude = data["latitude"]
    longitude = data["longitude"]
    data_str = data["data"]
    date = datetime.utcnow

    location = Location(
        latitude=latitude, longitude=longitude, data=data_str, date_time=date
    )
    db.session.add(location)
    db.session.commit()
    return jsonify({"message": "Location added successfully"})


@app.route("/get_locations", methods=["GET"])
def get_locations():
    locations = Location.query.all()
    location_list = []
    for location in locations:
        location_data = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "date_time": location.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": location.data,
        }
        location_list.append(location_data)
    return jsonify({"locations": location_list})


@app.route("/")
def mapview():
    # creating a map in the view
    mymap = Map(identifier="view-side", lat=30, lng=-8, markers=[(37.4419, -122.1419)])
    people_locations = []
    locations = get_locations["locations"]
    for location in locations:
        people_locations.append(
            {
                "icon": "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
                "lat": location["latitude"],
                "lng": location["longitude"],
                "infobox": location["data"],
            }
        )
    sndmap = Map(
        identifier="sndmap",
        lat=30,
        lng=-8,
        markers=people_locations,
        style="height:1200px;width:1200px;margin: auto;",
        zoom=5,
    )
    return render_template("example.html", mymap=mymap, sndmap=sndmap)


def Marker(latitude, longitude, info):
    return {
        "icon": "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
        "lat": latitude,
        "lng": longitude,
        "infobox": "<b>" + info + "</b>",
    }


if __name__ == "__main__":
    app.run(debug=True)
