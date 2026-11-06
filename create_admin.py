from getpass import getpass
from werkzeug.security import generate_password_hash
from utils.db import init_db, get_conn
from contextlib import closing

init_db()
username = input("Admin username: ").strip()
password = getpass("Admin password (min 8 characters): ")

if len(password) < 8:
    raise SystemExit("Password too short.")

with closing(get_conn()) as conn:
    conn.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'admin')",
        (username, generate_password_hash(password)),
    )
    conn.commit()
print("Admin created.")