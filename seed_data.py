"""
Populates the database with realistic sample data so the dashboards,
charts, and tables look alive for a demo/presentation.

Run:
    python seed_data.py
"""

import random
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from app import app
from models import db, User, Donation, Notification, Volunteer

random.seed(42)

DONOR_NAMES = [
    ("Spice Garden Restaurant", "Restaurant"), ("Green Leaf Hotel", "Hotel"),
    ("Royal Marriage Hall", "Marriage Hall"), ("Sunrise Bakery", "Bakery"),
    ("Fresh Mart Supermarket", "Supermarket"), ("Taj Continental Hotel", "Hotel"),
    ("Annapoorna Restaurant", "Restaurant"), ("City Celebration Hall", "Marriage Hall"),
    ("Golden Crust Bakery", "Bakery"), ("Big Basket Store", "Supermarket"),
    ("Priya's Kitchen", "Individual"), ("Curry Leaf Restaurant", "Restaurant"),
    ("Palace Banquet Hall", "Marriage Hall"), ("Daily Bread Bakery", "Bakery"),
    ("Metro Supermarket", "Supermarket"), ("Sangam Hotel", "Hotel"),
    ("Ramesh Kumar", "Individual"), ("Vasantham Restaurant", "Restaurant"),
    ("Grand Function Hall", "Marriage Hall"), ("Sweet Corner Bakery", "Bakery"),
]

NGO_NAMES = [
    "Helping Hands Foundation", "Feed The Need NGO", "Anna Dhanam Trust",
    "Care & Share Society", "No Hunger Mission", "Seva Bharathi NGO",
    "Food For All Trust", "Compassion Kitchen NGO", "Bright Future Foundation",
    "United Care NGO",
]

FOOD_ITEMS = [
    ("Vegetable Biryani", "Main Course"), ("Chicken Curry", "Main Course"),
    ("Paneer Butter Masala", "Main Course"), ("Idli Sambar", "Main Course"),
    ("Samosa", "Snacks"), ("Vada", "Snacks"), ("Bread Rolls", "Snacks"),
    ("Gulab Jamun", "Dessert"), ("Rasmalai", "Dessert"), ("Cake Slices", "Dessert"),
    ("Fresh Fruit Juice", "Beverage"), ("Butter Milk", "Beverage"),
    ("Chapati & Curry", "Main Course"), ("Fried Rice", "Main Course"),
    ("Cup Cakes", "Dessert"), ("Sandwiches", "Snacks"),
]

