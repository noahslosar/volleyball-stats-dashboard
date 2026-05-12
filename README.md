# 🏐 Volleyball Player Statistics Dashboard

An interactive Streamlit dashboard for exploring volleyball player statistics with multiple visualizations and filtering options.

## Features

- **📊 Interactive Visualizations**: 7+ charts including bar charts, scatter plots, heatmaps, and radar charts
- **🎛️ Dynamic Filtering**: Filter by position, minimum games played, and select individual players
- **📑 Tabbed Interface**: Organized into Overview, Attack Stats, Defense Stats, and Raw Data sections
- **📈 Real-time Updates**: All charts update instantly based on your filter selections
- **🎨 Multiple Chart Types**: Switch between bar charts, horizontal bars, and line charts

## Interactive Elements

- **Multiselect Dropdown**: Filter players by position (Setter, Libero, Middle, Outside, Opposite)
- **Slider**: Set minimum games played requirement
- **Selectbox**: Choose specific players for detailed radar chart analysis
- **Radio Buttons**: Switch between different chart visualization styles
- **Checkbox**: Toggle between raw stats and percentage-based views
- **Tabs**: Navigate between different dashboard sections

## Data Source

Statistics are sourced from a SQLite database containing comprehensive volleyball player performance metrics including:
- Attack statistics (kills, efficiency, attempts)
- Defense statistics (digs, passing, blocking)
- Serving statistics (aces, errors)
- Game participation data

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Open `http://localhost:8501` in your browser

## Deployment

This app is deployed on Streamlit Cloud and can be accessed at: [Your Streamlit Cloud URL]

## Technologies Used

- **Streamlit**: Web app framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **SQLite**: Database
- **Git**: Version control

## Dashboard Sections

### 📊 Overview
- Key performance metrics
- Top 10 players by points (customizable chart types)
- Team composition by position

### ⚡ Attack Stats
- Attack efficiency vs points scatter plot
- Position performance heatmap
- Top serve performers

### 🛡️ Defense Stats
- Individual player radar charts
- Top defensive players ranking
- Detailed player statistics tables

### 📊 Raw Data
- Complete player statistics table
- All data with filtering applied

## Contributing

Feel free to fork this repository and submit pull requests with improvements or additional features!

## License

This project is open source and available under the MIT License.
