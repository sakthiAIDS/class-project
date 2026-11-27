<<<<<<< HEAD
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and Oxlint's TypeScript related rules in your project.
=======
# Food Donation Management System

A full-stack web app that connects food donors (restaurants, hotels, bakeries,
marriage halls, supermarkets, individuals) with NGOs and volunteers to rescue
surplus food before it goes to waste.

Built as a college mini project. **This is a Food Donation Management System —
not an AI project.** A few small rule-based "AI support features" are layered
on top (see below), but they are not the core of the system.

---

## Tech Stack

| Layer      | Technology |
|------------|------------|
| Frontend   | HTML5, CSS3, JavaScript, Bootstrap 5, Font Awesome |
| Backend    | Python Flask |
| Database   | SQLite (default, zero setup) — MySQL supported via `database.sql` |
| Charts     | Chart.js |
| Auth       | Flask sessions + Werkzeug password hashing |

---

## 1. Run it in VS Code (step by step)

### Requirements
- Python 3.10+ installed
- VS Code with the **Python extension** installed

### Steps

1. **Open the folder in VS Code**
   `File → Open Folder…` → select the `food-donation-system` folder.

2. **Open a terminal in VS Code**
   `Terminal → New Terminal`

3. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```
   Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Load sample data** (20 donors, 10 NGOs, 100 donations, admin account)
   ```bash
   python seed_data.py
   ```
   This creates `instance/app.db` (SQLite) and prints demo login credentials.

6. **Run the app**
   ```bash
   python app.py
   ```

7. **Open your browser** at: `http://127.0.0.1:5000`

That's it — no MySQL server, no extra config needed to demo the project.

---

## 2. Demo Logins

| Role  | Email | Password |
|-------|-------|----------|
| Admin | admin@fooddonation.org | admin123 |
| Donor | donor1@example.com | donor123 |
| NGO   | ngo1@example.com | ngo123 |

You can also register a new account from the Register page.

---

## 3. Project Structure

```
food-donation-system/
│
├── app.py                  # Flask app: all routes/views
├── models.py                # SQLAlchemy database models
├── config.py                 # App configuration (SQLite/MySQL switch)
├── utils.py                    # Helper functions + rule-based AI features
├── seed_data.py                  # Generates sample donors/NGOs/donations
├── database.sql                    # MySQL schema (optional, see below)
├── requirements.txt
├── README.md
│
├── instance/
│   └── app.db                # SQLite database (auto-created)
│
├── templates/                # Jinja2 HTML templates
│   ├── base.html              # Shared layout: sidebar + topbar
│   ├── login.html
│   ├── register.html
│   ├── dashboard_user.html     # Donor dashboard
│   ├── donate_food.html
│   ├── history.html
│   ├── tracking.html
│   ├── notifications.html
│   ├── profile.html
│   ├── settings.html
│   ├── dashboard_ngo.html
│   ├── dashboard_admin.html
│   └── reports.html
│
└── static/
    ├── css/style.css          # All styling (design system + components)
    ├── js/main.js              # Dark mode, sidebar, counters, toasts
    ├── uploads/                  # Uploaded logos & food images
    └── qrcodes/                   # Generated donation QR codes
```

---

## 4. Switching to MySQL (optional)

The project uses SQLite by default so it "just works" in VS Code. If your
college specifically requires MySQL:

1. Install MySQL Server and create the database:
   ```bash
   mysql -u root -p < database.sql
   ```
2. Install the MySQL driver:
   ```bash
   pip install pymysql
   ```
3. Open `config.py` and:
   - Set `USE_MYSQL = True`
   - Fill in `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_DB`
4. Run `python seed_data.py` again to populate MySQL, then `python app.py`.

---

## 5. AI Support Features (not the core project)

These are small, explainable, rule-based helpers in `utils.py` — no external
AI service is called:

1. **Category suggestion** — matches keywords in the food name (e.g.
   "Biryani" → Main Course) as you type on the Donate Food page.
2. **Pickup priority** — flags a donation "High Priority" if it expires
   within 45 minutes.
3. **Best NGO recommendation** — scores nearby approved NGOs using distance
   and past pickup success rate, shown when an NGO taps the ✨ button on a
   donation card.
4. **Duplicate donation detection** — warns a donor if they submit the same
   food item again within a 2-hour window.

---

## 6. Key Features by Role

**Donor:** dashboard with stats & charts, donate food form, history, live
tracking timeline, notifications, profile, settings, dark mode.

**NGO:** browse/filter available donations, accept pickups, update pickup
status (volunteer assigned → picked up → delivered → completed), AI NGO
recommendation.

**Admin:** platform-wide analytics, approve/reject NGOs, disable fake
accounts, recent donations table, reports.

---

## 7. Notes for Presentation

- Sample data is deterministic (`random.seed(42)` in `seed_data.py`), so
  charts and tables look consistent every time you re-seed.
- Re-run `python seed_data.py` any time to reset the database to a clean demo
  state (this drops and recreates all tables).
- The Google Maps section on the Donate Food page is a styled placeholder
  (click-to-drop-pin) so the project runs without needing a paid Maps API
  key — swap in a real `<iframe>`/JS SDK embed if you have a key.
- PDF/Excel export buttons on the Reports page are wired up as placeholders
  ready for you to plug in `reportlab`/`openpyxl` if your project needs real
  file generation.

---

Built for a college mini-project exhibition — clean, commented, and easy to
extend.
>>>>>>> 8606cb47e998208affaca991b75fa79a5de99608
