"""
Utility helpers, including the lightweight rule-based "AI support features".

None of this is a machine-learning model — the project brief is explicit that
AI is a *supporting* feature, not the core project. These are simple,
explainable rules that feel smart in a demo without any external AI service.
"""

import math
import os
import random
import string
from datetime import datetime, timedelta

import qrcode


# ---------------------------------------------------------------------------
# Donation ID generation
# ---------------------------------------------------------------------------
def generate_donation_code():
    today = datetime.utcnow().strftime("%Y%m%d")
    suffix = "".join(random.choices(string.digits, k=4))
    return f"FD-{today}-{suffix}"


# ---------------------------------------------------------------------------
# AI Feature 1: Suggest a food category from the food name
# ---------------------------------------------------------------------------
CATEGORY_KEYWORDS = {
    "Main Course": ["biryani", "rice", "curry", "meals", "thali", "noodles",
                     "pasta", "roti", "chapati", "sambar", "kurma", "briyani"],
    "Snacks": ["samosa", "vada", "bajji", "bonda", "chips", "cutlet", "roll", "puff"],
    "Dessert": ["cake", "sweet", "halwa", "payasam", "ice cream", "jamun", "kheer", "pastry"],
    "Beverage": ["juice", "milk", "tea", "coffee", "lassi", "buttermilk", "shake"],
}


def suggest_category(food_name: str) -> str:
    name = (food_name or "").lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(k in name for k in keywords):
            return category
    return "Main Course"  # sensible default


# ---------------------------------------------------------------------------
# AI Feature 2: Pickup priority based on how soon food expires
# ---------------------------------------------------------------------------
def compute_priority(expiry_time: datetime) -> str:
    if not expiry_time:
        return "Normal"
    minutes_left = (expiry_time - datetime.utcnow()).total_seconds() / 60
    if minutes_left <= 45:
        return "High"
    return "Normal"


# ---------------------------------------------------------------------------
# AI Feature 3: Recommend the best NGO using distance + success rate + availability
# ---------------------------------------------------------------------------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def recommend_ngo(donation_lat, donation_lon, ngo_list):
    """
    ngo_list: list of User objects with role == 'ngo'
    Scores each NGO with a simple weighted formula and returns the best match
    plus distance / ETA for display.
    """
    scored = []
    for ngo in ngo_list:
        distance = haversine_km(donation_lat, donation_lon, ngo.latitude, ngo.longitude)
        # Lower distance is better, higher success rate is better.
        score = (ngo.pickup_success_rate * 0.7) - (distance * 3)
        eta_minutes = max(5, round(distance * 3))  # rough estimate, ~20km/h effective speed
        scored.append({
            "ngo": ngo,
            "distance_km": round(distance, 1),
            "eta_minutes": eta_minutes,
            "score": score,
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[0] if scored else None


# ---------------------------------------------------------------------------
# AI Feature 4: Duplicate donation detection
# ---------------------------------------------------------------------------
def is_duplicate_donation(donor_id, food_name, recent_donations, window_minutes=120):
    cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
    for d in recent_donations:
        if (d.donor_id == donor_id and
                d.food_name.strip().lower() == food_name.strip().lower() and
                d.created_at >= cutoff):
            return True
    return False


# ---------------------------------------------------------------------------
# QR code generator for a donation
# ---------------------------------------------------------------------------
def generate_qr_code(donation_code, qr_folder):
    os.makedirs(qr_folder, exist_ok=True)
    path = os.path.join(qr_folder, f"{donation_code}.png")
    img = qrcode.make(f"DONATION:{donation_code}")
    img.save(path)
    return f"qrcodes/{donation_code}.png"


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
