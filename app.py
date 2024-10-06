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

        # Dropdown for Tab 1
        html.Div(
            id='tab-1-dropdown',
            children=[
                dcc.Dropdown(
                    id='movie-dropdown',
                    options=[{'label': movie, 'value': movie} for movie in df['Movie']],
                    placeholder="Select a movie",
                    value=None,  # Default value
                    style={'width': '50%', 'margin': 'auto'}
                )
            ],
            style={'display': 'none'}  # Hidden initially
        ),

        # Content area for graphs
        html.Div(id='tabs-content')
    ]
)

# Define callback to toggle visibility of dropdown in Tab 1 and update graphs based on selected tab
@app.callback(
    [Output('tabs-content', 'children'),
     Output('tab-1-dropdown', 'style')],
    [Input('tabs-example', 'value'),
     Input('movie-dropdown', 'value')]
)
def render_content(tab, selected_movie):
    if tab == 'tab-1':
        # Dropdown is visible only on Tab 1
        dropdown_style = {'display': 'block', 'textAlign': 'center'}

        # Filter data if a movie is selected in the dropdown
        filtered_df = df[df['Movie'] == selected_movie] if selected_movie else df

        # Bar chart showing movie ratings
        fig = px.bar(filtered_df, x='Movie', y='Rating', title='Movie Rating Distribution',
                     labels={'Rating': 'Rating Score'}, template='plotly_white')

        return dcc.Graph(figure=fig), dropdown_style

    elif tab == 'tab-2':
        # Hide dropdown for other tabs
        dropdown_style = {'display': 'none'}

        # Pie chart showing the distribution of votes
        fig = px.pie(df, names='Movie', values='Votes', title='Votes Distribution',
                     labels={'Votes': 'Number of Votes'}, template='plotly_white')
        return dcc.Graph(figure=fig), dropdown_style

    elif tab == 'tab-3':
        # Hide dropdown for other tabs
        dropdown_style = {'display': 'none'}

        # Scatter plot showing box office performance
        fig = px.scatter(df, x='Movie', y='BoxOffice', size='BoxOffice', title='Box Office Performance',
                         labels={'BoxOffice': 'Box Office (in million $)'}, template='plotly_white')
        return dcc.Graph(figure=fig), dropdown_style

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
