"""
Food Donation Management System
--------------------------------
A Flask + SQLite (or MySQL) web app that connects food donors (restaurants,
hotels, marriage halls, bakeries, supermarkets, individuals) with NGOs and
volunteers to rescue surplus food before it goes to waste.

AI is used only as small supporting features (category suggestion, pickup
priority, NGO recommendation, duplicate detection) — see utils.py.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

import os
from datetime import datetime, timedelta
from functools import wraps

from flask import (Flask, render_template, request, redirect, url_for,
                    session, flash, jsonify, abort)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from models import (db, User, Donation, DonationImage, PickupRequest,
                     Volunteer, Notification, Report)
from utils import (generate_donation_code, suggest_category, compute_priority,
                    recommend_ngo, is_duplicate_donation, generate_qr_code,
                    allowed_file)

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["QR_FOLDER"], exist_ok=True)

db.init_app(app)


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                flash("You don't have access to that page.", "danger")
                return redirect(url_for("dashboard_router"))
            return f(*args, **kwargs)
        return wrapped
    return decorator


def current_user():
    uid = session.get("user_id")
    return User.query.get(uid) if uid else None


@app.context_processor
def inject_globals():
    return {
        "current_user": current_user(),
        "unread_count": (Notification.query
                          .filter_by(user_id=session.get("user_id"), is_read=False)
                          .count() if session.get("user_id") else 0),
        "now": datetime.utcnow(),
    }


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard_router"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            if not user.is_active:
                flash("Your account has been disabled. Contact admin.", "danger")
                return redirect(url_for("login"))
            session["user_id"] = user.id
            session["role"] = user.role
            session["name"] = user.name
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("dashboard_router"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        category = request.form.get("category", "Individual")
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
            return redirect(url_for("register"))
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register"))

        role = "ngo" if category == "NGO" else ("volunteer" if category == "Volunteer" else "donor")

        logo_path = None
        logo = request.files.get("logo")
        if logo and logo.filename and allowed_file(logo.filename, app.config["ALLOWED_EXTENSIONS"]):
            filename = secure_filename(f"{email}_{logo.filename}")
            logo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            logo_path = f"uploads/{filename}"

        user = User(
            name=name, email=email, phone=phone, address=address,
            category=category, role=role, logo_path=logo_path,
            password_hash=generate_password_hash(password),
            is_approved=(role != "ngo"),  # NGOs need admin approval
        )
        db.session.add(user)
        db.session.commit()

        if role == "ngo":
            flash("Registration successful! Your NGO account is pending admin approval.", "info")
        else:
            flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required()
def dashboard_router():
    role = session.get("role")
    if role == "admin":
        return redirect(url_for("admin_dashboard"))
    if role == "ngo":
        return redirect(url_for("ngo_dashboard"))
    return redirect(url_for("donor_dashboard"))


# ---------------------------------------------------------------------------
# Donor routes
# ---------------------------------------------------------------------------
@app.route("/donor/dashboard")
@login_required()
def donor_dashboard():
    user = current_user()
    donations = Donation.query.filter_by(donor_id=user.id).order_by(Donation.created_at.desc()).all()

    stats = {
        "total": len(donations),
        "pending": len([d for d in donations if d.status in ("created", "accepted", "volunteer_assigned")]),
        "completed": len([d for d in donations if d.status == "completed"]),
        "meals": sum(d.meals_count or 0 for d in donations),
    }
    recent = donations[:6]

    return render_template("dashboard_user.html", stats=stats, recent=recent)


@app.route("/donate", methods=["GET", "POST"])
@login_required()
def donate_food():
    if request.method == "POST":
        food_name = request.form.get("food_name", "").strip()
        category = request.form.get("category") or suggest_category(food_name)
        quantity = request.form.get("quantity", "")
        meals_count = int(request.form.get("meals_count") or 0)
        prep_time_raw = request.form.get("prep_time")
        expiry_time_raw = request.form.get("expiry_time")
        pickup_address = request.form.get("pickup_address", "")
        contact_person = request.form.get("contact_person", "")
        contact_phone = request.form.get("contact_phone", "")
        instructions = request.form.get("instructions", "")
        lat = float(request.form.get("latitude") or 11.3410)
        lon = float(request.form.get("longitude") or 77.7172)

        prep_time = datetime.fromisoformat(prep_time_raw) if prep_time_raw else None
        expiry_time = datetime.fromisoformat(expiry_time_raw) if expiry_time_raw else None

        user = current_user()

        # AI Feature 4: duplicate check within the last 2 hours
        recent = Donation.query.filter_by(donor_id=user.id).order_by(Donation.created_at.desc()).limit(20).all()
        if is_duplicate_donation(user.id, food_name, recent):
            flash("Similar donation already exists — submitted in the last 2 hours.", "warning")
            return redirect(url_for("donate_food"))

        image_path = None
        image = request.files.get("food_image")
        if image and image.filename and allowed_file(image.filename, app.config["ALLOWED_EXTENSIONS"]):
            filename = secure_filename(f"food_{datetime.utcnow().timestamp()}_{image.filename}")
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_path = f"uploads/{filename}"

        donation = Donation(
            donation_code=generate_donation_code(),
            donor_id=user.id,
            food_name=food_name,
            category=category,
            quantity=quantity,
            meals_count=meals_count,
            prep_time=prep_time,
            expiry_time=expiry_time,
            pickup_address=pickup_address,
            latitude=lat, longitude=lon,
            contact_person=contact_person,
            contact_phone=contact_phone,
            instructions=instructions,
            image_path=image_path,
            status="created",
            priority=compute_priority(expiry_time),
        )
        db.session.add(donation)
        db.session.commit()

        flash(f"Donation submitted! Your Donation ID is {donation.donation_code}.", "success")
        return redirect(url_for("track_donation", code=donation.donation_code))

    suggested = suggest_category(request.args.get("food_name", ""))
    return render_template("donate_food.html", suggested_category=suggested)


@app.route("/api/suggest-category")
@login_required()
def api_suggest_category():
    food_name = request.args.get("food_name", "")
    return jsonify({"category": suggest_category(food_name)})


@app.route("/history")
@login_required()
def history():
    user = current_user()
    donations = Donation.query.filter_by(donor_id=user.id).order_by(Donation.created_at.desc()).all()
    return render_template("history.html", donations=donations)


@app.route("/track/<code>")
@login_required()
def track_donation(code):
    donation = Donation.query.filter_by(donation_code=code).first_or_404()
    steps = ["created", "accepted", "volunteer_assigned", "picked_up", "delivered", "completed"]
    current_index = steps.index(donation.status) if donation.status in steps else 0
    return render_template("tracking.html", donation=donation, steps=steps, current_index=current_index)


@app.route("/notifications")
@login_required()
def notifications():
    user = current_user()
    notifs = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).all()
    Notification.query.filter_by(user_id=user.id, is_read=False).update({"is_read": True})
    db.session.commit()
    return render_template("notifications.html", notifications=notifs)


@app.route("/profile", methods=["GET", "POST"])
@login_required()
def profile():
    user = current_user()
    if request.method == "POST":
        user.name = request.form.get("name", user.name)
        user.phone = request.form.get("phone", user.phone)
        user.address = request.form.get("address", user.address)
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile"))

    donations = Donation.query.filter_by(donor_id=user.id).all()
    stats = {
        "total": len(donations),
        "meals": sum(d.meals_count or 0 for d in donations),
        "completed": len([d for d in donations if d.status == "completed"]),
    }
    return render_template("profile.html", stats=stats)


@app.route("/profile/change-password", methods=["POST"])
@login_required()
def change_password():
    user = current_user()
    current = request.form.get("current_password", "")
    new = request.form.get("new_password", "")
    if not check_password_hash(user.password_hash, current):
        flash("Current password is incorrect.", "danger")
    else:
        user.password_hash = generate_password_hash(new)
        db.session.commit()
        flash("Password changed successfully.", "success")
    return redirect(url_for("profile"))


@app.route("/settings")
@login_required()
def settings():
    return render_template("settings.html")


# ---------------------------------------------------------------------------
# NGO routes
# ---------------------------------------------------------------------------
@app.route("/ngo/dashboard")
@login_required(role="ngo")
def ngo_dashboard():
    user = current_user()
    available = (Donation.query
                 .filter(Donation.status == "created")
                 .order_by(Donation.priority.desc(), Donation.expiry_time.asc())
                 .all())
    accepted = Donation.query.filter_by(ngo_id=user.id).filter(
        Donation.status.in_(["accepted", "volunteer_assigned", "picked_up"])).all()
    completed = Donation.query.filter_by(ngo_id=user.id, status="completed").all()

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    todays_meals = sum(
        d.meals_count or 0 for d in
        Donation.query.filter_by(ngo_id=user.id).filter(Donation.accepted_at >= today_start).all()
    )

    stats = {
        "available": len(available),
        "accepted": len(accepted),
        "completed": len(completed),
        "todays_meals": todays_meals,
    }

    for d in available:
        d.distance_km = round(((d.latitude - user.latitude) ** 2 + (d.longitude - user.longitude) ** 2) ** 0.5 * 111, 1)
        d.minutes_to_expiry = int((d.expiry_time - datetime.utcnow()).total_seconds() / 60) if d.expiry_time else None

    return render_template("dashboard_ngo.html", stats=stats, available=available, accepted=accepted)


@app.route("/ngo/accept/<int:donation_id>", methods=["POST"])
@login_required(role="ngo")
def ngo_accept(donation_id):
    user = current_user()
    donation = Donation.query.get_or_404(donation_id)
    if donation.status != "created":
        flash("This donation has already been accepted by another NGO.", "warning")
        return redirect(url_for("ngo_dashboard"))

    donation.ngo_id = user.id
    donation.status = "accepted"
    donation.accepted_at = datetime.utcnow()
    db.session.add(donation)

    notif = Notification(user_id=donation.donor_id, title="Donation Accepted",
                          message=f"{user.name} accepted your donation {donation.donation_code}.",
                          type="accepted")
    db.session.add(notif)
    db.session.commit()
    flash(f"You accepted donation {donation.donation_code}.", "success")
    return redirect(url_for("ngo_dashboard"))


@app.route("/ngo/update-status/<int:donation_id>", methods=["POST"])
@login_required(role="ngo")
def ngo_update_status(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    new_status = request.form.get("status")
    valid = ["volunteer_assigned", "picked_up", "delivered", "completed"]
    if new_status in valid:
        donation.status = new_status
        now = datetime.utcnow()
        if new_status == "picked_up":
            donation.picked_up_at = now
        elif new_status == "delivered":
            donation.delivered_at = now
        elif new_status == "completed":
            donation.completed_at = now
        db.session.add(donation)

        notif = Notification(user_id=donation.donor_id, title="Donation Update",
                              message=f"Donation {donation.donation_code} is now {new_status.replace('_', ' ')}.",
                              type="pickup" if new_status != "delivered" else "delivered")
        db.session.add(notif)
        db.session.commit()
        flash("Status updated.", "success")
    return redirect(url_for("ngo_dashboard"))


@app.route("/api/recommend-ngo/<int:donation_id>")
@login_required()
def api_recommend_ngo(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    ngos = User.query.filter_by(role="ngo", is_approved=True, is_active=True).all()
    best = recommend_ngo(donation.latitude, donation.longitude, ngos)
    if not best:
        return jsonify({"found": False})
    return jsonify({
        "found": True,
        "ngo_name": best["ngo"].name,
        "distance_km": best["distance_km"],
        "eta_minutes": best["eta_minutes"],
    })


# ---------------------------------------------------------------------------
# Admin routes
# ---------------------------------------------------------------------------
@app.route("/admin/dashboard")
@login_required(role="admin")
def admin_dashboard():
    donors = User.query.filter_by(role="donor").count()
    ngos = User.query.filter_by(role="ngo").count()
    pending_ngos = User.query.filter_by(role="ngo", is_approved=False).all()

    pending_donations = Donation.query.filter(Donation.status != "completed").count()
    completed_donations = Donation.query.filter_by(status="completed").count()
    total_meals = db.session.query(db.func.sum(Donation.meals_count)).scalar() or 0
    food_saved_kg = round(total_meals * 0.4, 1)  # rough estimate: 0.4kg per meal

    recent_donations = Donation.query.order_by(Donation.created_at.desc()).limit(10).all()

    stats = {
        "donors": donors, "ngos": ngos,
        "pending_donations": pending_donations,
        "completed_donations": completed_donations,
        "food_saved_kg": food_saved_kg,
        "total_meals": total_meals,
    }
    return render_template("dashboard_admin.html", stats=stats,
                            pending_ngos=pending_ngos, recent_donations=recent_donations)


@app.route("/admin/approve-ngo/<int:user_id>", methods=["POST"])
@login_required(role="admin")
def approve_ngo(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash(f"{user.name} approved as a verified NGO.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/remove-user/<int:user_id>", methods=["POST"])
@login_required(role="admin")
def remove_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    flash(f"{user.name}'s account has been disabled.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/reports")
@login_required()
def reports():
    donations = Donation.query.all()
    total_meals = sum(d.meals_count or 0 for d in donations)
    completed = len([d for d in donations if d.status == "completed"])
    success_rate = round((completed / len(donations) * 100), 1) if donations else 0

    top_donors = (db.session.query(User.name, db.func.count(Donation.id).label("count"))
                  .join(Donation, Donation.donor_id == User.id)
                  .group_by(User.id).order_by(db.desc("count")).limit(5).all())
    top_ngos = (db.session.query(User.name, db.func.count(Donation.id).label("count"))
                .join(Donation, Donation.ngo_id == User.id)
                .group_by(User.id).order_by(db.desc("count")).limit(5).all())

    stats = {
        "total_meals": total_meals,
        "food_saved_kg": round(total_meals * 0.4, 1),
        "success_rate": success_rate,
        "total_donations": len(donations),
    }
    return render_template("reports.html", stats=stats, top_donors=top_donors, top_ngos=top_ngos)


@app.route("/reports/download/<fmt>")
@login_required()
def download_report(fmt):
    # Placeholder endpoint for PDF/Excel export (kept lightweight for the demo).
    flash(f"{fmt.upper()} report export is a placeholder in this prototype.", "info")
    return redirect(url_for("reports"))


# ---------------------------------------------------------------------------
# Chart data APIs (used by Chart.js on the dashboards)
# ---------------------------------------------------------------------------
@app.route("/api/charts/monthly-donations")
@login_required()
def chart_monthly_donations():
    labels, values = [], []
    today = datetime.utcnow()
    # Build last 6 months labels
    months = []
    year, month = today.year, today.month
    for i in range(5, -1, -1):
        m = month - i
        y = year
        while m <= 0:
            m += 12
            y -= 1
        months.append((y, m))

    for (y, m) in months:
        start = datetime(y, m, 1)
        end = datetime(y + 1, 1, 1) if m == 12 else datetime(y, m + 1, 1)
        count = Donation.query.filter(Donation.created_at >= start, Donation.created_at < end).count()
        labels.append(start.strftime("%b"))
        values.append(count)

    return jsonify({"labels": labels, "values": values})


@app.route("/api/charts/donation-categories")
@login_required()
def chart_donation_categories():
    rows = (db.session.query(Donation.category, db.func.count(Donation.id))
            .group_by(Donation.category).all())
    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]
    return jsonify({"labels": labels, "values": values})


@app.route("/api/charts/cities")
@login_required(role="admin")
def chart_cities():
    # Demo data since real city field isn't modeled explicitly; derived from address text.
    rows = (db.session.query(User.address, db.func.count(User.id))
            .filter(User.role == "donor").group_by(User.address).limit(6).all())
    labels = [r[0] or "Unknown" for r in rows]
    values = [r[1] for r in rows]
    return jsonify({"labels": labels, "values": values})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
