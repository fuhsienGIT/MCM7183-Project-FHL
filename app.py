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

# Read data from a CSV file
# Example CSV structure:
# Category,Series1,Series2,Series3
# A,10,20,30
# B,15,25,35
# C,20,30,40
df = pd.read_csv('https://raw.githubusercontent.com/fuhsienGIT/MCM7183-Project-FHL/refs/heads/main/assets/best-selling-manga.csv')

app.layout = [html.H1('MCM7183 Exercise 3'), 
              dcc.Dropdown(['Shueisha', 'Kodansha'], 'Shueisha', id='dropdown-country'),
              dcc.Graph(id="graph-scatter"), 
              #dcc.Dropdown([{'label':'2020', 'value':2020}, {'label':'2010', 'value':2010}, 
              #              {'label':'2000', 'value':2000}], 2020, id='dropdown-year'),
              dcc.Slider('Shōjo', 'Seinen', 5, value=5, id='slider-year',
                         marks = {i: str(i) for i in range('Shōjo', 'Seinen', 5)}),
              dcc.Graph(id="graph-pie")]

#@callback(
#    Output('graph-scatter', 'figure'),
#    Output('graph-pie', 'figure'),
#    Input('dropdown-country', 'value'),
#    Input('slider-year', 'value')
#)

if __name__ == '__main__':
    app.run(debug=True)
