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

# Sample data for the graphs
df = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Value1": [10, 20, 30, 40],
    "Value2": [40, 30, 20, 10],
    "Value3": [25, 35, 15, 45]
})

# Define layout of the dashboard
app.layout = html.Div(
    style={'backgroundColor': '#2c2c2c', 'color': '#FFFFFF', 'textAlign': 'center'},
    children=[
        # Top navigation bar
        html.Div(
            style={'display': 'flex', 'justifyContent': 'center', 'padding': '10px', 'backgroundColor': '#333'},
            children=[
                html.Button('Graph 1', id='btn-1', style={'color': '#FFFFFF', 'backgroundColor': '#1f77b4'}),
                html.Button('Graph 2', id='btn-2', style={'color': '#FFFFFF', 'backgroundColor': '#ff7f0e'}),
                html.Button('Graph 3', id='btn-3', style={'color': '#FFFFFF', 'backgroundColor': '#2ca02c'}),
            ]
        ),
        
        # Content area for graphs
        html.Div(
            style={'display': 'flex', 'justifyContent': 'center', 'padding': '20px'},
            children=[
                # Graph 1 (Bar Chart)
                dcc.Graph(
                    id='bar-chart',
                    figure=px.bar(df, x='Category', y='Value1', title='Bar Chart 1', template='plotly_dark')
                ),
                
                # Graph 2 (Line Chart)
                dcc.Graph(
                    id='line-chart',
                    figure=px.line(df, x='Category', y='Value2', title='Line Chart 2', template='plotly_dark')
                ),

                # Graph 3 (Pie Chart)
                dcc.Graph(
                    id='pie-chart',
                    figure=px.pie(df, names='Category', values='Value3', title='Pie Chart 3', template='plotly_dark')
                ),
            ]
        )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
