from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    vendorsweet = db.relationship(
        'VendorSweet', back_populates='sweet', cascade="all, delete-orphan")
    vendors = association_proxy(
        'vendor_sweets', 'vendor', creator=lambda vendor_obj: VendorSweet(vendor=vendor_obj))
    
    # Add serialization
    serialize_only = ('id', 'name')
    
    def __repr__(self):
        return f'<Sweet {self.id}>'


class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    vendorsweet = db.relationship(
        'VendorSweet', back_populates='vendor', cascade="all, delete-orphan")
    sweets = association_proxy(
        'vendor_sweets', 'sweet', creator=lambda sweet_obj: VendorSweet(sweet=sweet_obj))
    
    # Add serialization
    serialize_only=('id','name')
    
    def __repr__(self):
        return f'<Vendor {self.id}>'


class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    

    # Add relationships
    sweet = db.relationship('Sweet', back_populates = 'vendorsweet')
    vendor = db.relationship('Vendor', back_populates = 'vendorsweet')
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    
    # Add serialization
    serialize_rules = ('-sweet.vendorsweet', '-vendor.vendorsweet')
    
    # Add validation
    @validates('price')
    def validate_price(self,key,price):
        if price is None:
            raise ValueError('Prie must have a value')
        if price < 0 :
            raise ValueError('Price cannot be a negative number')
        return price


    
    def __repr__(self):
        return f'<VendorSweet {self.id}>'
