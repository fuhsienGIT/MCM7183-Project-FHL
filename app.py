from dash import Dash, html, dcc, callback, Input, Output
import numpy as np 
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.PULSE])
app.title = "MCM7183 Exercise 3"
server = app.server

# Read data from a CSV file
# Example CSV structure:
# Category,Series1,Series2,Series3
# A,10,20,30
# B,15,25,35
# C,20,30,40
df = pd.read_csv('https://raw.githubusercontent.com/fuhsienGIT/MCM7183-Project-FHL/refs/heads/main/assets/best-selling-manga.csv')

# Create traces for each series with different styles
trace1 = go.Bar(
    x=df['Manga series'], 
    y=df['Publisher'], 
    name='Manga',
    marker=dict(color='blue', pattern_shape="x")  # Style 1: Blue bars with 'x' pattern
)

trace2 = go.Bar(
    x=df['Manga series'], 
    y=df['No. of collected volumes'], 
    name='Manga',
    marker=dict(color='green', pattern_shape="dot")  # Style 2: Green bars with dots pattern
)

trace3 = go.Bar(
    x=df['Manga series'], 
    y=df['Demographic'], 
    name='Manga',
    marker=dict(color='orange', pattern_shape="|")  # Style 3: Orange bars with vertical line pattern
)
# Create the figure with all three traces (bars)
fig = go.Figure(data=[trace1, trace2, trace3])

# Customize the layout to group the bars
fig.update_layout(
    title='Bar Chart with 3 Different Visual Styles',
    xaxis_title='Category',
    yaxis_title='Values',
    barmode='group',  # Group the bars side by side
    template='simple_white'  # Use a simple white background for clean design
)

# Show the plot
fig.show()

