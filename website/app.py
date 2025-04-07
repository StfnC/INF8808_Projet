from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

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
        html.Div(
            [
                html.H1(children="First Viz"),
                html.Div(
                    children="""
            Example for the first viz.
        """
                ),
                dcc.Graph(id="graph1", figure=fig),
            ]
        ),
        html.Div(
            [
                html.H1(children="Second Viz"),
                html.Div(
                    children="""
            Example for the second viz.
        """
                ),
                dcc.Graph(id="graph2", figure=fig),
            ]
        ),
    ]
)
