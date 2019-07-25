#  Authored by ‘Robert Rua’, ‘Jeremy Halek’, ‘Gaston Alvarado’, 'Erika Haren,  ‘Yevgeniy Khmelnitskiy’
#import necessary libraries
from flask import Flask, request, jsonify, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func #Column, Integer, DateTime
from sqlalchemy.sql import func
import pusher
from database import db_session
from models import Sales
from datetime import datetime
import os
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import pandas as pd
#Create our app

model = pickle.load(open('model.pkl','rb'))

app = Flask(__name__)



#I added this from the pusher ###############
pusher_client = pusher.Pusher(
    app_id="824705",
    key="71fa2dc10281921e8d02",
    secret="65ef961a2937ca58c0f0",
    cluster="us2",
    ssl=True)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
######################end of pusher

        
#############
#Routes     #
#############

@app.route("/")
def dashboard():
    """Return to the dashboard."""
    # count = db.session.query(func.count(Buyers.field1)).scalar()
    #hi = db.session.query(func.count(Address.id)).scalar()
    count = Sales.query.count()
    print (count)
    # return render_template("index6.html", count=count)
    return render_template("index6.html",count=count)

# @app.route("/Registration", methods = ["GET", "POST"])
# def registration():
    
#     if request.method == "POST":
#         address = request.form["address"]
#         bedrooms = request.form["bedrooms"]
#         bathrooms = request.form["bathrooms"]
#         area = request.form["area"] #sqaure footage
#         city = request.form["city"]
#         state = request.form["state"]

#         Listing = Address(address=address, bedrooms=bedrooms, bathrooms=bathrooms, area=area, city=city, state=state)
        
#         db.session.add(Listing)
#         db.session.commit()

#         return "Thanks for the form data!"

#     return render_template("registration.html")

# @app.route('/api/data')
# def list_addresses():
#     results = db.session.query(Sales(seller, buyer, sold_price, closing_date, Type, status, address)).all()

#     homes = []
#     for result in results:
#         homes.append({
#             "seller": result[0],
#             "buyer": result[1],
#             "sold price": result[2],
#             "closing date": result[3],
#             "Type": result[4],
#             "status": result[5],
#             "address": result[6]
#         })
#     return jsonify(homes)

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
    # for the span tags
    total_customers = Sales.query.count()
    total_buyers = Sales.query.filter_by(Type="Buyer").count()
    total_sellers = Sales.query.filter_by(Type="Seller").count()
    active_properties = Sales.query.filter_by(status="Active").count()
    pending_properties = Sales.query.filter_by(status="Pending").count()
    price1 = db_session.query(func.sum(Sales.sold_price))
    total = price1[0][0]
    commissions = round((total * .03),2)
    taxes = round((total *.4),2)
    #total_sellers = Sales.query.filter_by(Type="Seller").count()
    #active_properties = Sales.query.filter_by(status="Active").count()
    #pending_properties = Sales.query.filter_by(status="Pending").count()
    # 3% of saleprice
    # print (total_price)
    # taxes are 30% of total gros sales
    info = {
        "total_customers": total_customers,
        "total_buyers": total_buyers,
        "total_sellers": total_sellers,
        "active_properties": active_properties,
        "pending_properties": pending_properties,
        "commissions": commissions,
        "taxes": taxes
    }
    # for the table
    sales = Sales.query.all()
    return render_template("index.html", info = info, sales = sales)

@app.route("/machinelearning", methods = ["GET", "POST"])
def machine_learning():
    """Return to the machinelearning."""
    
    if request.method == "POST":
        medhousing = request.form["medhousing"]
        bedrooms = request.form["bedrooms"]
        bathrooms = request.form["bathrooms"]
        yearbuilt = request.form["yearbuilt"] #sqaure footage
        acres = request.form["acres"]
        graduates = request.form["graduates"]
        foodstamps = request.form["foodstamps"]

        inputs=[]

        inputs.append(medhousing)
        inputs.append(bedrooms)
        inputs.append(bathrooms)
        inputs.append(yearbuilt)
        inputs.append(acres)
        inputs.append(graduates)
        inputs.append(foodstamps)

        inputs2=list(map(float, inputs))

        print(inputs2)

        X1 = np.array(inputs2)
        X=X1.reshape(1, -1)
        prediction= model.predict(X)
        print(prediction)
        output = prediction[0]
        output5=output[0]
        output6=int(output5)
        output2= "{:,}".format(output6)
        print(output2)
    
        return render_template("machinelearning.html", output2=output2)  

    return render_template("machinelearning.html", output2="0")    

if __name__ == "__main__": 
    app.run()