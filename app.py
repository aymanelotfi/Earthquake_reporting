from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
GoogleMaps(app,key="AIzaSyBJP7ueb4OId5v5Mh4lzNH2k6zX9v6mcsA")
markers = []
@app.route("/")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=30,
        lng=-8,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=30,
        lng=-8,
        markers=[
         Marker(31.2426931303958, -7.985738870163966,"Please Help me  !"),
         Marker(30.2426931303958, -8.985738870163966,"Please Help me !"),
         Marker(33.2426931303958, -7.985738870163966,"Please Help me ! Call me at xx"),
        ],
        style="height:1200px;width:1200px;margin: auto;",
        zoom = 5
    )
    return render_template('example.html', mymap=mymap, sndmap=sndmap)
def Marker(latitude,longitude,info):
    return        {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
             'lat': latitude,
             'lng': longitude,
             'infobox': "<b>"+info+"</b>"
          }
if __name__ == "__main__":
    app.run(debug=True)
