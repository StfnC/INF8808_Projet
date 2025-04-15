from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from visualisation_1 import setup_viz_1
from visualisation_2 import setup_viz_2
from visualisation_3 import setup_viz_3
from visualisation_5 import setup_viz_5
from visualisation_6 import setup_viz_6 
from visualisation_7 import setup_vis_7
app = Dash(__name__)

df_bar = pd.DataFrame(
    {
        "Letters": ["A", "B", "C", "A", "B", "C"],
        "Count": [6, 2, 1, 1, 6, 3],
        "Language": ["EN", "EN", "EN", "FR", "FR", "FR"],
    }
)

fig = px.bar(df_bar, x="Letters", y="Count", color="Language", barmode="group")

app.layout = html.Div(
    children=[
        html.Div(setup_viz_1(app)),
        html.Div(setup_viz_2(app)),
        html.Div(setup_viz_3(app)),
        html.Div(setup_viz_5(app)),
        html.Div(setup_viz_6(app)),
        html.Div(setup_vis_7(app)),
    ]
)
