# Volleyball Statistics Dashboard - Project Summary

## Overview
I've created a comprehensive interactive Streamlit dashboard (`app.py`) that visualizes your volleyball player statistics from the `volleyball_stats.db` database with **7+ interactive visualizations** including a map.

## Visualizations Included

### 1. **Top 10 Players by Points** (Bar Chart)
- Shows the highest-scoring players
- Color-coded by position
- Uses an attractive Set2 color palette

### 2. **Attack Efficiency vs Points Scored** (Scatter Plot)
- Correlates attack efficiency with total points
- Bubble size represents games played
- Interactive hover information showing player details
- Helps identify efficient scorers

### 3. **Position Performance Heatmap** (Heatmap)
- Displays average statistics by position
- Shows Points, Kills, Ace %, Digs, and Pass %
- Uses Viridis color scale for easy interpretation
- Great for comparing position performance at a glance

### 4. **Top Serve Performers** (Bar Chart)
- Highlights top 8 players by Ace percentage
- Color-coded by position
- Shows serve success metrics

### 5. **Team Composition by Position** (Pie Chart)
- Shows player distribution across positions
- Displays both percentages and labels
- Uses Set3 pastel color palette

### 6. **Team Locations Map** (Interactive Folium Map) ⭐
- Shows volleyball team venues across the USA
- Interactive markers for major tournament locations
- Includes: Lincoln NE, Austin TX, Palo Alto CA, Boulder CO, Stanford CA
- Color-coded markers for visual appeal
- Fully interactive - you can pan and zoom

### 7. **Defensive Stats - Top Player Radar Chart** (Radar Chart)
- Shows defensive capabilities for the top defensive player
- Metrics: Digs, Dig %, Pass Quality %, and Critical Rate %
- Visual representation of player strengths

### 8. **Full Statistics Table** (Interactive Data Table)
- Displays all player data with formatted numbers
- Searchable and sortable
- Shows all 31 columns from the database

## Features

✅ **Interactive Filters**: Use the sidebar to filter by position
✅ **Responsive Design**: Works on different screen sizes  
✅ **Color Aesthetics**: Multiple color palettes for visual appeal
  - Set2 (muted colors)
  - Plotly (vibrant)
  - Viridis (scientific)
  - Pastel (soft colors)
  - Custom colors for map markers

✅ **Data Quality**: All data is properly converted to numeric types
✅ **Hover Information**: Interactive charts show detailed info on hover
✅ **Professional Layout**: Clean, organized sections with headers

## How to Run

```bash
# Make sure you're in the project directory
cd C:\Users\Admin\PycharmProjects\StreamlitDatabase

# Run the Streamlit app
streamlit run app.py
```

The app will open at: `http://localhost:8501`

## Database Integration
- Automatically clones the GitHub repository if not present
- Connects to `volleyball_stats.db`
- Reads all data from the `player_stats` table
- Processes 27 player records with 31 statistics columns

## Data Included
- Player Jersey Numbers
- Player Names
- Playing Positions (Setter, Libero, Middle, Outside, Opposite)
- Attack Statistics (Attempts, Kills, Efficiency, etc.)
- Passing Statistics (Attempts, Pass Quality, etc.)
- Serving Statistics (Aces, Error %, Pass Stats, etc.)
- Blocking Statistics
- Defensive Statistics (Digs, Contact Rate, etc.)

## Technical Stack
- **Backend**: Python, SQLite3, Pandas
- **Visualization**: Plotly (interactive charts), Folium (maps)
- **Frontend**: Streamlit (web app framework)
- **Color Libraries**: Plotly qualitative color schemes

## Notes
- All numeric data is automatically formatted to 2 decimal places
- The sidebar filter allows you to focus on specific player positions
- The radar chart dynamically shows the top defensive player
- The map includes major volleyball tournament venues as examples

Enjoy exploring your volleyball statistics! 🏐

