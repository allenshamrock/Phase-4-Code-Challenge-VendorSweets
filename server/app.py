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
        if vendor:
            response  = make_response(vendor.to_dict(),200)
            return response
        response = make_response({"error": "Vendor not found"}, 404)
        return response
    

        


            
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
