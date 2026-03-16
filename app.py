from flask import Flask, render_template, request, send_file
from database import init_db, add_participant
import qrcode
import io

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    trainer_id = request.form.get("trainer_id", "").strip()
    contact = request.form.get("contact", "").strip()

    # Mandatory field validation
    if not name or not trainer_id:
        return render_template(
            "form.html",
            error="Please fill in the mandatory fields!"
        )

    lucky_number = add_participant(name, trainer_id, contact)

    return render_template("thankyou.html", lucky_number=lucky_number)


@app.route("/qr")
def qr_code():
    # Replace with your local IP for phone access
    local_ip = "http://192.168.1.100:5000"  # <-- Change this to your PC's LAN IP
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(local_ip)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)