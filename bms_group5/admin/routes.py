from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from functools import wraps

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

# --- Decorator for admin-only routes ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# === Admin Pages ===
@admin_bp.route("/admindashboard")
@admin_required
def admindashboard():
    return render_template("admin/admin_dashboard.html", title="Dashboard")

@admin_bp.route("/adminresidents")
@admin_required
def adminresidents():
    return render_template("admin_resident_management.html", title="Residents Management")

@admin_bp.route('/add_resident', methods=['GET', 'POST'])
@admin_required
def add_resident():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        purok = request.form.get('purok')

        # TODO: insert into your database (ORM or SQL)
        # example:
        # new_resident = Resident(name=name, age=age, purok=purok)
        # db.session.add(new_resident)
        # db.session.commit()

        flash(f"Resident {name} added successfully!", "success")
        return redirect(url_for('admin_bp.admin_resident_management'))

    return render_template('admin_add_resident.html')


@admin_bp.route("/adminofficials")
@admin_required
def adminofficials():
    return render_template("admin_brgyofficial.html", title="Barangay Officials")

@admin_bp.route('/add_official', methods=['GET', 'POST'])
def add_official():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        position = request.form.get('position')
        contact_number = request.form.get('contact_number')
        term_start = request.form.get('term_start')
        term_end = request.form.get('term_end')

        # --- Database code (to be added later) ---
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            # INSERT INTO barangay_officials (full_name, position, contact_number, term_start, term_end)
            # VALUES (%s, %s, %s, %s, %s)
        """, (full_name, position, contact_number, term_start, term_end))

        conn.commit()
        cursor.close()
        conn.close()
        """

        flash(f"Barangay official '{full_name}' added successfully!", "success")
        return redirect(url_for('admin.adminofficials'))

    return render_template('add_editofficial.html', title="Add Barangay Official")

@admin_bp.route("/admincomplaints")
@admin_required
def admincomplaints():
    return render_template("admin_complains.html", title="Complaints & Blotter")

@admin_bp.route("/admincertificates")
@admin_required
def admincertificates():
    return render_template("admin_certificates.html", title="Certificates")

@admin_bp.route("/adminannouncement")
@admin_required
def adminannouncement():
    return render_template("admin_announcement.html", title="Announcements")

@admin_bp.route("/adminaddannouncement", methods=["GET", "POST"])
@admin_required
def adminaddannouncement():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        date_posted = request.form.get("date_posted")

        # --- Example: Saving to database (commented out for now) ---
        # new_announcement = Announcement(title=title, content=content, date_posted=date_posted)
        # db.session.add(new_announcement)
        # db.session.commit()

        flash(f"Announcement '{title}' added successfully!", "success")
        return redirect(url_for("admin.adminannouncement"))

    return render_template("admin_addanouncement.html", title="Add Announcement")

@admin_bp.route("/adminsettings")
@admin_required
def adminsettings():
    return render_template("admin_settings.html", title="Settings")
