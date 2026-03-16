# export_excel.py
import sqlite3
import pandas as pd
import os

def run_export():
    """
    Exports the 'participants' table from SQLite database to Excel.
    Creates an 'exports' folder if it doesn't exist.
    Returns the path to the generated Excel file.
    """

    # Ensure exports folder exists
    export_folder = "exports"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # Database file path
    db_path = "participants.db"

    # Check if database exists
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")

    # Connect to the database
    conn = sqlite3.connect(db_path)

    try:
        # Query all participants
        df = pd.read_sql_query("SELECT * FROM participants", conn)

        # Excel file path
        excel_path = os.path.join(export_folder, "prerelease_participants.xlsx")

        # Export to Excel
        df.to_excel(excel_path, index=False)

    finally:
        # Close database connection
        conn.close()

    # Return the path to the generated file
    return excel_path