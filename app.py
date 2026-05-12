import streamlit as st
import sqlite3
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(page_title="Volleyball Stats Dashboard", layout="wide")

# Path to the database file (now included locally)
db_file_path = "volleyball_stats.db"

# Connect to the database
conn = sqlite3.connect(db_file_path)
df = pd.read_sql_query("SELECT * FROM player_stats", conn)
conn.close()

# Clean up the data - convert columns to numeric where applicable
numeric_columns = df.columns[3:]  # Skip #, Last Name, Position
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Rename columns for easier access
df = df.rename(columns={'#': 'Jersey', 'Last Name': 'Player', 'Position': 'Position'})

st.title("🏐 Volleyball Player Statistics Dashboard")
st.markdown("---")

# ============================================================================
# INTERACTIVE ELEMENTS - Sidebar Controls
# ============================================================================
st.sidebar.header("🎛️ Interactive Controls")

# 1. Position Filter (Multiselect)
selected_positions = st.sidebar.multiselect(
    "Select Positions:",
    df['Position'].unique(),
    default=df['Position'].unique(),
    key="position_filter"
)

# 2. Minimum Games Played Slider
min_games = st.sidebar.slider(
    "Minimum Games Played:",
    min_value=0,
    max_value=int(df['GP'].max()),
    value=0,
    step=1,
    key="games_slider"
)

# 3. Player Selection Dropdown
filtered_df = df[df['Position'].isin(selected_positions) & (df['GP'] >= min_games)]
selected_player = st.sidebar.selectbox(
    "Select Player for Detailed View:",
    ["All Players"] + sorted(filtered_df['Player'].unique().tolist()),
    key="player_select"
)

# 4. Chart Type Radio Buttons
chart_type = st.sidebar.radio(
    "Chart Style for Top Players:",
    ["Bar Chart", "Horizontal Bar", "Line Chart"],
    key="chart_type_radio"
)

# 5. Data View Toggle
show_percentages = st.sidebar.checkbox(
    "Show Percentage Stats Only",
    value=False,
    key="percentage_toggle"
)

# Apply filters
filtered_df = df[df['Position'].isin(selected_positions) & (df['GP'] >= min_games)]

# ============================================================================
# TABS - Main Navigation (6th Interactive Element)
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚡ Attack Stats", "🛡️ Defense Stats", "📊 Raw Data"])

with tab1:
    st.header("Overview Dashboard")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Players", len(filtered_df))
    with col2:
        st.metric("Total Points", f"{filtered_df['Points'].sum():.0f}")
    with col3:
        st.metric("Avg Efficiency", f"{filtered_df['Eff'].mean():.3f}")
    with col4:
        st.metric("Games Played", f"{filtered_df['GP'].sum():.0f}")
    
    # Top 10 Players Chart (Interactive based on chart type selection)
    st.header("Top 10 Players by Points")
    top_points = filtered_df.nlargest(10, 'Points')[['Player', 'Position', 'Points']]
    
    if chart_type == "Bar Chart":
        fig1 = px.bar(top_points, x='Player', y='Points', color='Position',
                      title="Top 10 Scorers - Bar Chart",
                      color_discrete_sequence=px.colors.qualitative.Set2)
    elif chart_type == "Horizontal Bar":
        fig1 = px.bar(top_points, y='Player', x='Points', color='Position', orientation='h',
                      title="Top 10 Scorers - Horizontal Bar",
                      color_discrete_sequence=px.colors.qualitative.Set2)
    else:  # Line Chart
        fig1 = px.line(top_points, x='Player', y='Points', color='Position',
                       title="Top 10 Scorers - Line Chart",
                       color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig1.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig1, width='stretch')
    
    # Position Distribution Pie Chart
    st.header("Team Composition by Position")
    position_counts = filtered_df['Position'].value_counts()
    fig_pie = px.pie(values=position_counts.values, names=position_counts.index,
                     title="Player Distribution by Position",
                     color_discrete_sequence=px.colors.qualitative.Set3)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, width='stretch')

with tab2:
    st.header("Attack Statistics")
    
    # Attack Efficiency Scatter Plot
    st.subheader("Attack Efficiency vs Points Scored")
    fig2 = px.scatter(filtered_df, x='Eff', y='Points', color='Position', 
                      size='GP', hover_name='Player',
                      title="Attack Efficiency vs Points (bubble size = Games Played)",
                      color_discrete_sequence=px.colors.qualitative.Plotly)
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, width='stretch')
    
    # Position Performance Heatmap
    st.subheader("Position Performance Heatmap")
    if show_percentages:
        position_stats = filtered_df.groupby('Position')[['Eff', 'Ks%', 'Es%', 'Bs%']].mean()
    else:
        position_stats = filtered_df.groupby('Position')[['Points', 'Ks', 'Att (Attack)']].mean()
    
    fig3 = go.Figure(data=go.Heatmap(
        z=position_stats.values,
        x=position_stats.columns,
        y=position_stats.index,
        colorscale='Viridis',
        colorbar=dict(title="Average Value")
    ))
    fig3.update_layout(title="Average Stats by Position", height=400)
    st.plotly_chart(fig3, width='stretch')
    
    # Top Servers Chart
    st.subheader("Top Serve Performers")
    top_servers = filtered_df.nlargest(8, 'Aces%')[['Player', 'Position', 'Aces%', 'Err%']]
    fig4 = px.bar(top_servers, x='Player', y='Aces%', color='Position',
                  title="Top 8 Players by Ace Percentage",
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, width='stretch')

with tab3:
    st.header("Defense Statistics")
    
    # Defensive Stats Radar Chart (for selected player)
    if selected_player != "All Players":
        st.subheader(f"Detailed Stats for {selected_player}")
        player_data = filtered_df[filtered_df['Player'] == selected_player].iloc[0]
        
        # Create radar chart for the selected player
        categories = ['Digs', 'Digs%', 'Good Pass%', 'CRT%', 'Aces%', 'Eff']
        values = [player_data['Digs']/10, player_data['Digs%'], player_data['Good Pass%'], 
                 player_data['CRT%'], player_data['Aces%'], player_data['Eff']]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=selected_player,
            line=dict(color='rgb(0, 128, 255)')
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title=f"Comprehensive Stats for {selected_player}",
            height=500
        )
        st.plotly_chart(fig_radar, width='stretch')
        
        # Player stats table
        st.subheader(f"Detailed Statistics for {selected_player}")
        player_stats = filtered_df[filtered_df['Player'] == selected_player].T
        player_stats.columns = ['Value']
        st.dataframe(player_stats.style.format("{:.2f}"))
    
    # Top Defensive Players
    st.subheader("Top Defensive Players")
    top_defenders = filtered_df.nlargest(5, 'Digs')[['Player', 'Position', 'Digs', 'Digs%', 'Good Pass%']]
    fig_defense = px.bar(top_defenders, x='Player', y='Digs', color='Position',
                        title="Top 5 Players by Total Digs",
                        color_discrete_sequence=px.colors.qualitative.Set1)
    fig_defense.update_layout(height=400)
    st.plotly_chart(fig_defense, width='stretch')

with tab4:
    st.header("Raw Data")
    
    # Full Data Table
    st.subheader("Complete Player Statistics")
    st.dataframe(filtered_df.style.format(subset=numeric_columns, formatter='{:.2f}'), width='stretch')

# Footer
st.markdown("---")
st.markdown("*Data sourced from volleyball_stats.db | Interactive Dashboard with Streamlit and Plotly*")
st.markdown(f"**Current Filters:** {len(selected_positions)} positions selected, minimum {min_games} games played, {len(filtered_df)} players shown")
