# EV Fleet Management Dashboard MVP

This is an academic Minimum Viable Product (MVP) demonstrating an EV Fleet Management dashboard. It is designed to be simple, clean, and beginner-friendly, avoiding complex frontend frameworks or advanced architectural patterns.

## Tech Stack
- **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript, Chart.js
- **Backend**: Python 3.10+, Flask
- **Database**: Oracle 11g (via SQL*Plus / oracledb)
- **ORM**: SQLAlchemy

## Project Structure
- `app.py`: Main Flask application handling routes and logic.
- `models.py`: SQLAlchemy models mirroring the Oracle DB schema.
- `seed_data.py`: A helper script to populate the Dev Database with dummy EV telemetry.
- `schema_oracle.sql`: The raw Oracle SQL code for manual database setup.
- `requirements.txt`: Python package dependencies.
- `templates/`: Jinja2 UI templates.
- `static/css/ & static/js/`: Vanilla frontend assets.

## Detailed Setup Instructions

Follow these steps exactly to run the MVP on your local machine.

### Prerequisites
Before you begin, ensure you have the following installed on your system:
1.  **Python 3.10 or higher**: Download from [python.org](https://www.python.org/downloads/).
2.  **Oracle Database 11g Express Edition (XE)**: Or access to any Oracle 11g database instance.

---

### Step 1: Database Setup (Oracle 11g)
We need to create the tables in your Oracle database where the application will store its data.

1.  Open your command prompt or terminal.
2.  Launch the SQL*Plus tool and connect to your database as an administrator:
    ```bash
    sqlplus sys as sysdba
    ```
    *(You will be prompted to enter your SYS password.)*
3.  **(Optional but recommended)** Create a dedicated user for this application so you don't use the SYS account. Run these commands inside SQL*Plus:
    ```sql
    CREATE USER fleet_admin IDENTIFIED BY fleet_password;
    GRANT CONNECT, RESOURCE, DBA TO fleet_admin;
    ```
4.  Connect to this newly created user:
    ```sql
    CONNECT fleet_admin/fleet_password;
    ```
5.  Run the schema script to create all the necessary tables. Assuming your command line is open in the project folder (`j:\Code\Projects\EV_Fleet_MVP`):
    ```sql
    @schema_oracle.sql
    ```
    *If successful, it will say "Table created" multiple times.* You can then exit SQL*Plus by typing `EXIT`.

---

### Step 2: Python Environment Setup
We will set up a virtual environment to keep the project's Python packages separate from your system-wide packages.

1.  Open your command prompt or PowerShell and navigate to the project folder:
    ```bash
    cd j:\Code\Projects\EV_Fleet_MVP
    ```
2.  Create a virtual environment named `venv`:
    ```bash
    python -m venv venv
    ```
3.  Activate the virtual environment. **You must do this every time you work on the project.**
    - **On Windows:**
      ```bash
      venv\Scripts\activate
      ```
    - **On macOS/Linux:**
      ```bash
      source venv/bin/activate
      ```
    *(You should see `(venv)` appear at the beginning of your command prompt line.)*

4.  Install the required Python packages into this virtual environment:
    ```bash
    pip install -r requirements.txt
    ```

---

### Step 3: Install Oracle Instant Client (Required for `oracledb` Thick Mode)
The `oracledb` library works in "Thin" mode out of the box, but if you need advanced Oracle features or older database support, it might require the Oracle Instant Client.
*   **Most modern Setups**: You can usually skip this step as `oracledb` installs a Thin driver natively!

---

### Step 4: Application Configuration
The Flask application needs to know how to connect to your database. It looks for environment variables.

If you used the credentials from Step 1 (`fleet_admin` / `fleet_password`) and the database is on your machine (`localhost`), you don't need to change anything because `app.py` has these as defaults.

If your credentials or host are different, you can either:
**Option A (Recommended):** Set environment variables in your command prompt before running the app:
*   On Windows cmd:
    ```cmd
    set ORACLE_USER=your_username
    set ORACLE_PASS=your_password
    set ORACLE_DSN=your_host:1521/your_service_name
    ```
*   On PowerShell:
    ```powershell
    $env:ORACLE_USER="your_username"
    $env:ORACLE_PASS="your_password"
    $env:ORACLE_DSN="your_host:1521/your_service_name"
    ```

**Option B (Easy but less secure):** Edit `app.py` directly (around line 12) and change the default string values.

---

### Step 5: Seed Dummy Data
Your database is currently empty. Let's add some fake vehicles, charging sessions, and telemetry data so the dashboard has something to show.

1.  Run the seed script:
    ```bash
    python seed_data.py
    ```
    *(Note: You might see a Warning about "Failed to initialize Oracle Client (Thick mode)" if the client isn't fully set up, but oracledb will gracefully fall back to Thin mode if connecting to newer databases).*
    *You should see output indicating successful seeding.*

---

### Step 6: Run the Application
Finally, start the web server!

1.  Run the Flask app:
    ```bash
    python app.py
    ```
2.  You should see output saying the server is running on `http://127.0.0.1:5000` or `http://0.0.0.0:5000`.
3.  Open your web browser and navigate to: [http://localhost:5000](http://localhost:5000)

### Step 7: Log In
You can access the dashboard using the hardcoded default credentials:
- **Username:** `admin`
- **Password:** `admin`

---

## Daily Workflow (How to start the app after a system restart)

Whenever you restart your computer or close your command prompt, you don't need to reinstall everything. Just follow these 4 simple steps to start the dashboard again:

1. **Open your Command Prompt (or PowerShell).**
2. **Navigate to the project folder:**
   ```bash
   cd j:\Code\Projects\EV_Fleet_MVP
   ```
3. **Activate the virtual environment:**
   ```bash
   venv\Scripts\activate
   ```
   *(You should see `(venv)` appear in your prompt)*
4. **Run the application:**
   ```bash
   python app.py
   ```
5. **Open your browser** and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)
