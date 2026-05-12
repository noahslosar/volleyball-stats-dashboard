import subprocess
import sqlite3
import os
import shutil

# Clone the repository
repo_url = "https://github.com/noahslosar/315_Proj1"
repo_path = "cloned_repo"

# Check if the directory already exists
if os.path.exists(repo_path):
    print(f"Repository already cloned at {repo_path}")
else:
    subprocess.run(["git", "clone", repo_url, repo_path], check=True)

# Path to the database file
db_file_path = os.path.join(repo_path, "volleyball_stats.db")

# Connect to it
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Get all table names in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Available tables:", tables)

# Query the first table (or replace with the actual table name)
if tables:
    table_name = tables[0][0]  # Get the first table name
    cursor.execute(f"SELECT * FROM {table_name}")
    results = cursor.fetchall()
    print(f"\nData from '{table_name}':")
    print(results)
else:
    print("No tables found in database")

conn.close()