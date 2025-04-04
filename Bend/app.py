import os
import logging
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from routes.card_routes import init_routes
import secrets

def create_app():
    """Crează și configurează aplicația Flask"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, 
         resources={r"/api/*": {"origins": ["http://localhost:5173"]}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Configure CSP headers
    @app.after_request
    def add_security_headers(response):
        # Add CORS headers to every response
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        # Add CSP headers
        csp_directives = [
            "default-src 'self' http://localhost:5173 http://localhost:5000",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' http://localhost:5173",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data:",
            "font-src 'self' data:",
            "connect-src 'self' http://localhost:5000 http://localhost:5173",
            "frame-ancestors 'none'",
            "form-action 'self'",
            "base-uri 'self'"
        ]
        
        response.headers['Content-Security-Policy'] = "; ".join(csp_directives)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        return response

    # Load configuration
    app.config.from_object(Config)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Rută de test pentru baza de date
    @app.route('/api/db-test', methods=['GET'])
    def test_db():
        try:
            conn = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                dbname=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            conn.close()
            return jsonify({"status": "Database connection successful"}), 200
        except Exception as e:
            app.logger.error(f"Database connection error: {str(e)}")
            return jsonify({"error": "Database connection failed", "details": str(e)}), 500
    
    # Initialize routes
    try:
        init_routes(app)
    except Exception as e:
        app.logger.error(f"Error initializing routes: {str(e)}")
        raise
    
    # Error handler for 400 errors
    @app.errorhandler(400)
    def handle_400_error(error):
        app.logger.error(f"Bad request error: {str(error)}")
        return jsonify({
            "error": "Bad Request",
            "message": str(error)
        }), 400
    
    # Error handler for 500 errors
    @app.errorhandler(500)
    def handle_500_error(error):
        app.logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(error)
        }), 500
    
    # Rută de test/sănătate
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "ok"}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)