# Property Rental Backend

A Flask-based REST API for a property rental platform. The backend supports property listing, booking management, user profiles, reviews, and amenity handling for guests, hosts, and administrators.

## Features

- User accounts with role-based access for guests, hosts, and admins
- Property creation, updates, deletion, and filtering
- Booking creation, status updates, and access control
- Property reviews and ratings
- Amenity management and association with properties
- JWT-based authentication for protected routes

## Tech Stack

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Flask-CORS
- Python-dotenv
- SQLite (default local database)

## Project Structure

- app.py: creates the Flask app and initializes the database and migrations
- models.py: SQLAlchemy models for users, properties, bookings, reviews, payments, and amenities
- routes/: API blueprints for users, properties, bookings, reviews, and amenities
- instance/: local database storage
- migrations/: database migration files

## Getting Started

1. Clone the repository and navigate into the project folder.
2. Install dependencies:

   ```bash
   pipenv install
   ```

3. Activate the virtual environment:

   ```bash
   pipenv shell
   ```

4. Create or update the database:

   ```bash
   flask db upgrade
   ```

   If you are starting from scratch and need migrations:

   ```bash
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade
   ```

5. Start the development server:

   ```bash
   flask --app app run
   ```

The application will use the local SQLite database stored in the instance folder by default.

## API Overview

The backend exposes REST endpoints under the /api prefix.

### Properties

- GET /api/properties
- GET /api/properties/<id>
- POST /api/properties
- PUT /api/properties/<id>
- DELETE /api/properties/<id>
- GET /api/properties/host/mine

### Bookings

- GET /api/bookings
- GET /api/bookings/<id>
- POST /api/bookings
- PUT /api/bookings/<id>/status
- DELETE /api/bookings/<id>

### Reviews

- GET /api/reviews/property/<property_id>
- GET /api/reviews/<id>
- POST /api/reviews
- PUT /api/reviews/<id>
- DELETE /api/reviews/<id>

### Users

- GET /api/users/me
- PUT /api/users/me
- PUT /api/users/me/upgrade-to-host
- PUT /api/users/me/preferences
- DELETE /api/users/me

### Amenities

- GET /api/amenities
- GET /api/amenities/<id>
- POST /api/amenities
- PUT /api/amenities/<id>
- DELETE /api/amenities/<id>

## Authentication

Protected endpoints require a valid JWT token. Include the token in the Authorization header:

```http
Authorization: Bearer <token>
```

## Notes

This project is designed as a backend service for a rental marketplace and can be extended with authentication, payments, notifications, and deployment configuration.
