import random
import string
from datetime import datetime, date, time, timedelta
from flask import Blueprint, request, jsonify
from extensions import db
from models import MenuItem, RestaurantTable, Booking
from config import Config

api_bp = Blueprint('api', __name__, url_prefix='/api')

def generate_booking_reference():
    """Generates a unique reference code like PG-8A3X91."""
    while True:
        code = 'PG-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        existing = Booking.query.filter_by(booking_reference=code).first()
        if not existing:
            return code

def parse_time_str(time_str):
    """Parses 'HH:MM' string to datetime.time object."""
    try:
        return datetime.strptime(time_str.strip(), '%H:%M').time()
    except (ValueError, AttributeError):
        return None

def parse_date_str(date_str):
    """Parses 'YYYY-MM-DD' string to datetime.date object."""
    try:
        return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
    except (ValueError, AttributeError):
        return None

def is_within_operating_hours(booking_time):
    """Checks if requested booking time is within operating hours (12:00 - 23:00)."""
    open_time = parse_time_str(Config.OPENING_TIME)
    close_time = parse_time_str(Config.CLOSING_TIME)
    
    # Last acceptable reservation time is 90 mins before closing (e.g., 21:30)
    last_booking = (datetime.combine(date.today(), close_time) - timedelta(minutes=Config.SLOT_DURATION_MINUTES)).time()
    return open_time <= booking_time <= last_booking

def has_time_overlap(time1, time2, duration_minutes=90):
    """Returns True if time1 and time2 overlap within slot duration."""
    t1_mins = time1.hour * 60 + time1.minute
    t2_mins = time2.hour * 60 + time2.minute
    return abs(t1_mins - t2_mins) < duration_minutes

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Application health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'Pyrites Grill REST API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@api_bp.route('/restaurants', methods=['GET'])
def get_restaurant_info():
    """Returns restaurant profile, operating hours, and location zones."""
    return jsonify({
        'name': Config.RESTAURANT_NAME,
        'cuisine': 'Modern Grill, Steaks & Smoked BBQ',
        'address': '742 Ember Ridge Boulevard, Culinary District',
        'phone': '+91 98765 43210',
        'email': 'reservations@pyritesgrill.com',
        'opening_time': Config.OPENING_TIME,
        'closing_time': Config.CLOSING_TIME,
        'slot_duration_minutes': Config.SLOT_DURATION_MINUTES,
        'max_guests_per_booking': Config.MAX_GUESTS_PER_BOOKING,
        'location_zones': ['Patio Terrace', 'Main Dining Room', 'Window Lounge', 'Private Alcove', 'Chef\'s Table VIP']
    }), 200

@api_bp.route('/menu', methods=['GET'])
def get_menu():
    """Retrieve menu items optional filter by category."""
    category = request.args.get('category')
    query = MenuItem.query.filter_by(is_available=True)
    
    if category:
        query = query.filter(MenuItem.category.ilike(category))
        
    items = query.all()
    return jsonify({
        'count': len(items),
        'items': [item.to_dict() for item in items]
    }), 200

@api_bp.route('/availability', methods=['GET'])
def check_availability():
    """Checks booking availability for a date, time, and guest count."""
    date_str = request.args.get('date')
    time_str = request.args.get('time')
    guests_param = request.args.get('guests')

    if not date_str or not time_str or not guests_param:
        return jsonify({'error': 'Missing required params: date (YYYY-MM-DD), time (HH:MM), guests'}), 400

    b_date = parse_date_str(date_str)
    b_time = parse_time_str(time_str)
    
    try:
        guest_count = int(guests_param)
    except ValueError:
        return jsonify({'error': 'guests parameter must be a valid integer'}), 400

    if not b_date or not b_time:
        return jsonify({'error': 'Invalid date format (YYYY-MM-DD) or time format (HH:MM)'}), 400

    if b_date < date.today():
        return jsonify({'error': 'Booking date cannot be in the past'}), 400

    if guest_count < 1 or guest_count > Config.MAX_GUESTS_PER_BOOKING:
        return jsonify({'error': f'Guest count must be between 1 and {Config.MAX_GUESTS_PER_BOOKING}'}), 400

    if not is_within_operating_hours(b_time):
        return jsonify({'error': f'Booking time must be between {Config.OPENING_TIME} and 21:30'}), 400

    # Query candidate tables that fit guest count
    suitable_tables = RestaurantTable.query.filter(RestaurantTable.capacity >= guest_count).all()
    
    if not suitable_tables:
        return jsonify({
            'available': False,
            'message': 'No single table can accommodate this party size. Please contact us for group events.',
            'available_tables_count': 0
        }), 200

    # Fetch existing confirmed bookings for that date
    existing_bookings = Booking.query.filter(
        Booking.booking_date == b_date,
        Booking.status == 'CONFIRMED'
    ).all()

    # Find free tables
    free_tables = []
    for table in suitable_tables:
        # Check if table has an overlapping booking
        table_bookings = [b for b in existing_bookings if b.table_id == table.id]
        is_booked = any(has_time_overlap(b_time, b.booking_time, Config.SLOT_DURATION_MINUTES) for b in table_bookings)
        if not is_booked:
            free_tables.append(table)

    is_available = len(free_tables) > 0
    return jsonify({
        'available': is_available,
        'date': b_date.strftime('%Y-%m-%d'),
        'time': b_time.strftime('%H:%M'),
        'guests': guest_count,
        'available_tables_count': len(free_tables),
        'message': 'Table available! You can proceed with booking.' if is_available else 'Selected time slot is fully booked. Please select another time.'
    }), 200

