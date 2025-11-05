from fastapi import Depends, HTTPException, Header
from db import get_conn

def login_user(username: str, password: str):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(401, "invalid credentials")
    return {"token": f"demo-{row['username']}", "role": row["role"], "username": row["username"]}

def get_current_role(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(401, "missing auth")
    # demo token format: "Bearer demo-username"
    token = authorization.replace("Bearer ", "")
    if not token.startswith("demo-"):
        raise HTTPException(401, "invalid token")
    username = token.split("demo-")[-1]
    conn = get_conn()
    row = conn.execute("SELECT role FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(401, "invalid user")
    return row["role"]
