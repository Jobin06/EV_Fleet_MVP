from app import app
from models import db, UserAccount, Vehicle, BatteryPack, Telemetry, ChargingSession, Trip, Alert
from datetime import datetime, timedelta
import random

def seed_database():
    with app.app_context():
        # WARNING: In a real Oracle setup with existing data, handle dropping tables carefully.
        # db.drop_all() # Uncomment to clear existing schema during dev (if SQLAlchemy manages it)
        # db.create_all() # Create tables if not already created via SQL script
        
        print("Starting seed...")

        # Create Admin
        if not UserAccount.query.filter_by(username='admin').first():
            admin = UserAccount(username='admin', password_hash='admin', is_admin=1)
            db.session.add(admin)
        
        # Create Vehicles
        vehicles_data = [
            {'id': 'EV-1001', 'driver': 'Alice Smith', 'status': 'ACTIVE'},
            {'id': 'EV-1002', 'driver': 'Bob Jones', 'status': 'CHARGING'},
            {'id': 'EV-1003', 'driver': 'Charlie Brown', 'status': 'INACTIVE'}
        ]
        
        added_vehicles = []
        for v_data in vehicles_data:
            if not Vehicle.query.get(v_data['id']):
                v = Vehicle(id=v_data['id'], driver_name=v_data['driver'], status=v_data['status'])
                db.session.add(v)
                added_vehicles.append(v)
                
                # Add Battery Pack
                pack = BatteryPack(id=f"BP-{v_data['id'][3:]}", vehicle_id=v.id, capacity_kwh=random.choice([60.0, 75.0, 100.0]))
                db.session.add(pack)

        db.session.commit()
        print("Vehicles and Packs added.")

        # Create Telemetry
        now = datetime.utcnow()
        for v in Vehicle.query.all():
            base_soc = random.uniform(20.0, 90.0)
            if v.status == 'CHARGING':
                base_soc = 40.0
                
            for i in range(20):
                # Simulate time series data
                timestamp = now - timedelta(minutes=(20-i)*5)
                # JUMPING SoC changes to make the graph look more interesting
                if v.status == 'CHARGING':
                    soc_variance = (i * random.uniform(1.0, 3.0)) 
                else:
                    soc_variance = -(i * random.uniform(0.5, 4.0)) 
                    
                current_soc = min(max(base_soc + soc_variance, 0), 100)
                
                t = Telemetry(
                    vehicle_id=v.id,
                    timestamp=timestamp,
                    soc=current_soc,
                    pack_voltage=350.0 + random.uniform(-10, 10),
                    pack_current=random.uniform(5.0, 50.0) if v.status == 'ACTIVE' else (random.uniform(-100, -50) if v.status == 'CHARGING' else 0.0),
                    temperature=25.0 + random.uniform(-5, 10)
                )
                db.session.add(t)

        # Create Charging Sessions
        for v in Vehicle.query.all():
            if random.choice([True, False]): # Randomly assign some history
                cs = ChargingSession(
                    vehicle_id=v.id,
                    start_time=now - timedelta(days=1),
                    end_time=now - timedelta(days=1) + timedelta(hours=2),
                    energy_added_kwh=random.uniform(10.0, 40.0),
                    charging_type=random.choice(['Level 2', 'DCFC', 'Level 1']),
                    status='COMPLETED'
                )
                db.session.add(cs)
            
            if v.status == 'CHARGING':
                cs_active = ChargingSession(
                    vehicle_id=v.id,
                    start_time=now - timedelta(hours=1),
                    charging_type='DCFC',
                    status='CHARGING'
                )
                db.session.add(cs_active)

        # Create Alerts
        v = Vehicle.query.first()
        if v:
            a1 = Alert(vehicle_id=v.id, timestamp=now - timedelta(minutes=10), alert_type='Low Tire Pressure', status='ACTIVE')
            a2 = Alert(vehicle_id=v.id, timestamp=now - timedelta(days=2), alert_type='Battery Temperature High', status='RESOLVED')
            db.session.add(a1)
            db.session.add(a2)

        db.session.commit()
        print("Seed data successfully added!")

if __name__ == '__main__':
    seed_database()
