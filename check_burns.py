import sqlite3

conn = sqlite3.connect('volleyball_stats.db')
cursor = conn.cursor()

# Get all Burns players
cursor.execute('SELECT * FROM player_stats WHERE "Last Name" LIKE "Burns"')
burns_players = cursor.fetchall()

print("Burns players found:")
for i, player in enumerate(burns_players):
    print(f"{i+1}. {player[1]} - {player[2]} - GP: {player[4]} - Points: {player[5]}")

conn.close()
