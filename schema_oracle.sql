-- ==========================================
-- Oracle 11g Compatible Schema
-- EV Fleet MVP
-- ==========================================

------------------------------------------------
-- USER ACCOUNT
------------------------------------------------
CREATE TABLE user_account (
    id NUMBER PRIMARY KEY,
    username VARCHAR2(50) UNIQUE NOT NULL,
    password_hash VARCHAR2(255) NOT NULL,
    is_admin NUMBER(1) DEFAULT 0 NOT NULL
);

CREATE SEQUENCE user_account_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER user_account_trg
BEFORE INSERT ON user_account
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT user_account_seq.NEXTVAL
        INTO :NEW.id
        FROM dual;
    END IF;
END;
/

------------------------------------------------
-- VEHICLE (No identity needed, using VARCHAR PK)
------------------------------------------------
CREATE TABLE vehicle (
    id VARCHAR2(50) PRIMARY KEY,
    driver_name VARCHAR2(100),
    status VARCHAR2(50) DEFAULT 'INACTIVE' NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

------------------------------------------------
-- BATTERY PACK
------------------------------------------------
CREATE TABLE battery_pack (
    id VARCHAR2(50) PRIMARY KEY,
    vehicle_id VARCHAR2(50) UNIQUE NOT NULL,
    capacity_kwh NUMBER(10, 2) NOT NULL,
    CONSTRAINT fk_battery_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicle(id)
        ON DELETE CASCADE
);

------------------------------------------------
-- TELEMETRY
------------------------------------------------
CREATE TABLE telemetry (
    id NUMBER PRIMARY KEY,
    vehicle_id VARCHAR2(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    soc NUMBER(5, 2) NOT NULL,
    pack_voltage NUMBER(10, 2),
    pack_current NUMBER(10, 2),
    temperature NUMBER(5, 2),
    CONSTRAINT fk_telemetry_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicle(id)
        ON DELETE CASCADE
);

CREATE SEQUENCE telemetry_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER telemetry_trg
BEFORE INSERT ON telemetry
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT telemetry_seq.NEXTVAL
        INTO :NEW.id
        FROM dual;
    END IF;
END;
/

------------------------------------------------
-- CHARGING SESSION
------------------------------------------------
CREATE TABLE charging_session (
    id NUMBER PRIMARY KEY,
    vehicle_id VARCHAR2(50) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    energy_added_kwh NUMBER(10, 2),
    charging_type VARCHAR2(50),
    status VARCHAR2(50) DEFAULT 'CHARGING' NOT NULL,
    CONSTRAINT fk_charging_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicle(id)
        ON DELETE CASCADE
);

CREATE SEQUENCE charging_session_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER charging_session_trg
BEFORE INSERT ON charging_session
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT charging_session_seq.NEXTVAL
        INTO :NEW.id
        FROM dual;
    END IF;
END;
/

------------------------------------------------
-- TRIP
------------------------------------------------
CREATE TABLE trip (
    id NUMBER PRIMARY KEY,
    vehicle_id VARCHAR2(50) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    distance_km NUMBER(10, 2),
    energy_used_kwh NUMBER(10, 2),
    CONSTRAINT fk_trip_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicle(id)
        ON DELETE CASCADE
);

CREATE SEQUENCE trip_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER trip_trg
BEFORE INSERT ON trip
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT trip_seq.NEXTVAL
        INTO :NEW.id
        FROM dual;
    END IF;
END;
/

------------------------------------------------
-- ALERT
------------------------------------------------
CREATE TABLE alert (
    id NUMBER PRIMARY KEY,
    vehicle_id VARCHAR2(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    alert_type VARCHAR2(100) NOT NULL,
    status VARCHAR2(50) DEFAULT 'ACTIVE' NOT NULL,
    CONSTRAINT fk_alert_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicle(id)
        ON DELETE CASCADE
);

CREATE SEQUENCE alert_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER alert_trg
BEFORE INSERT ON alert
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT alert_seq.NEXTVAL
        INTO :NEW.id
        FROM dual;
    END IF;
END;
/

COMMIT;