-- Create tables (idempotent for local dev)
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS patients (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  age INTEGER NOT NULL,
  sensitivity REAL NOT NULL DEFAULT 1.0
);

CREATE TABLE IF NOT EXISTS readings (
  id INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL,
  glucose REAL NOT NULL,
  insulin REAL NOT NULL,
  carbs REAL NOT NULL DEFAULT 0.0,
  activity REAL NOT NULL DEFAULT 0.0,
  note TEXT,
  ts DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(patient_id) REFERENCES patients(id)
);

-- Seed demo users (plaintext only for local dev)
INSERT OR IGNORE INTO users (id, username, password, role) VALUES
  (1, 'doctor1', 'pass', 'doctor'),
  (2, 'nurse1',  'pass', 'nurse'),
  (3, 'patient1','pass', 'patient'),
  (4, 'family1', 'pass', 'family');

-- Seed patients
INSERT OR IGNORE INTO patients (id, name, age, sensitivity) VALUES
  (1, 'Alice Carter', 45, 1.0),
  (2, 'Bob Singh',    34, 1.2);

-- Seed readings (light history)
INSERT INTO readings (patient_id, glucose, insulin, carbs, activity, note) VALUES
  (1, 178, 0.0,  0, 0.2, 'baseline'),
  (1, 165, 1.0,  0, 0.0, 'post correction'),
  (1, 140, 0.0, 30, 0.0, 'meal'),
  (1, 155, 0.5,  0, 0.5, 'walk'),
  (2, 190, 0.0,  0, 0.3, 'baseline');
