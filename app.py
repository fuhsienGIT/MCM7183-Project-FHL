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

df = pd.read_csv("https://raw.githubusercontent.com/wenjiun/MCM7183Exercise3/main/assets/gdp_1960_2020.csv")
subset_2020 = df[df['year'].isin([2020])]

image_path = 'https://raw.githubusercontent.com/wenjiun/MCM7183Exercise3/main/assets/logo-mmu.png'

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("World GDP", className="display-4"),
        html.Hr(),
        html.P(
            "For MCM7183 Data Analytic Visualization", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Yearly GDP", href="/page-1", active="exact"),
                dbc.NavLink("GDP by Continent", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Home Page',
                        style={'textAlign':'center'}),
                dbc.Row([
dbc.Col(html.H1('MCM7183 Exercise 3', className="p-2 bg-light border text-center"),  width=10), 
dbc.Col(html.Img(src=image_path, className="m-2"))])
                ]
    elif pathname == "/page-1":
        return [
                html.H1('Yearly GDP',
                        style={'textAlign':'center'}),
dbc.Row(dbc.Col(dcc.Dropdown(subset_2020['country'], ['Malaysia'], id='dropdown-country', multi=True, className="mt-5"), width={"size": 4, "offset": 4})), 
dbc.Row(dcc.Graph(id="graph-scatter"))
                ]
    elif pathname == "/page-2":
        return [
                html.H1('GDP by Continent',
                        style={'textAlign':'center'}),
dbc.Row(dbc.Col(dcc.Slider(1960, 2020, 5, value=2020, id='slider-year',
                         marks = {i: str(i) for i in range(1960, 2021, 5)}, className="mt-5"), width={"size": 10, "offset": 1})), 
dbc.Row(dcc.Graph(id="graph-pie"))
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback(
    Output('graph-scatter', 'figure'),
    Input('dropdown-country', 'value')
)
def update_graph1(countries_selected):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for country_selected in countries_selected:
        subset_Country = df[df['country'].isin([country_selected])]
        trace = go.Scatter(x=subset_Country["year"], y=subset_Country["gdp"], name=country_selected)
        fig.add_trace(trace)
    return fig;

@app.callback(
    Output('graph-pie', 'figure'),
    Input('slider-year', 'value')
)
def update_graph2(year_selected):
    subset_Year = df[df['year'].isin([year_selected])]
    subset_Year_Asia = subset_Year[subset_Year['state'].isin(["Asia"])]
    subset_Year_Africa = subset_Year[subset_Year['state'].isin(["Africa"])]
    subset_Year_America = subset_Year[subset_Year['state'].isin(["America"])]
    subset_Year_Europe = subset_Year[subset_Year['state'].isin(["Europe"])]
    subset_Year_Oceania = subset_Year[subset_Year['state'].isin(["Oceania"])]
    pie_data = [sum(subset_Year_Asia['gdp']),sum(subset_Year_Africa['gdp']),sum(subset_Year_America['gdp']),sum(subset_Year_Europe['gdp']),sum(subset_Year_Oceania['gdp'])];
    mylabels = ["Asia", "Africa", "America", "Europe","Oceania"]
    pie_df = {'Continent': mylabels,'GDP': pie_data}
    fig2 = px.pie(pie_df,values="GDP",names="Continent")
    fig2.update_traces(sort=False) 
    return fig2;

if __name__ == '__main__':
    app.run(debug=True)
