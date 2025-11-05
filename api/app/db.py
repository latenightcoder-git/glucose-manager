import sqlite3, os
DB_PATH = os.getenv("DB_PATH", "glucose.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT);
    CREATE TABLE IF NOT EXISTS patients(
      id INTEGER PRIMARY KEY, name TEXT, age INT, sensitivity REAL);
    CREATE TABLE IF NOT EXISTS readings(
      id INTEGER PRIMARY KEY, patient_id INT, glucose REAL, insulin REAL,
      carbs REAL, activity REAL, note TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP);
    INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin');
    """)
    # If there are no patients yet, seed a couple for local dev
    cur = conn.execute("SELECT COUNT(1) as c FROM patients")
    row = cur.fetchone()
    if row is None or row[0] == 0:
        conn.executescript("""
        INSERT INTO patients (name, age, sensitivity) VALUES
          ('John Doe', 45, 1.2),
          ('Jane Smith', 32, 1.0);
        INSERT INTO readings (patient_id, glucose, insulin, carbs, activity, note) VALUES
          (1, 120.5, 5.0, 45.0, 2.0, 'Post breakfast reading'),
          (1, 95.0, 0.0, 0.0, 1.0, 'Fasting reading'),
          (2, 110.0, 4.0, 30.0, 1.5, 'Lunch reading');
        """)
    conn.commit()
    conn.close()
