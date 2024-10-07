from dash import Dash, html, dcc, callback, Input, Output
import numpy as np 
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
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

df = pd.DataFrame(data)

df_anime = pd.read_csv("https://raw.githubusercontent.com/fuhsienGIT/MCM7183-Project-FHL/refs/heads/main/assets/MALratings.csv")

# Categorize movies into rating tiers
def categorize_Score(score):
    if score >= 8.0:
        return 'Top Tier'
    elif score >= 6.5:
        return 'Middle Tier'
    else:
        return 'Low Tier'

df['Score Tier'] = df['Score'].apply(categorize_Score)

# Define the layout of the dashboard with tabs
app.layout = html.Div(
    style={'backgroundColor': '#f9f9f9', 'color': '#000', 'padding': '10px'},
    children=[
        # Title
        html.H1("Movie Ratings Dashboard", style={'textAlign': 'center'}),

        # Tabs for different views
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='Rating Distribution by Tier', value='tab-1'),
            dcc.Tab(label='Votes Distribution (Pie)', value='tab-2'),
            dcc.Tab(label='Box Office Performance (Scatter)', value='tab-3'),
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
        # Bar chart showing movie ratings grouped by rating tier
        fig = px.bar(df_anime, x='Title', y='Score', color='Rating Tier', barmode='group',
                     title='Movie Rating Distribution by Tier',
                     labels={'Score': 'Score Value', 'Score Tier': 'Rating Category'},
                     template='plotly_white')

        return dcc.Graph(figure=fig)

    elif tab == 'tab-2':
        # Pie chart showing the distribution of votes
        fig = px.pie(df, names='Movie', values='Votes', title='Votes Distribution',
                     labels={'Votes': 'Number of Votes'}, template='plotly_white')
        return dcc.Graph(figure=fig)

    elif tab == 'tab-3':
        # Scatter plot showing box office performance
        fig = px.scatter(df, x='Movie', y='BoxOffice', size='BoxOffice', title='Box Office Performance',
                         labels={'BoxOffice': 'Box Office (in million $)'}, template='plotly_white')
        return dcc.Graph(figure=fig)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
