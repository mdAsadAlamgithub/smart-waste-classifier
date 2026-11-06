from getpass import getpass
from contextlib import closing
from werkzeug.security import generate_password_hash
from utils.db import init_db, get_conn

init_db()
username = input("Admin username: ").strip()
password = getpass("New password (min 8 characters): ")

if len(password) < 8:
    raise SystemExit("Password too short.")

with closing(get_conn()) as conn:
    row = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    hashed = generate_password_hash(password)
    if row:
        conn.execute("UPDATE users SET password_hash = ? WHERE username = ?", (hashed, username))
        print("Password updated.")
    else:
        conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'admin')",
            (username, hashed),
        )
        print("Admin created.")
    conn.commit()