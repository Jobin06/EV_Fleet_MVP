from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, UserAccount, Vehicle, BatteryPack, Telemetry, ChargingSession, Trip, Alert
from sqlalchemy.sql import func
import os

import oracledb

app = Flask(__name__)
app.secret_key = 'super_secret_academic_mvp_key'  # Used for session based auth

# Init oracledb thick mode to support Oracle 11g
try:
    oracledb.init_oracle_client()
except Exception as e:
    print("Warning: Failed to initialize Oracle Client (Thick mode). Is it installed and in PATH?", e)

# Oracle Connection Configuration
# NOTE: Replace 'username', 'password', and 'oracle_host:port/service_name' with your actual Oracle DB credentials.
# Ensure cx_Oracle is installed and the Oracle Instant Client is accessible in your system PATH.
oracle_user = os.environ.get('ORACLE_USER', 'fleet_admin')
oracle_pass = os.environ.get('ORACLE_PASS', 'fleet_password')
oracle_dsn = os.environ.get('ORACLE_DSN', 'localhost:1521/XE')

app.config['SQLALCHEMY_DATABASE_URI'] = f'oracle+oracledb://{oracle_user}:{oracle_pass}@{oracle_dsn}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Authentication Middleware
@app.before_request
def require_login():
    # If not logged in and not accessing login page/static files
    allowed_routes = ['login', 'static']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication
        user = UserAccount.query.filter_by(username=username).first()
        # For this MVP, we are not using complex password hashing checking (just checking string match or hardcoded logic)
        # Using a very simple check for academic purposes
        if user and user.password_hash == password:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        elif username == 'admin' and password == 'admin': # Hardcoded fallback admin
            session['user_id'] = 0
            session['username'] = 'admin'
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
def dashboard():
    # Fetch MVP Dashboard Stats
    total_vehicles = Vehicle.query.count()
    active_vehicles = Vehicle.query.filter_by(status='ACTIVE').count()
    charging_vehicles = Vehicle.query.filter_by(status='CHARGING').count()
    
    # Calculate fleet average SoC
    latest_telemetry_subquery = db.session.query(
        Telemetry.vehicle_id, 
        func.max(Telemetry.timestamp).label('max_time')
    ).group_by(Telemetry.vehicle_id).subquery()
    
    fleet_soc_query = db.session.query(func.avg(Telemetry.soc)).join(
        latest_telemetry_subquery,
        db.and_(
            Telemetry.vehicle_id == latest_telemetry_subquery.c.vehicle_id,
            Telemetry.timestamp == latest_telemetry_subquery.c.max_time
        )
    ).scalar()
    
    avg_soc = round(fleet_soc_query, 1) if fleet_soc_query else 0.0
    
    active_alerts = Alert.query.filter_by(status='ACTIVE').count()
    
    # Fetch vehicles for table
    vehicles = Vehicle.query.all()
    
    # Attach latest SoC to vehicle objects for the table
    for v in vehicles:
        latest_tel = Telemetry.query.filter_by(vehicle_id=v.id).order_by(Telemetry.timestamp.desc()).first()
        v.current_soc = latest_tel.soc if latest_tel else 'N/A'

    return render_template('dashboard.html', 
                           total_vehicles=total_vehicles,
                           active_vehicles=active_vehicles,
                           charging_vehicles=charging_vehicles,
                           avg_soc=avg_soc,
                           active_alerts=active_alerts,
                           vehicles=vehicles)

@app.route('/vehicle/<vehicle_id>')
def vehicle_detail(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    pack = vehicle.battery_pack
    
    latest_tel = Telemetry.query.filter_by(vehicle_id=vehicle_id).order_by(Telemetry.timestamp.desc()).first()
    
    # Get telemetry data for the chart (last 20 records)
    recent_telemetry = Telemetry.query.filter_by(vehicle_id=vehicle_id).order_by(Telemetry.timestamp.desc()).limit(20).all()
    recent_telemetry.reverse() # Chronological order
    
    chart_labels = [t.timestamp.strftime('%H:%M:%S') for t in recent_telemetry]
    chart_data = [t.soc for t in recent_telemetry]

    return render_template('vehicle_detail.html', 
                           vehicle=vehicle, 
                           pack=pack, 
                           telemetry=latest_tel,
                           chart_labels=chart_labels,
                           chart_data=chart_data)

@app.route('/charging_history')
def charging_history():
    sessions = ChargingSession.query.order_by(ChargingSession.start_time.desc()).all()
    return render_template('charging_history.html', sessions=sessions)

@app.route('/alerts')
def alerts():
    all_alerts = Alert.query.order_by(Alert.timestamp.desc()).all()
    return render_template('alerts.html', alerts=all_alerts)

if __name__ == '__main__':
    # Run server
    app.run(debug=True, host='0.0.0.0', port=5000)
