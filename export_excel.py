# export_excel.py
# This module handles exporting participant data from the SQLite database
# into an Excel (.xlsx) file for download or reporting purposes.

import sqlite3   # Built-in Python library to interact with SQLite databases
import pandas as pd  # Used to query the database into a DataFrame and write to Excel
import os        # Used for file system operations (checking paths, creating folders)


def run_export():
    """
    Exports the 'participants' table from SQLite database to Excel.
    Creates an 'exports' folder if it doesn't exist.
    Returns the path to the generated Excel file.
    """

    # --- Output folder setup ---
    # Define the folder where the Excel file will be saved.
    # If the folder doesn't exist yet, create it automatically.
    export_folder = "exports"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # --- Database path ---
    # Path to the SQLite database file that stores participant records.
    db_path = "participants.db"

    # --- Database existence check ---
    # Before attempting a connection, verify the database file actually exists.
    # Raises a clear error instead of a cryptic SQLite exception if it's missing.
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")

    # --- Database connection ---
    # Open a connection to the SQLite database file.
    conn = sqlite3.connect(db_path)

    try:
        # --- Query all participants ---
        # Use pandas to run a SELECT query and load all rows from the
        # 'participants' table directly into a DataFrame for easy manipulation.
        df = pd.read_sql_query("SELECT * FROM participants", conn)

        # --- Define Excel output path ---
        # Build the full file path where the Excel file will be saved,
        # combining the export folder and the target filename.
        excel_path = os.path.join(export_folder, "prerelease_participants.xlsx")

        # --- Write to Excel ---
        # Export the DataFrame to an .xlsx file.
        # index=False prevents pandas from writing the row numbers as a column.
        df.to_excel(excel_path, index=False)

    finally:
        # --- Close database connection ---
        # Always close the connection whether the export succeeded or failed,
        # to avoid leaving open file handles on the database.
        conn.close()

    # --- Return file path ---
    # Return the path to the generated Excel file so the caller (app.py)
    # can send it as a downloadable HTTP response.
    return excel_path
    