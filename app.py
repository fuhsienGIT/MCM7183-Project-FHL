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

df = pd.read_csv("https://raw.githubusercontent.com/fuhsienGIT/MCM7183-Project-FHL/refs/heads/main/assets/disney_plus_titles.csv")

# Define the layout of the dashboard with tabs
app.layout = html.Div(
    style={'backgroundColor': '#f9f9f9', 'color': '#000', 'padding': '10px'},
    children=[
        # Title
        html.H1("Movie Ratings Dashboard", style={'textAlign': 'center'}),

        # Tabs for different views
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='Rating Distribution', value='tab-1'),
            dcc.Tab(label='Votes Distribution (Pie)', value='tab-2'),
            dcc.Tab(label='Box Office Performance (Scatter)', value='tab-3'),
        ]),

        # Content area for graphs
        html.Div(id='tabs-content')
    ]
)

# Define callback to update graphs based on the selected tab and dropdown in Tab 1
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs-example', 'value'),
     Input('movie-dropdown', 'value')]
)
def render_content(tab, selected_movie):
    if tab == 'tab-1':
        # Filter data if a movie is selected in the dropdown
        filtered_df = df[df['title'] == selected_movie] if selected_movie else df

        # Bar chart showing movie ratings
        fig = px.bar(filtered_df, x='title', y='rating', title='Movie Rating Distribution',
                     labels={'rating': 'Rating Score'}, template='plotly_white')

        # Dropdown for filtering by movie
        dropdown = dcc.Dropdown(
            id='movie-dropdown',
            options=[{'label': movie, 'value': movie} for movie in df['title']],
            placeholder="Select a movie",
            value=None,  # Default value
            style={'width': '50%', 'margin': 'auto'}
        )

        return html.Div([dropdown, dcc.Graph(figure=fig)])

    elif tab == 'tab-2':
        # Pie chart showing the distribution of votes
        fig = px.pie(df, names='title', values='type', title='Votes Distribution',
                     labels={'type': 'Number of Votes'}, template='plotly_white')
        return dcc.Graph(figure=fig)

    elif tab == 'tab-3':
        # Scatter plot showing box office performance
        fig = px.scatter(df, x='title', y='duration', size='duration', title='Box Office Performance',
                         labels={'duration': 'Box Office (in million $)'}, template='plotly_white')
        return dcc.Graph(figure=fig)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
