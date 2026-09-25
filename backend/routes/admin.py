from functools import wraps
from flask import Blueprint, request, jsonify
from extensions import db
from models import Booking, MenuItem
from config import Config

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def require_admin_key(f):
    """Decorator to enforce API key security header for administrative actions."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != Config.ADMIN_API_KEY:
            return jsonify({'error': 'Unauthorized access: Invalid or missing X-API-Key header'}), 401
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/bookings', methods=['GET'])
@require_admin_key
def get_all_bookings():
    """Admin endpoint to retrieve all bookings with status and date filters."""
    status = request.args.get('status')
    date_str = request.args.get('date')

    query = Booking.query.order_by(Booking.created_at.desc())

    if status:
        query = query.filter(Booking.status == status.upper())
    if date_str:
        query = query.filter(Booking.booking_date == date_str)

    bookings = query.all()
    return jsonify({
        'total': len(bookings),
        'bookings': [b.to_dict() for b in bookings]
    }), 200

@admin_bp.route('/menu', methods=['POST'])
@require_admin_key
def add_menu_item():
    """Admin endpoint to add a new item to the Pyrites Grill menu."""
    data = request.get_json() or {}

    name = data.get('name', '').strip()
    category = data.get('category', '').strip()
    description = data.get('description', '').strip()
    price_inr = data.get('price_inr')
    image_url = data.get('image_url', '').strip()

    if not name or not category or not description or price_inr is None or not image_url:
        return jsonify({'error': 'Missing required fields: name, category, description, price_inr, image_url'}), 400

    try:
        price_inr = int(price_inr)
    except ValueError:
        return jsonify({'error': 'price_inr must be a valid integer'}), 400

    new_item = MenuItem(
        name=name,
        category=category,
        description=description,
        price_inr=price_inr,
        image_url=image_url,
        is_available=data.get('is_available', True)
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        'message': 'Menu item created successfully!',
        'menu_item': new_item.to_dict()
    }), 201
