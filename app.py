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

# Sample DataFrame for sales and profit
data = {
    'Category': ['Electronics', 'Furniture', 'Clothing', 'Food'],
    'Sales': [1000, 1500, 700, 1200],
    'Profit': [200, 300, 150, 250]
}

df = pd.DataFrame(data)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Simple Sales Dashboard"),
    
    # Dropdown for selecting a category
    html.Label("Select Category:"),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': cat, 'value': cat} for cat in df['Category']],
        value='Electronics',  # Default value
        clearable=False
    ),
    
    # Bar chart for sales
    dcc.Graph(id='sales-bar-chart'),

    # Pie chart for sales and profit comparison
    dcc.Graph(id='profit-pie-chart')
])

# Callback to update the bar chart based on dropdown selection
@app.callback(
    Output('sales-bar-chart', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_bar_chart(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    fig = px.bar(
        filtered_df,
        x='Category',
        y='Sales',
        title=f'Sales for {selected_category}'
    )
    return fig

# Callback to update the pie chart for sales vs profit
@app.callback(
    Output('profit-pie-chart', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_pie_chart(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    fig = px.pie(
        filtered_df,
        names=['Sales', 'Profit'],
        values=[filtered_df['Sales'].values[0], filtered_df['Profit'].values[0]],
        title=f'Sales vs Profit for {selected_category}'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
