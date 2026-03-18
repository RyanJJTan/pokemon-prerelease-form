# database.py
# This module manages all direct interactions with the SQLite database.
# It handles database initialization and inserting new participant records.

import sqlite3  # Built-in Python library for working with SQLite databases
import random   # Used to generate a random lucky number for each participant

# --- Database file name ---
# Defines the SQLite database filename used across all functions in this module.
# Keeping it as a constant makes it easy to change in one place if needed.
DB_NAME = "participants.db"


def init_db():
    # Open a connection to the database file (creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)

    # Create a cursor object to execute SQL statements
    c = conn.cursor()

    # --- Create table if not exists ---
    # Defines the schema for the 'participants' table.
    # - id: auto-incrementing primary key, uniquely identifies each row
    # - name: participant's full name (text)
    # - trainer_id: the trainer's ID associated with the participant (text)
    # - contact: optional contact information (text)
    # - lucky_number: a randomly assigned number given to the participant upon registration
    c.execute("""
    CREATE TABLE IF NOT EXISTS participants(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        trainer_id TEXT,
        contact TEXT,
        lucky_number INTEGER
    )
    """)

    # --- Commit and close ---
    # Save the changes to the database file and close the connection.
    conn.commit()
    conn.close()


def add_participant(name, trainer_id, contact):
    # --- Generate lucky number ---
    # Randomly pick a number between 1 and 999 (inclusive) to assign to this participant.
    lucky_number = random.randint(1, 999)

    # --- Open database connection ---
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # --- Insert participant record ---
    # Uses parameterized query (?) to safely insert values and prevent SQL injection.
    # Inserts name, trainer_id, contact, and the generated lucky_number into the table.
    c.execute(
        "INSERT INTO participants (name, trainer_id, contact, lucky_number) VALUES (?, ?, ?, ?)",
        (name, trainer_id, contact, lucky_number)
    )

    # --- Commit and close ---
    # Persist the new record to disk and release the database connection.
    conn.commit()
    conn.close()

    # --- Return lucky number ---
    # Send the lucky number back to the caller (app.py) so it can be
    # displayed to the participant on the thank-you page.
    return lucky_number
