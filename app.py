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

# Remove the unwanted player (name "4" with position "None")
df = df[~((df['Last Name'] == '4') & (df['Position'] == 'None'))]

# Remove one of the Burns players (the one with fewer games played)
df = df[~((df['Last Name'] == 'Burns') & (df['GP'] == 1))]

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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Overview", "🏐 Attack Stats", "🎯 Serve Stats", "🛡️ Defense Stats", "📈 Position Analysis", "📊 Raw Data"])

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
    
    # 1. Games Played Bar Chart - All Players
    st.header("Games Played by All Players")
    gp_data = filtered_df.sort_values('GP', ascending=False)[['Player', 'Position', 'GP']]
    fig_gp = px.bar(gp_data, x='Player', y='GP', color='Position',
                    title="Games Played by All Players",
                    color_discrete_sequence=px.colors.qualitative.Set2)
    fig_gp.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_gp, width='stretch')
    
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
    st.header("Attack Statistics - Kills & Kill %")
    
    # 2. Kills (Ks) and Kill % (Ks%) Focus
    st.subheader("Kills vs Kill Percentage")
    fig_kills = px.scatter(filtered_df, x='Ks', y='Ks%', color='Position', 
                          size='GP', hover_name='Player',
                          title="Kills vs Kill Percentage (bubble size = Games Played)",
                          color_discrete_sequence=px.colors.qualitative.Plotly,
                          labels={'Ks': 'Total Kills', 'Ks%': 'Kill Percentage'})
    fig_kills.update_layout(height=400)
    st.plotly_chart(fig_kills, width='stretch')
    
    # Top Killers Chart
    st.subheader("Top Players by Kills")
    top_kills = filtered_df.nlargest(10, 'Ks')[['Player', 'Position', 'Ks', 'Ks%']]
    fig_top_kills = px.bar(top_kills, x='Player', y='Ks', color='Position',
                          title="Top 10 Players by Total Kills",
                          color_discrete_sequence=px.colors.qualitative.Set1)
    fig_top_kills.update_layout(height=400)
    st.plotly_chart(fig_top_kills, width='stretch')
    
    # Kill Efficiency by Position
    st.subheader("Average Kill Stats by Position")
    kill_stats = filtered_df.groupby('Position')[['Ks', 'Ks%', 'Att (Attack)']].mean().reset_index()
    fig_kill_pos = px.bar(kill_stats, x='Position', y='Ks', color='Position',
                         title="Average Kills by Position",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_kill_pos.update_layout(height=400)
    st.plotly_chart(fig_kill_pos, width='stretch')

with tab3:
    st.header("Serve Statistics - Aces, Errors & Attempts")
    
    # 4. Aces, Errors, and Total Serve Attempts
    st.subheader("Serve Performance Overview")
    
    # Create a combined chart for aces and errors
    serve_data = filtered_df[['Player', 'Position', 'Aces%', 'Err%', 'Att (Serve)']].copy()
    serve_data['Player_Pos'] = serve_data['Player'] + ' (' + serve_data['Position'] + ')'
    
    # Top servers by aces
    top_aces = filtered_df.nlargest(8, 'Aces%')[['Player', 'Position', 'Aces%', 'Err%', 'Att (Serve)']]
    fig_aces = px.bar(top_aces, x='Player', y=['Aces%', 'Err%'], 
                     title="Top 8 Players by Ace % (with Error %)",
                     color_discrete_sequence=['green', 'red'],
                     labels={'value': 'Percentage', 'variable': 'Stat Type'})
    fig_aces.update_layout(height=400)
    st.plotly_chart(fig_aces, width='stretch')
    
    # Serve attempts distribution
    st.subheader("Serve Attempts Distribution")
    fig_attempts = px.histogram(filtered_df, x='Att (Serve)', color='Position',
                               title="Distribution of Serve Attempts",
                               color_discrete_sequence=px.colors.qualitative.Set3)
    fig_attempts.update_layout(height=400)
    st.plotly_chart(fig_attempts, width='stretch')
    
    # Serve efficiency scatter
    st.subheader("Serve Efficiency: Aces vs Errors")
    fig_serve_eff = px.scatter(filtered_df, x='Aces%', y='Err%', color='Position',
                              size='Att (Serve)', hover_name='Player',
                              title="Ace % vs Error % (bubble size = Serve Attempts)",
                              color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_serve_eff.update_layout(height=400)
    st.plotly_chart(fig_serve_eff, width='stretch')

with tab4:
    st.header("Defense Statistics - Digs Focus")
    
    # 3. Digs Focus
    st.subheader("Digs Performance Analysis")
    
    # Top diggers
    top_digs = filtered_df.nlargest(10, 'Digs')[['Player', 'Position', 'Digs', 'Digs%', 'Good Pass%']]
    fig_top_digs = px.bar(top_digs, x='Player', y='Digs', color='Position',
                         title="Top 10 Players by Total Digs",
                         color_discrete_sequence=px.colors.qualitative.Set1)
    fig_top_digs.update_layout(height=400)
    st.plotly_chart(fig_top_digs, width='stretch')
    
    # Digs vs Dig %
    st.subheader("Digs vs Dig Percentage")
    fig_digs_scatter = px.scatter(filtered_df, x='Digs', y='Digs%', color='Position',
                                 size='GP', hover_name='Player',
                                 title="Total Digs vs Dig Percentage (bubble size = Games Played)",
                                 color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_digs_scatter.update_layout(height=400)
    st.plotly_chart(fig_digs_scatter, width='stretch')
    
    # Digs by position
    st.subheader("Average Digs by Position")
    digs_by_pos = filtered_df.groupby('Position')[['Digs', 'Digs%']].mean().reset_index()
    fig_digs_pos = px.bar(digs_by_pos, x='Position', y='Digs', color='Position',
                         title="Average Digs by Position",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_digs_pos.update_layout(height=400)
    st.plotly_chart(fig_digs_pos, width='stretch')

with tab5:
    st.header("Position Analysis - Passing & Points")
    
    # 5. Points scored grouped by positions
    st.subheader("Points Scored by Position")
    points_by_pos = filtered_df.groupby('Position')['Points'].sum().reset_index()
    fig_points_pos = px.bar(points_by_pos, x='Position', y='Points', color='Position',
                           title="Total Points Scored by Position",
                           color_discrete_sequence=px.colors.qualitative.Set2)
    fig_points_pos.update_layout(height=400)
    st.plotly_chart(fig_points_pos, width='stretch')
    
    # 2. Good Pass % and FBSO % Focus
    st.subheader("Passing Performance: Good Pass % vs FBSO %")
    fig_passing = px.scatter(filtered_df, x='Good Pass%', y='FBSO%', color='Position',
                            size='GP', hover_name='Player',
                            title="Good Pass % vs FBSO % (bubble size = Games Played)",
                            color_discrete_sequence=px.colors.qualitative.Plotly,
                            labels={'Good Pass%': 'Good Pass %', 'FBSO%': 'FBSO %'})
    fig_passing.update_layout(height=400)
    st.plotly_chart(fig_passing, width='stretch')
    
    # Top passers
    st.subheader("Top Players by Passing Performance")
    top_passers = filtered_df.nlargest(8, 'Good Pass%')[['Player', 'Position', 'Good Pass%', 'FBSO%']]
    fig_top_pass = px.bar(top_passers, x='Player', y='Good Pass%', color='Position',
                         title="Top 8 Players by Good Pass %",
                         color_discrete_sequence=px.colors.qualitative.Set3)
    fig_top_pass.update_layout(height=400)
    st.plotly_chart(fig_top_pass, width='stretch')
    
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
        # Only format numeric values, leave strings as-is
        numeric_cols = player_stats.index.difference(['Player', 'Position', 'Jersey'])
        st.dataframe(player_stats.style.format({col: "{:.2f}" for col in numeric_cols}))

with tab6:
    st.header("Raw Data")
    
    # Full Data Table
    st.subheader("Complete Player Statistics")
    st.dataframe(filtered_df.style.format(subset=numeric_columns, formatter='{:.2f}'), width='stretch')

# Footer
st.markdown("---")
st.markdown("*Data sourced from volleyball_stats.db | Interactive Dashboard with Streamlit and Plotly*")
st.markdown(f"**Current Filters:** {len(selected_positions)} positions selected, minimum {min_games} games played, {len(filtered_df)} players shown")
