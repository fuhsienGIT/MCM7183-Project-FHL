from dash import Dash, html, dcc, callback, Input, Output
import numpy as np 
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import streamlit as st
import matplotlib.pyplot as plt

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

#df = pd.DataFrame(data)

movie_data = pd.read_csv("https://raw.githubusercontent.com/fuhsienGIT/MCM7183-Project-FHL/refs/heads/main/assets/MALratings.csv")

# Function to display the average movie score
def display_average_score():
    average_score = movie_data['Score'].mean()
    st.write(f"Average Movie Score: {average_score}")

# Function to display the top-rated movies by score
def display_top_rated_movies():
    top_rated_movies = movie_data.nlargest(10, 'Score')
    st.write("Top 10 Rated Movies:")
    st.dataframe(top_rated_movies)

# Function to display a histogram of movie scores
def display_score_histogram():
    plt.figure(figsize=(10, 6))
    plt.hist(movie_data['Score'], bins=10, color='blue')
    plt.xlabel('Score')
    plt.ylabel('Count')
    plt.title('Movie Score Distribution')
    st.pyplot()

# Main Streamlit app
def main():
    st.title("Movie Rating Dashboard")

    # Tabs for different functions
    tabs = ["Average Score", "Top Rated Movies", "Score Histogram"]
    selected_tab = st.selectbox("Select a tab:", tabs)

    if selected_tab == "Average Score":
        display_average_score()
    elif selected_tab == "Top Rated Movies":
        display_top_rated_movies()
    elif selected_tab == "Score Histogram":
        display_score_histogram()

if __name__ == "__main__":
    main()
