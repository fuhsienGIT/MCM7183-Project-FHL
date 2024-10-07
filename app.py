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

pd.DataFrame(data)

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

        # Dropdown for Tab 1, allowing multi-selection for movie subsets
        html.Div(
            id='tab-1-dropdown',
            children=[
                dcc.Dropdown(
                    id='movie-dropdown',
                    options=[{'label': movie, 'value': movie} for movie in df['Movie']],
                    placeholder="Select one or more movies",
                    multi=True,  # Allow multiple selections
                    value=[],  # Start with no selection
                    style={'width': '50%', 'margin': 'auto'}
                )
            ]
        ),

        # Content area for graphs
        html.Div(id='tabs-content')
    ]
)

# Define callback to update graphs based on the selected tab and selected movies in Tab 1
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs-example', 'value'),
     Input('movie-dropdown', 'value')]
)
def render_content(tab, selected_movies):
    if tab == 'tab-1':
        # Filter data based on the selected movies
        if selected_movies:
            filtered_df = df[df['Movie'].isin(selected_movies)]
        else:
            filtered_df = df  # If no movie is selected, show all movies

        # Bar chart showing movie ratings for selected movies
        fig = px.bar(filtered_df, x='Movie', y='Rating', title='Movie Rating Distribution',
                     labels={'Rating': 'Rating Score'}, template='plotly_white')

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
