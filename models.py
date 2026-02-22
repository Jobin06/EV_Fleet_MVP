from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserAccount(db.Model):
    __tablename__ = 'user_account'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Integer, default=0, nullable=False) # 1 for True, 0 for False (Oracle compatibility)

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    
    id = db.Column(db.String(50), primary_key=True)
    driver_name = db.Column(db.String(100))
    status = db.Column(db.String(50), default='INACTIVE', nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    battery_pack = db.relationship('BatteryPack', back_populates='vehicle', uselist=False, cascade='all, delete-orphan')
    telemetry_records = db.relationship('Telemetry', back_populates='vehicle', cascade='all, delete-orphan')
    charging_sessions = db.relationship('ChargingSession', back_populates='vehicle', cascade='all, delete-orphan')
    trips = db.relationship('Trip', back_populates='vehicle', cascade='all, delete-orphan')
    alerts = db.relationship('Alert', back_populates='vehicle', cascade='all, delete-orphan')

class BatteryPack(db.Model):
    __tablename__ = 'battery_pack'
    
    id = db.Column(db.String(50), primary_key=True)
    vehicle_id = db.Column(db.String(50), db.ForeignKey('vehicle.id', ondelete='CASCADE'), unique=True, nullable=False)
    capacity_kwh = db.Column(db.Float, nullable=False) # Maps roughly to NUMBER in Oracle
    
    vehicle = db.relationship('Vehicle', back_populates='battery_pack')

class Telemetry(db.Model):
    __tablename__ = 'telemetry'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(50), db.ForeignKey('vehicle.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    soc = db.Column(db.Float, nullable=False) # State of Charge %
    pack_voltage = db.Column(db.Float)
    pack_current = db.Column(db.Float)
    temperature = db.Column(db.Float)
    
    vehicle = db.relationship('Vehicle', back_populates='telemetry_records')

class ChargingSession(db.Model):
    __tablename__ = 'charging_session'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(50), db.ForeignKey('vehicle.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    energy_added_kwh = db.Column(db.Float)
    charging_type = db.Column(db.String(50))
    status = db.Column(db.String(50), default='CHARGING', nullable=False)
    
    vehicle = db.relationship('Vehicle', back_populates='charging_sessions')

class Trip(db.Model):
    __tablename__ = 'trip'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(50), db.ForeignKey('vehicle.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    distance_km = db.Column(db.Float)
    energy_used_kwh = db.Column(db.Float)
    
    vehicle = db.relationship('Vehicle', back_populates='trips')

class Alert(db.Model):
    __tablename__ = 'alert'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(50), db.ForeignKey('vehicle.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    alert_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='ACTIVE', nullable=False)
    
    vehicle = db.relationship('Vehicle', back_populates='alerts')
