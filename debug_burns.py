import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('volleyball_stats.db')
df = pd.read_sql_query("SELECT * FROM player_stats", conn)
conn.close()

# Apply the same filtering as in the app
df = df[~((df['Last Name'] == '4') & (df['Position'] == 'None'))]
df = df[~((df['Last Name'] == 'Burns') & (df['GP'] == 1))]

# Check Burns players
burns_players = df[df['Last Name'] == 'Burns']
print("Burns players after filtering:")
print(burns_players[['Last Name', 'Position', 'GP', 'Points']].to_string())

print(f"\nTotal Burns players: {len(burns_players)}")

# Also check what the GP values are for Burns players
print("\nAll Burns entries in original data:")
conn = sqlite3.connect('volleyball_stats.db')
original_df = pd.read_sql_query("SELECT * FROM player_stats WHERE \"Last Name\" = 'Burns'", conn)
conn.close()
print(original_df[['Last Name', 'Position', 'GP', 'Points']].to_string())
