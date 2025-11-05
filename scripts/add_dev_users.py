import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api', 'app', 'glucose.db')
# Fallback: if the above path doesn't exist, try current directory glucose.db
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'api', 'app', 'glucose.db')
    DB_PATH = os.path.abspath(DB_PATH)

print('Using DB path:', DB_PATH)
con = sqlite3.connect(DB_PATH)
con.row_factory = sqlite3.Row
cur = con.cursor()
users = [
    ('dr_jones','docpass','doctor'),
    ('patient_al','patientpass','patient')
]
for u,p,r in users:
    try:
        cur.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)", (u,p,r))
        print(f'Inserted user: {u} role={r}')
    except Exception as e:
        print(f'Skipped {u} (may already exist):', e)
con.commit()
# show users table rows for verification
print('\nCurrent users:')
for row in cur.execute('SELECT id, username, role FROM users'): 
    print(dict(row))
con.close()
