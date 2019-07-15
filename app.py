#  Authored by ‘Robert Rua’, ‘Jeremy Halek’, ‘Gaston Alvarado’, 'Erika Haren,  ‘Yevgeniy Khmelnitskiy’
#import necessary libraries
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#Create our app

app = Flask(__name__)

#################
#Creating database
#################

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/RealEstate.sqlite"

db = SQLAlchemy(app)

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64))
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    area = db.Column(db.Integer)
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))

    def __init__(self, address, bedrooms, bathrooms, area, city, state):
        self.address = address
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.area = area
        self.city = city
        self.state = state

    def __repr__(self):
        return '<Address %r>' % (self.address)
    

#############
#Routes     #
#############

@app.before_first_request
def setup():
    #recreate database each time for demo
    db.drop_all
    
#@app.route("/Landing_Page")
#def landing_page():
#   """Return to the landing page."""
#   
#    return render_template("landing_page.html")  

#@app.route("/Dashboard")
#def dashboard():
#    """Return to the dashboard."""
#   
#    return render_template("dashboard.html") 

@app.route("/Registration", methods = ["GET", "POST"])
def registration():
    
    if request.method == "POST":
        address = request.form["address"]
        bedrooms = request.form["bedrooms"]
        bathrooms = request.form["bathrooms"]
        area = request.form["area"] #sqaure footage
        city = request.form["city"]
        state = request.form["state"]

        Listing = Address(address=address, bedrooms=bedrooms, bathrooms=bathrooms, area=area, city=city, state=state)
        
        db.session.add(Listing)
        db.session.commit()

        return "Thanks for the form data!"

    return render_template("registration.html")

@app.route('/api/data')
def list_addresses():
    results = db.session.query(Address.address, Address.bedrooms, Address.bathrooms, Address.area, Address.city, Address.state).all()

    homes = []
    for result in results:
        homes.append({
            "address": result[0],
            "bedrooms": result[1],
            "bathrooms": result[2],
            "area": result[3],
            "city": result[4],
            "state": result[5]
        })
    return jsonify(homes)

if __name__ == "__main__":
    db.create_all()
    app.run()