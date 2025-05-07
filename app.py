# photon_heist_lab/app.py
import os, json, base64, hashlib, random, urllib.parse
from PIL import Image
import piexif
from flask import (
    Flask, render_template, request, redirect,
    send_file, make_response, jsonify, url_for
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

# ---------------- FLAGS (ocultas) ----------------
FLAGS = {
    "recon":      "FLAG{recon_ready}",
    "pixels":     "FLAG{pixels_reveal}",
    "hash":       "FLAG{hash_broken}",
    "escalated":  "FLAG{photon_escalated}",
    "unlocked":   "FLAG{photon_core_unlocked}",
    "complete":   "FLAG{photon_heist_complete}",
}

# ---------------- Herramientas ----------------
def xor_bytes(data: bytes, key_byte: int) -> bytes:
    return bytes(b ^ key_byte for b in data)

def ensure_dirs():
    os.makedirs("static/img",   exist_ok=True)
    os.makedirs("static/files", exist_ok=True)

def create_noise_image(path="static/img/cell.jpg"):
    img = Image.new("RGB", (300, 300))
    pixels = img.load()
    for x in range(300):
        for y in range(300):
            pixels[x, y] = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
    exif_dict = {"Exif": {}}
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = base64.b64encode(
        b"MD5:5ebe2294ecd0e0f08eab7690d2a6ee69"
    )
    img.save(path, exif=piexif.dump(exif_dict))

def create_blueprint_bin(path="static/files/core_blueprint.bin"):
    plaintext = (
        b"Photon Blueprint v1.0\n" +
        FLAGS["complete"].encode() + b"\n"
    )
    with open(path, "wb") as f:
        f.write(xor_bytes(plaintext, 0x42))

def bootstrap_assets():
    ensure_dirs()
    if not os.path.exists("static/img/cell.jpg"):
        create_noise_image()
    if not os.path.exists("static/files/core_blueprint.bin"):
        create_blueprint_bin()

# ---------------- Rutas ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/robots.txt")
def robots():
    return (
        "User-agent: *\n"
        "Disallow: /backup/\n"
        f"# {FLAGS['recon']}\n"
    ), 200, {"Content-Type": "text/plain"}

@app.route("/backup/")
def backup():
    return send_file("static/img/cell.jpg")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == "secret":
            cookie_dict = {"uid": 7, "role": "user", "sig": "resu"}
            raw_json    = json.dumps(cookie_dict, separators=(',', ':'))
            safe_cookie = urllib.parse.quote_plus(raw_json)   # <- codificación segura
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie("user_data", safe_cookie, samesite="Lax")
            return resp
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/check")
def api_check():
    raw = request.cookies.get("user_data")
    if not raw:
        return jsonify(error="no_cookie"), 401

    try:
        decoded = urllib.parse.unquote_plus(raw)
        data    = json.loads(decoded)
        sig     = request.args.get("sig", "")
        if sig == data["role"][::-1]:
            if data["role"] == "admin":
                return jsonify(flag=FLAGS["escalated"])
            return jsonify(status="user_ok")
    except Exception:
        pass
    return jsonify(error="invalid"), 401

@app.route("/unlock", methods=["GET", "POST"])
def unlock():
    if request.method == "POST":
        final_flag = request.form.get("final_flag", "").strip()
        if final_flag == FLAGS["complete"]:
            return redirect(url_for("final"))
        return "Flag incorrecta", 403

    key = request.args.get("key", "").lower()
    expected = "7c2572ab6333f87e699738dbf9ab8da6ccc88149"
    if key == expected:
        return render_template("unlock.html", flag=FLAGS["unlocked"])
    return "Invalid key", 403

@app.route("/final")
def final():
    return render_template("final.html")

# ---------------- main ----------------
if __name__ == "__main__":
    bootstrap_assets()
    app.run(host="0.0.0.0", port=8000, debug=False)
else:
    bootstrap_assets()
