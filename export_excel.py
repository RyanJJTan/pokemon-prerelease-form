import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("participants.db")

# Query the database
df = pd.read_sql_query("SELECT * FROM participants", conn)

# Export to excel and upload into the exports folder
df.to_excel("exports/prerelease_participants.xlsx", index=False)

# Close connection after exporting
conn.close()

print("Export complete.")