@api_bp.route('/bookings', methods=['POST'])
def create_booking():
    """Creates a table reservation with double-booking prevention & concurrency lock."""
    data = request.get_json() or {}
    
    customer_name = data.get('customer_name', '').strip()
    customer_email = data.get('customer_email', '').strip().lower()
    customer_phone = data.get('customer_phone', '').strip()
    date_str = data.get('booking_date')
    time_str = data.get('booking_time')
    guest_count = data.get('guest_count')
    special_requests = data.get('special_requests', '').strip()

    # Validate required inputs
    if not customer_name or not customer_email or not customer_phone or not date_str or not time_str or not guest_count:
        return jsonify({'error': 'Missing required fields: customer_name, customer_email, customer_phone, booking_date, booking_time, guest_count'}), 400

    if '@' not in customer_email or '.' not in customer_email:
        return jsonify({'error': 'Invalid customer email address'}), 400

    b_date = parse_date_str(date_str)
    b_time = parse_time_str(time_str)

    try:
        guest_count = int(guest_count)
    except (ValueError, TypeError):
        return jsonify({'error': 'guest_count must be a positive integer'}), 400

    if not b_date or not b_time:
        return jsonify({'error': 'Invalid date format (YYYY-MM-DD) or time format (HH:MM)'}), 400

    if b_date < date.today():
        return jsonify({'error': 'Booking date cannot be in the past'}), 400

    if guest_count < 1 or guest_count > Config.MAX_GUESTS_PER_BOOKING:
        return jsonify({'error': f'Guest count must be between 1 and {Config.MAX_GUESTS_PER_BOOKING}'}), 400

    if not is_within_operating_hours(b_time):
        return jsonify({'error': f'Booking time must be between {Config.OPENING_TIME} and 21:30'}), 400

    try:
        # Atomic transaction with row locking on candidate tables to handle concurrency
        # 1. Fetch tables with capacity >= guest_count, ordered by capacity ASC
        candidate_tables = RestaurantTable.query.filter(
            RestaurantTable.capacity >= guest_count
        ).order_by(RestaurantTable.capacity.asc()).with_for_update().all()

        if not candidate_tables:
            return jsonify({'error': 'No tables available for this party size'}), 400

        # 2. Get existing bookings for the date with row locking
        existing_bookings = Booking.query.filter(
            Booking.booking_date == b_date,
            Booking.status == 'CONFIRMED'
        ).with_for_update().all()

        assigned_table = None
        for table in candidate_tables:
            table_bookings = [b for b in existing_bookings if b.table_id == table.id]
            is_booked = any(has_time_overlap(b_time, b.booking_time, Config.SLOT_DURATION_MINUTES) for b in table_bookings)
            if not is_booked:
                assigned_table = table
                break

        if not assigned_table:
            return jsonify({
                'error': 'Table double-booking prevented. The selected time slot was just taken by another guest. Please choose a different time.'
            }), 409  # 409 Conflict

        # 3. Create booking record
        ref = generate_booking_reference()
        new_booking = Booking(
            booking_reference=ref,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            booking_date=b_date,
            booking_time=b_time,
            guest_count=guest_count,
            special_requests=special_requests,
            status='CONFIRMED',
            table_id=assigned_table.id
        )

        db.session.add(new_booking)
        db.session.commit()

        return jsonify({
            'message': 'Booking confirmed successfully!',
            'booking': new_booking.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to complete reservation due to a database error', 'details': str(e)}), 500


@api_bp.route('/bookings/<reference>', methods=['GET'])
def get_booking_by_reference(reference):
    """Retrieve booking by reference and email verification."""
    email = request.args.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'error': 'Email query parameter is required for security verification'}), 400

    booking = Booking.query.filter_by(booking_reference=reference.upper()).first()

    if not booking or booking.customer_email.lower() != email:
        return jsonify({'error': 'Booking not found or email verification failed'}), 404

    return jsonify({'booking': booking.to_dict()}), 200


@api_bp.route('/bookings/<reference>/cancel', methods=['POST'])
def cancel_booking(reference):
    """Cancel a booking securely with email verification."""
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'error': 'Email is required to confirm cancellation'}), 400

    booking = Booking.query.filter_by(booking_reference=reference.upper()).first()

    if not booking or booking.customer_email.lower() != email:
        return jsonify({'error': 'Booking not found or email verification failed'}), 404

    if booking.status == 'CANCELLED':
        return jsonify({'message': 'Booking is already cancelled', 'booking': booking.to_dict()}), 200

    booking.status = 'CANCELLED'
    db.session.commit()

    return jsonify({
        'message': 'Booking has been successfully cancelled.',
        'booking': booking.to_dict()
    }), 200
