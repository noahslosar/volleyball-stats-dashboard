import sqlite3

db_path = "cloned_repo/volleyball_stats.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(player_stats)")
columns = cursor.fetchall()

print("Column names:")
for col in columns:
    print(f"  {col[1]}")

conn.close()

