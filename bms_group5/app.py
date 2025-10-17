from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
from admin.routes import admin_bp

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this'  # Change this to a random secret key

app.register_blueprint(admin_bp, url_prefix="/admin")

# Dummy admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "cadaypogi"

# Temporary user storage (use database in production)
users = {
    'admin': generate_password_hash('admin123')
}

@app.route('/')
def splash():
    """Splash screen"""
    return render_template('splash.html')

@app.route('/home')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        # --- Admin login ---
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['username'] = username
            session.permanent = True if remember else False
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('admin.admindashboard'))

        # --- Normal resident login ---
        elif username in users and check_password_hash(users[username], password):
            session['user'] = username
            session.permanent = True if remember else False
            flash('Matagumpay na nag-login!', 'success')
            return redirect(url_for('dashboard'))

        else:
            flash('Mali ang username o password.', 'error')
            return redirect(url_for('login'))
    
    return render_template('residents/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate registration
        if username in users:
            flash('Username ay ginagamit na.', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Hindi tugma ang mga password.', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        users[username] = generate_password_hash(password)
        flash('Matagumpay na nag-register! Mag-login na.', 'success')
        return redirect(url_for('login'))
    
    return render_template('residents/register.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page (requires login)"""
    if 'user' not in session:
        flash('Kailangan mag-login muna.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('residents/resident_dashboard.html', username=session['user'])

@app.route("/announcement")
def announcement():
    if 'user' not in session:
        flash('Kailangan mag-login muna.', 'warning')
        return redirect(url_for('login'))
    return render_template("residents/announcement.html")

@app.route("/certificates")
def certificates():
    if 'user' not in session:
        flash('Kailangan mag-login muna.', 'warning')
        return redirect(url_for('login'))
    return render_template("residents/certificates.html")

@app.route("/complaints")
def complaints():
    if 'user' not in session:
        flash('Kailangan mag-login muna.', 'warning')
        return redirect(url_for('login'))
    return render_template("residents/complaint.html")

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        username = request.form.get('username')
        # TODO: Save the username to database or file
        print(f"Saved username: {username}")
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('residents/settings.html')


@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    session.pop("username", None)
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route('/forgot-password')
def forgot_password():
    """Forgot password page"""
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)