from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import geojson

from utils import categories

DATA_PATH = "./data"
GEO_PATH = "./data/geojson"


def load_data():
    medals_df = pd.read_csv(f"{DATA_PATH}/medals.csv")
    with open(f"{GEO_PATH}/countries.geo.json", encoding="utf8") as file:
        countries = geojson.load(file)
    return medals_df, countries


def sport_to_cat(sport: str) -> str:
    for cat, sports in categories.items():
        if sport in sports:
            return cat
    return "Catégorie inconnue"


def sport_to_color(sport: str) -> str:
    for cat, sports in categories.items():
        if sport in sports:
            return cat
    return "Catégorie inconnue"


def compute_medals_per_cat_per_country(
    df: pd.DataFrame, country_code: str, category: str
) -> pd.DataFrame:
    count = 0
    intermed_df = df.groupby(["discipline", "country_code"], as_index=False).count()
    country_df = intermed_df[intermed_df["country_code"] == country_code]
    for _, row in country_df.iterrows():
        if sport_to_cat(row["discipline"].lower()) == category:
            count += row["medal_type"]
    return count


def setup_viz_3(app):
    medals_df, countries = load_data()
    max_medals_per_category = {}
    for category in categories:
        max_medals_per_category[category] = 0
    for id, row in medals_df.iterrows():
        category = sport_to_cat(row["discipline"].lower())
        if category in max_medals_per_category:
            max_medals_per_category[category] += 1

    countries_to_category = {}

    for name, group in medals_df.groupby("country_code"):
        best_sport = group.groupby("discipline")["name"].count().idxmax()
        category = sport_to_cat(best_sport.lower())
        countries_to_category[name] = category

    df_results = pd.DataFrame(
        columns=["country_code", "best_category", *categories.keys()]
    )
    for country in countries["features"]:
        name = country["properties"]["iso_a3"]
        best_category = countries_to_category.get(name, np.nan)
        cat_results = []
        for category in categories:
            cat_max = max_medals_per_category[category]
            cat_results.append(
                (
                    compute_medals_per_cat_per_country(medals_df, name, category)
                    / cat_max
                )
                * 100
            )
        df_results.loc[len(df_results)] = [name, best_category, *cat_results]

    @app.callback(Output("choropleth", "figure"), Input("category-dropdown", "value"))
    def display_choropleth(category: str):
        if category == "global":
            fig = px.choropleth_map(
                df_results,
                geojson=countries,
                color="best_category",
                locations="country_code",
                featureidkey="properties.iso_a3",
            )
            return fig
        else:
            return px.choropleth_map(
                df_results,
                geojson=countries,
                color=category,
                locations="country_code",
                featureidkey="properties.iso_a3",
                color_continuous_scale="Reds",
            )

    return html.Div(
        [
            html.H1("Médailles olmpiques par pays et par catégorie"),
            html.P("Sélectionnez une catégorie"),
            dcc.Dropdown(
                id="category-dropdown",
                options=[{"label": cat, "value": cat} for cat in categories.keys()]
                + [{"label": "Global", "value": "global"}],
                value="global",
                style={
                'color': 'black',            
                'backgroundColor': 'white'    
            }
            ),
            dcc.Graph(id="choropleth"),
        ]
    )
