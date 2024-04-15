#!/usr/bin/env python3

from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def home():
    return '<h1>Code Challenge</h1>'

class Vendors(Resource):
    def get(self):
        vendors = [
            {"id":vendor.id, "name":vendor.name} for vendor in Vendor.query.all() 
            ]
        response = make_response( vendors,200)
        return response
    
class VendorsById(Resource):
    def get(self,id):
        vendor = Vendor.query.filter(Vendor.id == id).first()
        if not vendor:
            response = make_response({"error": "Vendor not found"}, 404)
            return response
        response = make_response(vendor.to_dict(), 200)
        return response


class Sweets(Resource):
    def get(self):
        sweets = [sweet.to_dict() for sweet in Sweet.query.all()]
        response = make_response(sweets, 200)
        return response


class SweetsById(Resource):
    def get(self, id):
        sweet = Sweet.query.filter(Sweet.id == id).first()
        if not sweet:
            response = make_response({"error": "Sweet not found"}, 404)
            return  response
        response = make_response(sweet.to_dict(), 200)
        return response


class VendorSweets(Resource):
    def post(self):
        data = request.get_json()

        price = data.get('price')
        vendor_id = data.get('vendor_id')
        sweet_id = data.get('sweet_id')

        if price is None or vendor_id is None or sweet_id is None:
            return {"errors": ["validation errors"]}, 404

        vendor_sweet = VendorSweet(
            price=price, vendor_id=vendor_id, sweet_id=sweet_id)

        db.session.add(vendor_sweet)
        db.session.commit()
        return vendor_sweet.to_dict(), 201


class VendorSweetsyId(Resource):
    def delete(self, id):
        vendors_sweet = VendorSweet.query.filter_by(id=id).first()
        if not vendors_sweet:
            return {"error": "VendorSweet not found"}, 400
        db.session.delete(vendors_sweet)
        db.session.commit()
        return {}, 204



api.add_resource(Vendors, "/vendors")
api.add_resource(Sweets, "/sweets")
api.add_resource(VendorSweets, "/vendor_sweets")
api.add_resource(VendorsById, "/vendors/<int:id>")
api.add_resource(SweetsById, "/sweets/<int:id>")
api.add_resource(VendorSweetsyId, "/ vendor_sweets/<int: id >")

        


            
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
