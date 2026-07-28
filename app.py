from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from config import Config
from extensions import db, migrate, cors, jwt, bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from resources.Auth import auth_bp
    from resources.User import user_bp
    from resources.Property import property_bp
    from resources.Booking import booking_bp
    from resources.Payment import payment_bp
    from resources.Review import review_bp
    from resources.Amenities import amenities_bp
    from resources.Favourite import favourite_bp
    from resources.Maintenance import maintenance_bp
    from resources.Propertyimage import property_image_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(property_bp, url_prefix="/api/properties")
    app.register_blueprint(booking_bp, url_prefix="/api/bookings")
    app.register_blueprint(payment_bp, url_prefix="/api/payments")
    app.register_blueprint(review_bp, url_prefix="/api/reviews")
    app.register_blueprint(amenities_bp, url_prefix="/api/amenities")
    app.register_blueprint(favourite_bp, url_prefix="/api/favourites")
    app.register_blueprint(maintenance_bp, url_prefix="/api/maintenance")
    app.register_blueprint(property_image_bp, url_prefix="/api/property-images")

    return app


app = create_app()