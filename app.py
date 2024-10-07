from dash import Dash, html, dcc, callback, Input, Output
import numpy as np 
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import streamlit as st
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots


app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "MCM7183 Exercise 3"
server = app.server

# Sample movie rating data
data = {
    'Movie': ['Movie A', 'Movie B', 'Movie C', 'Movie D', 'Movie E'],
    'Rating': [8.5, 7.8, 9.0, 6.5, 8.2],
    'Votes': [1200, 1500, 950, 1100, 1300],
    'BoxOffice': [80, 150, 200, 50, 100]
}

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/fuhsienGIT/MCM7183-Project-FHL/refs/heads/main/assets/MALratings.csv")
# Data Cleaning Steps

# Inspect the dataset to identify columns
print(df.head())  # Check what the dataset looks like

# Remove unnecessary columns (based on inspection, you can adjust this)
columns_to_keep = ['Title', 'Score', 'Popularity', 'Genres']  # Keeping only necessary columns
df = df[columns_to_keep]

# Rename columns for readability
df.columns = ['Title', 'Score', 'Popularity', 'Genres']

# Handle missing values (if any) by dropping rows with missing data
df.dropna(inplace=True)

# Categorize movies into score tiers based on the new ranges
def categorize_movie(score):
    if 8.0 <= score <= 10:
        return 'Top Tier'
    elif 6.0 <= score < 8.0:
        return 'Middle Tier'
    else:
        return 'Low Tier'

df['Score Tier'] = df['Score'].apply(categorize_movie)

# Drop duplicates within each tier based on Score, keeping only one movie per score
df_top_tier = df[df['Score Tier'] == 'Top Tier'].drop_duplicates(subset='Score').head(10)
df_middle_tier = df[df['Score Tier'] == 'Middle Tier'].drop_duplicates(subset='Score').head(10)
df_low_tier = df[df['Score Tier'] == 'Low Tier'].drop_duplicates(subset='Score').head(10)

# Combine the top 10 movies from each tier
df_limited = pd.concat([df_top_tier, df_middle_tier, df_low_tier])

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard with tabs
app.layout = html.Div(
    style={'backgroundColor': '#f9f9f9', 'color': '#000', 'padding': '10px'},
    children=[
        # Title
        html.H1("Anime Ratings Dashboard", style={'textAlign': 'center'}),

        # Tabs for different views
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='Score Distribution by Tier', value='tab-1'),
            dcc.Tab(label='Genres Distribution (Pie)', value='tab-2'),
            dcc.Tab(label='Genres vs Score (Scatter)', value='tab-3'),
        ]),

        # Content area for graphs
        html.Div(id='tabs-content')
    ]
)

# Define callback to update graphs based on the selected tab
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs-example', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        # Bar chart showing anime scores grouped by score tier (limited to 10 per tier, distinct scores)
        fig = px.bar(df_limited, x='Title', y='Score', color='Score Tier', barmode='group',
                     title='Anime Score Distribution by Tier (Top 10 with Distinct Scores per Tier)',
                     labels={'Score': 'Score Value', 'Score Tier': 'Score Category'},
                     template='plotly_white')

        # Ensure the categories are ordered correctly and are not shifting positions
        fig.update_layout(xaxis={'categoryorder': 'total ascending'})
        return dcc.Graph(figure=fig)

    elif tab == 'tab-2':
        # Pie chart showing the distribution of Genres
        fig = px.pie(df_limited, names='Genres', title='Distribution of Genres in Top Movies',
                     labels={'Genres': 'Genres'}, template='plotly_white')
        return dcc.Graph(figure=fig)

    elif tab == 'tab-3':
        # Scatter plot showing genres vs score
        fig = px.scatter(df_limited, x='Genres', y='Score', size='Popularity', title='Genres vs Score Performance',
                         labels={'Genres': 'Genres', 'Score': 'Anime Score'}, template='plotly_white')
        return dcc.Graph(figure=fig)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