CITIES = [
    ("Tiruchengode", 11.3805, 77.8951), ("Salem", 11.6643, 78.1460),
    ("Erode", 11.3410, 77.7172), ("Namakkal", 11.2189, 78.1677),
    ("Coimbatore", 11.0168, 76.9558), ("Karur", 10.9601, 78.0766),
]


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # --- Admin ---
        admin = User(name="System Admin", email="admin@fooddonation.org",
                     phone="9999900000", address="Admin Office, Tiruchengode",
                     category="Individual", role="admin",
                     password_hash=generate_password_hash("admin123"),
                     is_approved=True)
        db.session.add(admin)

        # --- Donors ---
        donors = []
        for i, (name, category) in enumerate(DONOR_NAMES):
            city, lat, lon = random.choice(CITIES)
            jitter_lat = lat + random.uniform(-0.03, 0.03)
            jitter_lon = lon + random.uniform(-0.03, 0.03)
            donor = User(
                name=name, email=f"donor{i+1}@example.com", phone=f"98765{10000+i}",
                address=f"{random.randint(1,200)} Main Road, {city}",
                category=category, role="donor",
                password_hash=generate_password_hash("donor123"),
                is_approved=True, latitude=jitter_lat, longitude=jitter_lon,
            )
            donors.append(donor)
            db.session.add(donor)

        # --- NGOs ---
        ngos = []
        for i, name in enumerate(NGO_NAMES):
            city, lat, lon = random.choice(CITIES)
            jitter_lat = lat + random.uniform(-0.03, 0.03)
            jitter_lon = lon + random.uniform(-0.03, 0.03)
            ngo = User(
                name=name, email=f"ngo{i+1}@example.com", phone=f"97654{20000+i}",
                address=f"{random.randint(1,150)} Trust Road, {city}",
                category="NGO", role="ngo",
                password_hash=generate_password_hash("ngo123"),
                is_approved=(i != len(NGO_NAMES) - 1),  # leave last one pending for demo
                pickup_success_rate=round(random.uniform(75, 99), 1),
                latitude=jitter_lat, longitude=jitter_lon,
            )
            ngos.append(ngo)
            db.session.add(ngo)

        # --- Volunteers ---
        for i in range(8):
            v = Volunteer(name=f"Volunteer {i+1}", phone=f"96543{30000+i}",
                           vehicle=random.choice(["Two Wheeler", "Van", "Bicycle"]),
                           ngo_id=None)
            db.session.add(v)

        db.session.commit()

        # --- Donations ---
        statuses_pool = (["completed"] * 5 + ["created"] * 2 + ["accepted"] * 2 +
                          ["picked_up"] * 1 + ["delivered"] * 1)

        for i in range(100):
            donor = random.choice(donors)
            food_name, category = random.choice(FOOD_ITEMS)
            days_ago = random.randint(0, 150)
            created_at = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
            prep_time = created_at
            expiry_time = created_at + timedelta(hours=random.randint(2, 8))
            meals = random.randint(15, 250)
            status = random.choice(statuses_pool)

            donation = Donation(
                donation_code=f"FD-{created_at.strftime('%Y%m%d')}-{1000+i}",
                donor_id=donor.id,
                food_name=food_name, category=category,
                quantity=f"{random.randint(5, 40)} kg",
                meals_count=meals,
                prep_time=prep_time, expiry_time=expiry_time,
                pickup_address=donor.address,
                latitude=donor.latitude, longitude=donor.longitude,
                contact_person=donor.name, contact_phone=donor.phone,
                instructions=random.choice(["Handle with care", "Call before arrival",
                                             "Use side entrance", ""]),
                status=status,
                priority=random.choice(["High", "Normal", "Normal"]),
                created_at=created_at,
            )
            if status != "created":
                donation.ngo_id = random.choice(ngos).id
                donation.accepted_at = created_at + timedelta(minutes=random.randint(5, 40))
            if status in ("picked_up", "delivered", "completed"):
                donation.picked_up_at = donation.accepted_at + timedelta(minutes=20)
            if status in ("delivered", "completed"):
                donation.delivered_at = donation.picked_up_at + timedelta(minutes=30)
            if status == "completed":
                donation.completed_at = donation.delivered_at + timedelta(minutes=10)

            db.session.add(donation)

        db.session.commit()

        # --- Notifications for the first donor (handy demo login) ---
        demo_donor = donors[0]
        sample_notifs = [
            ("Donation Accepted", "Helping Hands Foundation accepted your donation.", "accepted"),
            ("Pickup Started", "Volunteer is on the way to collect your donation.", "pickup"),
            ("Donation Delivered", "Your donation was delivered successfully. Thank you!", "delivered"),
            ("Expiry Reminder", "One of your donations expires in 30 minutes.", "expiry"),
        ]
        for title, msg, ntype in sample_notifs:
            db.session.add(Notification(user_id=demo_donor.id, title=title, message=msg, type=ntype))

        db.session.commit()
        print("Sample data created:")
        print(f"  Donors     : {len(donors)}")
        print(f"  NGOs       : {len(ngos)}")
        print(f"  Donations  : {Donation.query.count()}")
        print("\nDemo logins:")
        print("  Admin : admin@fooddonation.org / admin123")
        print(f"  Donor : donor1@example.com / donor123")
        print(f"  NGO   : ngo1@example.com / ngo123")


if __name__ == "__main__":
    run()
