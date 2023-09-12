from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from flask_googlemaps import GoogleMaps
#from flask_googlemaps import Map
import pandas as pd 
import folium
from folium import plugins

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///locations.db"
db = SQLAlchemy(app)



class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255),nullable=False)


@app.route("/add_location", methods=["POST"])
def add_location():
    data = request.form
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    data_str = data.get("data")
    phone_number=data.get('phone_number')
    date = datetime.now()

    location = Location(
        # id=(date - datetime(1970, 1, 1)).total_seconds(),
        latitude=latitude,
        longitude=longitude,
        data=data_str,
        date_time=date,
        phone_number =phone_number
    )
    db.session.add(location)
    db.session.commit()
    return mapview()


#@app.route("/get_locations", methods=["GET"])
def get_locations():
    locations = Location.query.all()
    location_list = []
    for location in locations:
        location_data = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "date_time": location.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": location.data,
            "phone_number":location.phone_number
        }
        location_list.append(location_data)
    return location_list


@app.route("/")
def mapview():
    m = folium.Map(
    location=[31.228674, -7.992047],
    zoom_start=8.5,
    min_zoom=8.5,
    max_lat=35.628674,
    min_lat=29.628674,
    max_lon=-4.992047,
    min_lon=-10.992047,
    max_bounds=True,
)
    plugins.Geocoder(
    collapsed=False,
    position="topright",
    placeholder="Search | البحث",
    ).add_to(m)


    plugins.Fullscreen(
    position='topright',
    title='Expand me | تكبير الخريطة',
    title_cancel='Exit me | تصغير الخريطة',
    force_separate_button=True
    ).add_to(m)
    tileurl = 'https://api.mapbox.com/styles/v1/phd2020/clmer2mra01d001pbgjkictpt/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoicGhkMjAyMCIsImEiOiJja29lZzFwZmUwNHkzMm5wMjZnYjVvcGltIn0.tE0ritrelQOyLdKUH6hgOw'

    folium.TileLayer(
        tiles = tileurl,
        attr = 'Satellite View',
        name = 'Satellite View | عرض القمر الصناعي',
        overlay = False,
        control = True
       ).add_to(m)
    folium.LayerControl().add_to(m)


    # creating a map in the view
    #mymap = Map(identifier="view-side", lat=30, lng=-8, markers=[(37.4419, -122.1419)])

    locations = get_locations()
    # for location in locations:
    #     people_locations.append(Marker_user(location['latitude'],location['longitude'],location['data'],
    #                                    location['phone_number']))
    douars_locations = pd.read_csv('Douars_50km.csv')
    for i in range(len(douars_locations)):
        folium.Marker(
        location=[douars_locations.iloc[i]['Y'], douars_locations.iloc[i]['X']],
        popup=douars_locations.iloc[i]['Name'],
         icon= folium.Icon(color='red')
        ).add_to(m)
    for location in locations:
        folium.Marker(
        location=[location['latitude'], location['longitude']],
        popup=(location['data']+"</b>"+"<p> Phone number: "+location['phone_number']+"</p>"),
        icon= folium.Icon(color='blue')
        ).add_to(m)

        
    return render_template("example.html",map=m._repr_html_())


@app.route("/add_location_form", methods=["GET"])
def add_location_form():
    return render_template("add_location_form.html")
@app.route("/manuel_filling",methods = ["GET"])
def manuel_filling():
    return render_template("manuel.html")
@app.route("/about")
def about():
    return render_template("about.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
