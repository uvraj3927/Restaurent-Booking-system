import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import Config
from extensions import db
from models import RestaurantTable, MenuItem, Booking
from routes.api import api_bp
from routes.admin import admin_bp
from seeds import seed_database

def create_app():
    # Set relative static folder to point to frontend directory
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
    
    app.config.from_object(Config)

    # Enable CORS for the REST API endpoints
    allowed_origins = [
        "http://restaurant-booking-frontend-868ca2b4.s3-website-us-east-1.amazonaws.com",
        "http://44.200.253.83:5000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
    ]
    frontend_origin = os.getenv("FRONTEND_URL")
    if frontend_origin:
        allowed_origins.append(frontend_origin.rstrip("/"))
    CORS(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-API-Key"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )
    # Initialize extensions
    db.init_app(app)

    # Register API blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    # Serve static frontend pages
    @app.route('/')
    def serve_index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.exists(os.path.join(frontend_dir, path)):
            return send_from_directory(frontend_dir, path)
        return send_from_directory(frontend_dir, 'index.html')

    # Custom 404 handler for API routes
    @app.errorhandler(404)
    def not_found(e):
        if request_is_api():
            return jsonify({'error': 'Endpoint not found'}), 404
        return send_from_directory(frontend_dir, 'index.html')

    def request_is_api():
        from flask import request
        return request.path.startswith('/api/')

    # Automatically create tables and seed initial data
    with app.app_context():
        try:
            db.create_all()
            seed_database()
        except Exception as e:
            print(f"Warning: DB initialization encountered an error: {e}")

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
