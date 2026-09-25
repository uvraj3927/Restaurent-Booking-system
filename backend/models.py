from datetime import datetime
from extensions import db

class RestaurantTable(db.Model):
    __tablename__ = 'restaurant_tables'

    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    location_zone = db.Column(db.String(50), nullable=False)

    bookings = db.relationship('Booking', backref='table', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'table_number': self.table_number,
            'capacity': self.capacity,
            'location_zone': self.location_zone
        }


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_inr = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'price_inr': self.price_inr,
            'image_url': self.image_url,
            'is_available': self.is_available
        }


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_reference = db.Column(db.String(20), unique=True, index=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), index=True, nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    guest_count = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='CONFIRMED', nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('restaurant_tables.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'booking_reference': self.booking_reference,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'booking_date': self.booking_date.strftime('%Y-%m-%d'),
            'booking_time': self.booking_time.strftime('%H:%M'),
            'guest_count': self.guest_count,
            'special_requests': self.special_requests or '',
            'status': self.status,
            'table_id': self.table_id,
            'table_number': self.table.table_number if self.table else None,
            'location_zone': self.table.location_zone if self.table else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
