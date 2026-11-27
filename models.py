"""
Database models for the Food Donation Management System.

Tables:
    User            -> donors, ngos, volunteers, admin (role based)
    Donation        -> a single food donation posting
    DonationImage   -> extra images attached to a donation
    PickupRequest   -> links a donation to the NGO/volunteer handling pickup
    Volunteer       -> volunteers who can be assigned to a pickup
    Notification    -> in-app notifications for a user
    Report          -> generated report snapshots (for the Reports page)
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    password_hash = db.Column(db.String(255), nullable=False)

    # donor | ngo | volunteer | admin
    role = db.Column(db.String(20), nullable=False, default="donor")
    # Restaurant / Hotel / Marriage Hall / Bakery / Supermarket / NGO / Volunteer / Individual
    category = db.Column(db.String(30), default="Individual")

    logo_path = db.Column(db.String(255))
    is_approved = db.Column(db.Boolean, default=True)   # NGOs need admin approval
    is_active = db.Column(db.Boolean, default=True)
    pickup_success_rate = db.Column(db.Float, default=90.0)  # used by AI recommendation
    latitude = db.Column(db.Float, default=11.3410)
    longitude = db.Column(db.Float, default=77.7172)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    donations = db.relationship("Donation", backref="donor", lazy=True,
                                 foreign_keys="Donation.donor_id")

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "email": self.email,
            "role": self.role, "category": self.category,
        }


class Donation(db.Model):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)
    donation_code = db.Column(db.String(20), unique=True, nullable=False)  # e.g. FD-20260727-0001

    donor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ngo_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    food_name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(30), nullable=False)   # Veg/Non Veg/Dessert/Snacks/Beverage
    quantity = db.Column(db.String(50))
    meals_count = db.Column(db.Integer, default=0)

    prep_time = db.Column(db.DateTime)
    expiry_time = db.Column(db.DateTime)

    pickup_address = db.Column(db.String(255))
    latitude = db.Column(db.Float, default=11.3410)
    longitude = db.Column(db.Float, default=77.7172)

    contact_person = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    instructions = db.Column(db.Text)
    image_path = db.Column(db.String(255))

    # created | accepted | volunteer_assigned | picked_up | delivered | completed | expired
    status = db.Column(db.String(30), default="created")
    priority = db.Column(db.String(10), default="Normal")  # High / Normal

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime)
    picked_up_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    images = db.relationship("DonationImage", backref="donation", lazy=True)
    ngo = db.relationship("User", foreign_keys=[ngo_id])


class DonationImage(db.Model):
    __tablename__ = "donation_images"
    id = db.Column(db.Integer, primary_key=True)
    donation_id = db.Column(db.Integer, db.ForeignKey("donations.id"), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)


class PickupRequest(db.Model):
    __tablename__ = "pickup_requests"
    id = db.Column(db.Integer, primary_key=True)
    donation_id = db.Column(db.Integer, db.ForeignKey("donations.id"), nullable=False)
    ngo_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey("volunteers.id"), nullable=True)
    status = db.Column(db.String(30), default="assigned")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Volunteer(db.Model):
    __tablename__ = "volunteers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    vehicle = db.Column(db.String(50), default="Two Wheeler")
    is_available = db.Column(db.Boolean, default=True)
    ngo_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.String(255))
    type = db.Column(db.String(30), default="info")  # accepted/pickup/delivered/expiry/info
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Report(db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(20))  # Daily/Weekly/Monthly/Yearly
    total_donations = db.Column(db.Integer, default=0)
    total_meals = db.Column(db.Integer, default=0)
    food_saved_kg = db.Column(db.Float, default=0)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
