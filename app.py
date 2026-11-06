import os
import io
import csv
import uuid
import random
from functools import wraps
from flask import (Flask, render_template, request, redirect, url_for,
                   flash, session, jsonify, Response)
from PIL import Image
from werkzeug.security import check_password_hash

import config
from utils.classifier import predict, load
from utils.recommendations import (get_recommendation, DISCLAIMER,
                                   CATEGORIES, CATEGORY_MAP, ECO_TIPS)
from utils import db

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
db.init_db()
load()


@app.context_processor
def inject_globals():
    return {"CATEGORIES": CATEGORIES, "CAT": CATEGORY_MAP}


def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS


def is_valid_image(path):
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False


def valid_labels():
    return sorted(set(load()[1]) | {"other"})


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Please log in as admin.")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


# ---------- Public pages ----------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/guide")
def guide():
    return render_template("guide.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/predict", methods=["POST"])
def predict_route():
    file = request.files.get("image")
    if not file or file.filename == "":
        flash("Please choose an image first.")
        return redirect(url_for("index"))
    if not allowed(file.filename):
        flash("Only JPG, JPEG and PNG images are allowed.")
        return redirect(url_for("index"))

    ext = file.filename.rsplit(".", 1)[1].lower()
    name = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(config.UPLOAD_FOLDER, name)
    file.save(path)

    if not is_valid_image(path):
        os.remove(path)
        flash("That file is not a valid image.")
        return redirect(url_for("index"))

    results = predict(path)
    top = results[0]

    if top["label"] == "other":
        status = "other"
    elif top["confidence"] < config.CONFIDENCE_THRESHOLD:
        status = "uncertain"
    else:
        status = "ok"

    pid = db.save_prediction(name, top["label"], top["confidence"], status)
    session["last_pred"] = pid          # only this prediction can receive feedback

    return render_template(
        "result.html",
        image_name=name,
        results=results,
        top=top,
        status=status,
        rec=get_recommendation(top["label"], status),
        disclaimer=DISCLAIMER,
        threshold=int(config.CONFIDENCE_THRESHOLD * 100),
        tip=random.choice(ECO_TIPS),
        pid=pid,
        labels=valid_labels(),
    )


@app.route("/feedback", methods=["POST"])
def feedback():
    pid = request.form.get("pid", type=int)
    if pid is None or pid != session.get("last_pred"):
        return jsonify(ok=False), 403
    correct = request.form.get("correct") == "1"
    label = None
    if not correct:
        label = request.form.get("label")
        if label not in valid_labels():
            return jsonify(ok=False), 400
    db.set_feedback(pid, correct, label)
    return jsonify(ok=True)


# ---------- Admin ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = db.get_user(request.form.get("username", "").strip())
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session.clear()
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
@admin_required
def dashboard():
    return render_template("dashboard.html", stats=db.get_stats())


@app.route("/history")
@admin_required
def history():
    page = max(request.args.get("page", 1, type=int), 1)
    label = request.args.get("label") or None
    status = request.args.get("status") or None
    per_page = 20
    rows, total = db.get_history(page, per_page, label, status)
    pages = max((total + per_page - 1) // per_page, 1)
    return render_template("history.html", rows=rows, page=page, pages=pages, total=total,
                           label=label, status=status, labels=db.get_labels())


@app.route("/history/delete/<int:pid>", methods=["POST"])
@admin_required
def delete_item(pid):
    filename = db.delete_prediction(pid)
    if filename:
        file_path = os.path.join(config.UPLOAD_FOLDER, os.path.basename(filename))
        if os.path.exists(file_path):
            os.remove(file_path)
        flash(f"Prediction #{pid} deleted.")
    return redirect(request.referrer or url_for("history"))


@app.route("/export.csv")
@admin_required
def export_csv():
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id", "time", "image", "predicted", "confidence", "status",
                "user_feedback", "corrected_label"])
    for r in db.get_all():
        fb = "" if r["feedback_correct"] is None else ("correct" if r["feedback_correct"] else "wrong")
        w.writerow([r["id"], r["local_time"], r["image_path"], r["predicted_class"],
                    round(r["confidence"], 4), r["status"], fb, r["corrected_label"] or ""])
    return Response(buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=predictions.csv"})


@app.errorhandler(413)
def too_large(_):
    flash("File too large. Maximum size is 5 MB.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)