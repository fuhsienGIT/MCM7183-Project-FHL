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

# Define genre mapping to the six categories
def categorize_genres(genres):
    genres = genres.lower()
    if 'action' in genres:
        return 'Action'
    elif 'adventure' in genres:
        return 'Adventure'
    elif 'comedy' in genres:
        return 'Comedy'
    elif 'sci-fi' in genres or 'science fiction' in genres:
        return 'Sci-Fi'
    elif 'slice of life' in genres:
        return 'Slice of Life'
    elif 'fantasy' in genres:
        return 'Fantasy'
    else:
        return 'Other'

# Apply the genre mapping to the Genres column
df['Main Genre'] = df['Genres'].apply(categorize_genres)

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

# Get the top 10 movies by popularity (lowest ranked values)
df_top_ranked = df.nsmallest(10, 'Popularity')

# Add Scores and Genres to the Titles for display
df_top_ranked['Title_and_Score'] = df_top_ranked['Title'] + ' (Score: ' + df_top_ranked['Score'].astype(str) + ')'

# Get the top 3 most popular anime titles for the summary
df_top_3 = df_top_ranked.head(3)
top_anime_titles = df_top_3['Title'].tolist()

# Create the formal summary text
summary_text = """
Based on the dataset analysis, the Action and Adventure genres stand out as the most favored, 
consistently appearing in the top-rated anime selections, reflecting their broad appeal among viewers. 
Additionally, Comedy and Slice of Life maintain significant popularity, particularly in the middle tiers, 
attracting a different segment of the audience. Sci-Fi and Fantasy genres also show strong performance, 
appealing to niche interests while still holding a solid place in the rankings.
"""

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
            dcc.Tab(label='Top 10 Movies by Popularity', value='tab-3'),
            dcc.Tab(label='Summary', value='tab-4'),  # New Summary Tab
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
        fig.update_layout(xaxis={'categoryorder': 'total ascending'},title_x=0.5)  # Align title to the center)

             # Add a text note about the tiers below the chart
        tier_text = html.P(
            "Top Tier: Score 8.0 - 10.0 | Middle Tier: Score 6.0 - 7.9 | Low Tier: Score Below 6.0", 
            style={'textAlign': 'center', 'fontWeight': 'bold'}
        )
        return dcc.Graph(figure=fig)

    elif tab == 'tab-2':
        # Pie chart showing the distribution of genres among the six categories
        fig = px.pie(df_limited, names='Main Genre', title='Distribution of Genres in Top Movies',
                     labels={'Main Genre': 'Genres'}, template='plotly_white')
        return dcc.Graph(figure=fig)

    elif tab == 'tab-3':
        # Horizontal bar chart showing the top 10 movies by Popularity (lowest rank values), including Scores and Genres
        fig = px.bar(df_top_ranked, x='Popularity', y='Title_and_Score', color='Main Genre', orientation='h',
                     title='Top 10 Movies by Popularity (Lowest Rank) with Scores and Genres',
                     labels={'Popularity': 'Popularity (Lower is Better)', 'Title_and_Score': 'Anime Title (Score)'},
                     template='plotly_white')

        # Customize layout to ensure readability
        fig.update_layout(xaxis={'categoryorder': 'total ascending'}, yaxis={'autorange': 'reversed'})
        return dcc.Graph(figure=fig)

    elif tab == 'tab-4':
        # Summary text displaying the top 3 most popular anime and genre analysis
        return html.Div(
            [
                html.H3("Anime Popularity Summary"),
                html.P(f"The most popular anime based on the dataset are: {', '.join(top_anime_titles[:3])}."),
                html.P(summary_text, style={'textAlign': 'center'}),
            ]
        )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
