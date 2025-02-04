from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_mom():
    return "<p>Hello mom!</p>"

# import h3



# lat, lng = 37.769377, -122.388903
# resolution = 9
# h3.latlng_to_cell(lat, lng, resolution)