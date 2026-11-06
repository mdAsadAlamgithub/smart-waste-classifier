import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from PIL import Image

import config
from utils.classifier import predict, load
from utils.recommendations import get_recommendation, DISCLAIMER

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
load()   # load the model at startup so the first request isn't slow


def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS


def is_valid_image(path):
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False


@app.route("/")
def index():
    return render_template("index.html")


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
    name = f"{uuid.uuid4().hex}.{ext}"          # never trust the original filename
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

    return render_template(
        "result.html",
        image_name=name,
        results=results,
        top=top,
        status=status,
        rec=get_recommendation(top["label"], status),
        disclaimer=DISCLAIMER,
        threshold=int(config.CONFIDENCE_THRESHOLD * 100),
    )


@app.errorhandler(413)
def too_large(_):
    flash("File too large. Maximum size is 5 MB.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # use_reloader=False stops Flask from loading TensorFlow twice
    app.run(debug=True, use_reloader=False)