import sqlite3
import os
from contextlib import closing
import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'admin'
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT NOT NULL,
    predicted_class TEXT NOT NULL,
    confidence REAL NOT NULL,
    status TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""


def get_conn():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
    with closing(get_conn()) as conn:
        conn.executescript(SCHEMA)
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(predictions)")}
        if "feedback_correct" not in cols:      # 1 = correct, 0 = wrong, NULL = no feedback
            conn.execute("ALTER TABLE predictions ADD COLUMN feedback_correct INTEGER")
        if "corrected_label" not in cols:
            conn.execute("ALTER TABLE predictions ADD COLUMN corrected_label TEXT")
        conn.commit()


def save_prediction(image_path, label, confidence, status):
    with closing(get_conn()) as conn:
        cur = conn.execute(
            "INSERT INTO predictions (image_path, predicted_class, confidence, status) "
            "VALUES (?, ?, ?, ?)",
            (image_path, label, confidence, status),
        )
        conn.commit()
        return cur.lastrowid


def set_feedback(pid, correct, corrected_label):
    with closing(get_conn()) as conn:
        conn.execute(
            "UPDATE predictions SET feedback_correct = ?, corrected_label = ? WHERE id = ?",
            (1 if correct else 0, corrected_label, pid),
        )
        conn.commit()


def get_user(username):
    with closing(get_conn()) as conn:
        return conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()


def get_labels():
    with closing(get_conn()) as conn:
        return [r[0] for r in conn.execute(
            "SELECT DISTINCT predicted_class FROM predictions ORDER BY predicted_class")]


def _filters(label, status):
    where, params = [], []
    if label:
        where.append("predicted_class = ?")
        params.append(label)
    if status:
        where.append("status = ?")
        params.append(status)
    clause = ("WHERE " + " AND ".join(where)) if where else ""
    return clause, params


def get_history(page=1, per_page=20, label=None, status=None):
    clause, params = _filters(label, status)
    offset = (page - 1) * per_page
    with closing(get_conn()) as conn:
        total = conn.execute(f"SELECT COUNT(*) FROM predictions {clause}", params).fetchone()[0]
        rows = conn.execute(
            f"SELECT *, datetime(created_at, 'localtime') AS local_time "
            f"FROM predictions {clause} ORDER BY id DESC LIMIT ? OFFSET ?",
            params + [per_page, offset],
        ).fetchall()
    return rows, total


def get_all():
    with closing(get_conn()) as conn:
        return conn.execute(
            "SELECT *, datetime(created_at, 'localtime') AS local_time "
            "FROM predictions ORDER BY id"
        ).fetchall()


def delete_prediction(pid):
    """Delete a row and return its image filename so the file can be removed too."""
    with closing(get_conn()) as conn:
        row = conn.execute("SELECT image_path FROM predictions WHERE id = ?", (pid,)).fetchone()
        if not row:
            return None
        conn.execute("DELETE FROM predictions WHERE id = ?", (pid,))
        conn.commit()
        return row["image_path"]


def get_stats():
    with closing(get_conn()) as conn:
        total = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
        by_class = conn.execute(
            "SELECT predicted_class AS label, COUNT(*) AS n FROM predictions "
            "GROUP BY predicted_class ORDER BY n DESC").fetchall()
        by_status = conn.execute(
            "SELECT status, COUNT(*) AS n FROM predictions GROUP BY status").fetchall()
        daily = conn.execute(
            "SELECT date(created_at, 'localtime') AS day, COUNT(*) AS n "
            "FROM predictions GROUP BY day ORDER BY day DESC LIMIT 14").fetchall()
        avg_conf = conn.execute("SELECT AVG(confidence) FROM predictions").fetchone()[0]
        reviewed, correct = conn.execute(
            "SELECT COUNT(feedback_correct), COALESCE(SUM(feedback_correct), 0) FROM predictions"
        ).fetchone()
        mistakes = conn.execute(
            "SELECT predicted_class AS predicted, corrected_label AS actual, COUNT(*) AS n "
            "FROM predictions WHERE feedback_correct = 0 AND corrected_label IS NOT NULL "
            "GROUP BY predicted_class, corrected_label ORDER BY n DESC LIMIT 5").fetchall()

    daily = list(reversed(daily))
    return {
        "total": total,
        "avg_confidence": round((avg_conf or 0) * 100, 1),
        "classes": [r["label"] for r in by_class],
        "class_counts": [r["n"] for r in by_class],
        "top_class": by_class[0]["label"] if by_class else "-",
        "statuses": {r["status"]: r["n"] for r in by_status},
        "days": [r["day"] for r in daily],
        "day_counts": [r["n"] for r in daily],
        "reviewed": reviewed,
        "correct": int(correct),
        "feedback_acc": round(correct / reviewed * 100, 1) if reviewed else None,
        "mistakes": [dict(r) for r in mistakes],
    }