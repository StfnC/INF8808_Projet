from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from visualisation_1 import setup_viz_1
from visualisation_2 import setup_viz_2
from visualisation_3 import setup_viz_3
from visualisation_5 import setup_viz_5
from visualisation_6 import setup_viz_6 
from visualisation_7 import setup_vis_7

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '20px'}, children=[
    html.Div(style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
    }, children=[
        html.H1("Analyse des Jeux Olympiques - 2024",
                style={
                    'textAlign': 'center',
                    'color': '#2c3e50',
                    'marginBottom': '30px',
                    'fontFamily': 'Arial, sans-serif'
                }),
      
        html.Div(style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'marginBottom': '30px',
            'borderRadius': '8px',
            'border': '1px solid #e1e5eb'
        }, children=[setup_viz_1(app)]),
     
        html.Div(style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'marginBottom': '30px',
            'borderRadius': '8px',
            'border': '1px solid #e1e5eb'
        }, children=[setup_viz_2(app)]),
      
        html.Div(style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'marginBottom': '30px',
            'borderRadius': '8px',
            'border': '1px solid #e1e5eb'
        }, children=[setup_viz_3(app)]),
        
        html.Div(style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'marginBottom': '30px',
            'borderRadius': '8px',
            'border': '1px solid #e1e5eb'
        }, children=[setup_viz_5(app)]),
        
        html.Div(style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'marginBottom': '30px',
            'borderRadius': '8px',
            'border': '1px solid #e1e5eb'
        }, children=[setup_viz_6(app)]),
        
        html.Div(style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'marginBottom': '30px',
            'borderRadius': '8px',
            'border': '1px solid #e1e5eb'
        }, children=[setup_vis_7(app)]),
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
    