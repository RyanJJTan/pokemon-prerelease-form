# imports of what is needed.
from flask import Flask, render_template, request, send_file
from database import init_db, add_participant

# Initialization
app = Flask(__name__)
init_db()

# Home
@app.route("/")
def home():
    return render_template("form.html")

# After submitting the form
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

# import of export
from flask import send_file
from export_excel import run_export

# Admin using /export link
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

 # purge db data as admin
@app.route("/purge")
def purge():
    from flask import request
    import sqlite3

    key = request.args.get("key")

    if key != "dpMTG":
        return "Unauthorized", 403

    conn = sqlite3.connect("participants.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM participants")
    conn.commit()
    conn.close()

    return "Database purged successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)