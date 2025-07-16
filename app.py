# app.py
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from gpt import get_response
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# ---------------------- Models ----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------------- Login Required Decorator ----------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.endpoint == 'get_bot_response':
                return "Please log in to use the chat."
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------- Routes ----------------------
@app.route("/")
def dashboard():
    return render_template("index.html", user_id=session.get('user_id'))

@app.route("/get", methods=["GET"])
@login_required
def get_bot_response():
    user_text = request.args.get("msg")
    try:
        reply = get_response(user_text)
        new_entry = ChatHistory(user_id=session['user_id'], message=user_text, response=reply)
        db.session.add(new_entry)
        db.session.commit()
        return reply
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"

# -----------------------------------------------History-----------------------------------------------
@app.route("/history")
@login_required
def history():
    chats = ChatHistory.query.filter_by(user_id=session['user_id']).order_by(ChatHistory.timestamp.desc()).all()
    return render_template("history.html", chats=chats)

@app.route("/search")
@login_required
def search():
    query = request.args.get("q")
    if not query:
        return redirect(url_for("history"))
    results = ChatHistory.query.filter(ChatHistory.user_id==session['user_id'], ChatHistory.message.contains(query)).order_by(ChatHistory.timestamp.desc()).all()
    return render_template("history.html", chats=results, query=query)
# -----------------------------------------------Register-----------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("password1")

        if not email or not password:
            return render_template("register.html", error="Email and password are required.")

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("register.html", error="Email already registered")

        try:
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful!", "success")
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            return render_template("register.html", error=f"Database error: {str(e)}")

    return render_template("register.html")
# ------------------------------------------------Login-------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")
# -----------------------------------------------Logout-----------------------------------------------
@app.route("/logout")
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for("dashboard"))
# ----------------------------------------------Profile-------------------------------------------------
@app.route("/profile")
@login_required
def profile():
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('logout'))
    return render_template("profile.html", user=user)

# ---------------------------------------------Update Profile---------------------------------------------    
@app.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile():
    user = User.query.get(session["user_id"])
    
    if request.method == "POST":
        new_email = request.form.get("email")
        new_password = request.form.get("password")
        confirm_password = request.form.get("password1")

        if not new_email:
            flash("Email cannot be empty.", "danger")
            return redirect(url_for("update_profile"))

        if new_password and new_password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("update_profile"))

        # Check for existing user with same email
        if new_email != user.email and User.query.filter_by(email=new_email).first():
            flash("Email already in use by another account.", "danger")
            return redirect(url_for("update_profile"))

        # Update fields
        user.email = new_email
        if new_password:
            user.password_hash = generate_password_hash(new_password)

        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating profile: {str(e)}", "danger")

        return redirect(url_for("profile"))

    return render_template("update_profile.html", user=user)

# ---------------------- Main ----------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
