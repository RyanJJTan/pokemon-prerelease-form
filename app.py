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

from flask import send_file
from export_excel import run_export

@app.route("/export")
def export():
    try:
        # Generate Excel
        excel_file = run_export()
        # Send file as attachment
        return send_file(excel_file, as_attachment=True)
    except Exception as e:
        # Show error message instead of generic 500
        return f"Error generating Excel: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)