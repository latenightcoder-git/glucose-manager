-- Initial seed data
INSERT OR IGNORE INTO users (username, password, role) 
VALUES ('admin', 'admin123', 'admin');

INSERT OR IGNORE INTO patients (name, age, sensitivity) 
VALUES 
('John Doe', 45, 1.2),
('Jane Smith', 32, 1.0);

INSERT OR IGNORE INTO readings (patient_id, glucose, insulin, carbs, activity, note)
VALUES 
(1, 120.5, 5.0, 45.0, 2.0, 'Post breakfast reading'),
(1, 95.0, 0.0, 0.0, 1.0, 'Fasting reading'),
(2, 110.0, 4.0, 30.0, 1.5, 'Lunch reading');