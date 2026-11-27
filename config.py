"""
Configuration for the Food Donation Management System.

By default this project uses SQLite so it runs instantly in VS Code with
zero setup. If your college wants MySQL, flip USE_MYSQL to True below,
create the database using database.sql, and fill in your credentials.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ---- Switch this to True to use MySQL instead of SQLite ----
USE_MYSQL = False

MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_HOST = "localhost"
MYSQL_DB = "food_donation_db"


class Config:
    SECRET_KEY = "campus-food-rescue-secret-key-change-in-production"

    if USE_MYSQL:
        # Requires: pip install pymysql
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    QR_FOLDER = os.path.join(BASE_DIR, "static", "qrcodes")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB uploads
