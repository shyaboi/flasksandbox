from flask import Flask, request,jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os



app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Database SQL
app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "db.sqlite")
app.config['SQLAlchemy_TRACK_MODIFICATION'] = False

#init db
db = SQLAlchemy(app)

#init ma
ma = Marshmallow(app)

class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), unique=True)
    desc=db.Column(db.String(200))
    price=db.Column(db.Float)
    qty=db.Column(db.Integer)

    def __init__(self, name, desc, price, qty):
        self.name = name
        self.desc = desc
        self.price = price
        self.qty = qty


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'desc', 'price', 'qty')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route("/product", methods=["POST"])
def add_product():
    name=request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty=request.json["qty"]

    new_product = Product(name,desc,price,qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/json")
def json():
    return jsonify({'honk':"honk"})


@app.route("/features")
def features():
   return render_template('features.html')

@app.route("/usage")
def usage():
   return render_template('usage.html')

if __name__=="__main__":
    app.run(debug=True)