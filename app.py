from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kalavara.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define models
class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    dish_name = db.Column(db.String(100), nullable=False)

class AdminView(db.Model):
    __tablename__ = 'admin_view'
    id = db.Column(db.Integer, primary_key=True)
    total_dishes = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Function to add a dish
def add_dish(user_id, dish_name):
    new_dish = Dish(user_id=user_id, dish_name=dish_name)
    db.session.add(new_dish)
    db.session.commit()

    # Update admin view
    admin_view = AdminView.query.get(1)
    if admin_view:
        admin_view.total_dishes = Dish.query.count()
        admin_view.updated_at = datetime.utcnow()
        db.session.commit()

# Function to fetch admin summary
def get_admin_summary():
    admin_view = AdminView.query.get(1)
    return (admin_view.total_dishes, admin_view.updated_at) if admin_view else (0, None)

# User dashboard route
@app.route('/dashboard_user', methods=['GET', 'POST'])
def dashboard_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        dish_name = request.form['dish_name']
        add_dish(user_id, dish_name)
    return render_template('dashboard_user.html')

# Admin dashboard route
@app.route('/dashboard_admin', methods=['GET'])
def dashboard_admin():
    total_dishes, updated_at = get_admin_summary()
    return render_template('dashboard_admin.html', total_dishes=total_dishes, updated_at=updated_at)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)

from waitress import serve
from app import app

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)

