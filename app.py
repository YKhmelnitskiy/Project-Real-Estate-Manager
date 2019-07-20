#  Authored by ‘Robert Rua’, ‘Jeremy Halek’, ‘Gaston Alvarado’, 'Erika Haren,  ‘Yevgeniy Khmelnitskiy’
#import necessary libraries
from flask import Flask, request, jsonify, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func #Column, Integer, DateTime
import pusher
from database import db_session
from models import Sales
from datetime import datetime
import os
#Create our app

app = Flask(__name__)

#################
#Creating database
#################

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/RealEstate.sqlite"

db = SQLAlchemy(app)
#I added this from the pusher ###############
pusher_client = pusher.Pusher(
    app_id="824700",
    key="11cb3fcd5df6c3b7e3ba",
    secret="39f07790b821e7a6fc91",
    cluster="us2",
    ssl=True)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
######################end of pusher

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64))
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    area = db.Column(db.Integer)
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))

    # def __init__(self, address, bedrooms, bathrooms, area, city, state):
    #     self.address = address
    #     self.bedrooms = bedrooms
    #     self.bathrooms = bathrooms
    #     self.area = area
    #     self.city = city
    #     self.state = state

    def __repr__(self):
        return '<Table %r>' % (self.address)

class Buyers(db.Model):
    __tablename__ = 'buyers_list'
    field1 = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)
    price = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    agent = db.Column(db.String(64))

    # def __init__(self, name, age, price, date, agent):
    #     self.name = name
    #     self.age = age
    #     self.price = price
    #     self.date = date
    #     self.agent = agent

    def __repr__(self):
        return '<Table %r>' % (self.name)

class Pipeline(db.Model):
    __tablename__ = 'pipeline_list'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64))
    Last_Name = db.Column(db.String(64))
    Zip_Code = db.Column(db.Integer)
    City = db.Column(db.String)
    State = db.Column(db.String(64))
    Email = db.Column(db.String(64))
    Phone_Number = db.Column(db.String(64))
    Company = db.Column(db.String(64))
    Title = db.Column(db.String(64))
    Last_Contact = db.Column(db.DateTime)
    Budget = db.Column(db.Integer)
    Agent = db.Column(db.String(64))
    
    # def __init__(self, Name, Last_Name, Zip_Code, City, State, Email, Phone_Number, Company, Title, Last_Contact, Budget, Agent):
    #     self.First_Name = Name
    #     self.Last_Name = Last_Name
    #     self.Zip_Code = Zip_Code
    #     self.City = City
    #     self.State = State
    #     self.Email = Email
    #     self.Phone_Number = Phone_Number
    #     self.Company = Company
    #     self.Title = Title
    #     self.Last_Contact = Last_Contact
    #     self.Budget = Budget
    #     self.Agent = Agent

    def __repr__(self):
        return '<Table %r>' % (self.First_Name)
        
#############
#Routes     #
#############

@app.before_first_request
def setup():
    db.create_all()
    #recreate database each time for demo
    # db.drop_all
    
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
@app.route("/")
def dashboard():
    """Return to the dashboard."""
    count = db.session.query(func.count(Buyers.field1)).scalar()
    #hi = db.session.query(func.count(Address.id)).scalar()
    
    print (count)
    #print (hi)
    return render_template("index6.html", count=count)

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

@app.route("/calendar")
def calendar():
    """Return to the calendar."""

    return render_template("calendar.html")

@app.route("/chats")
def chats():
    """Return to the chats."""

    return render_template("chats.html")

@app.route("/contact-card")
def contact_card():
    """Return to the contact-card."""

    return render_template("contact-card.html")

@app.route("/contact-list")
def contact_list():
    """Return to the contact-list."""

    return render_template("contact-list.html")

@app.route("/file-manager")
def file_manager():
    """Return to the file-manager."""

    return render_template("file-manager.html")

# @app.route("/form-layout")
# def form_layout():
#     """Return to the form-layout."""

#     return render_template("form-layout.html")

@app.route('/form-layout', methods=["POST", "GET"])
def form_layout():
    if request.method == "POST":
        seller = request.form["seller"]
        buyer = request.form["buyer"]
        sold_price = request.form["sold_price"]
        closing_date= datetime.strptime(request.form['closing_date'], '%d-%m-%Y %H:%M %p')
        Type = request.form["Type"]
        status = request.form["status"]
        address = request.form["address"]
        new_sale = Sales(seller, buyer, sold_price, closing_date, Type, status, address)
        db_session.add(new_sale)
        db_session.commit()

        data = {
            "id": new_sale.id,
            "seller": seller,
            "buyer": buyer,
            "sold_price": sold_price, 
            "closing_date": request.form['closing_date'],
            "Type": Type,
            "status": status, 
            "address": address}
      
        pusher_client.trigger('table', 'new-record', {'data': data })
        return redirect("/form-layout", code=302)
    else:
        sales = Sales.query.all()
        return render_template('form-layout.html', sales=sales)

@app.route('/edit/<int:id>', methods=["POST", "GET"])
def update_record(id):
    if request.method == "POST":
        #sales = request.form["sales"]
        seller = request.form["seller"]
        buyer = request.form["buyer"]
        sold_price = request.form["sold_price"]
        #closing_price = request.form["closing_price"]
        Type = request.form["Type"]
        status = request.form["status"]
        address = request.form["address"]

        update_sales = Sales.query.get(id)
        update_sales.seller = seller
        update_sales.buyer = buyer
        update_sales.sold_price = sold_price
        update_sales.Type = Type
        update_sales.status = status
        update_sales.address = address

        db_session.commit()

        data = {
            "id": id,
            "seller": seller,
            "buyer": buyer,
            "sold_price": sold_price, 
            "closing_date": request.form['closing_date'],
            "Type": Type,
            "status": status, 
            "address": address}

        pusher_client.trigger('table', 'update-record', {'data': data })
       
        return redirect("/form-layout", code=302)
    else:
        new_sale = Sales.query.get(id)
        new_sale.closing_date = new_sale.closing_date.strftime("%d-%m-%Y %H:%M %p")
        #new_sales.departure = new_sales.departure.strftime("%d-%m-%Y %H:%M %p")

        return render_template('edit.html', data=new_sale)

@app.route("/inbox-detail")
def inbox_detail():
    """Return to the inbox-detail."""

    return render_template("inbox-detail.html")

@app.route("/inbox")
def inbox():
    """Return to the inbox."""

    return render_template("inbox.html")

@app.route("/index")
def index():
    """Return to the index."""

    return render_template("index.html")

@app.route("/machinelearning")
def machine_learning():
    """Return to the machinelearning."""

    return render_template("machinelearning.html")

if __name__ == "__main__": 
    app.run()