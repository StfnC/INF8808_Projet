# Age Distribution by Gender Within Sports box plot
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import ast


DATA_PATH = './data'


def load_data():
    medals_df = pd.read_csv(f'{DATA_PATH}/medals.csv')
    medals_total_df = pd.read_csv(f'{DATA_PATH}/medals_total.csv')
    athletes_df = pd.read_csv(f'{DATA_PATH}/athletes.csv')
    return medals_df, medals_total_df, athletes_df

def clean_up(df: pd.DataFrame) -> pd.DataFrame:
    return df[["code", "gender", "height", "weight", "disciplines"]].dropna()

def remove_invalid_valued(df: pd.DataFrame, column: str) -> pd.DataFrame:
    return df[df[column].apply(lambda x: isinstance(x, (int, float)) and x > 0)]

def clean_up_disciplines(df: pd.DataFrame) -> pd.DataFrame:
    df['disciplines'] = df['disciplines'].apply(normalize_disciplines)
    df = df.explode('disciplines')
    df['disciplines'] = df['disciplines'].str.strip()
    return df

def normalize_disciplines(val):
    if isinstance(val, list):
        return val
    try:
        return ast.literal_eval(val)
    except:
        return [str(val)]

def create_box_plot(df: pd.DataFrame, column: str, title: str):
    fig = px.box(
        df,
        x="disciplines",
        y=column,
        color="gender",
        title=title,
        labels={
            "disciplines": "Disciplines",
            column: "Taille (cm)",
            "gender": "Genre"
        },
        color_discrete_map={
            "Male": "blue",
            "Female": "red"
        }
    )
    fig.update_layout(
        xaxis_tickangle=45,
        boxmode="group",
        height=600,
        width=1000,
        template="plotly_white"
    )
    return fig

    
def preprocess():
    medals_df, medals_total_df, athletes_df = load_data()
    athletes_df = clean_up(athletes_df)
    athletes_df = clean_up_disciplines(athletes_df)
    height_athletes_df = remove_invalid_valued(athletes_df, 'height')
    img = create_box_plot(height_athletes_df, "height", "Relation entre la taille et le sexe dans les disciplines sportives")
    img.show()
    return medals_df, medals_total_df, athletes_df

if __name__ == "__main__":
    preprocess()

def setup_vis_7(app):
    medals_df, medals_total_df, athletes_df = load_data()
    athletes_df = clean_up(athletes_df)
    athletes_df = clean_up_disciplines(athletes_df)
    height_athletes_df = remove_invalid_valued(athletes_df, 'height')

    available_disciplines = sorted(height_athletes_df['disciplines'].unique())

    def create_figure(df, selected_discipline=None):
        if selected_discipline and selected_discipline != 'all':
            df = df[df['disciplines'] == selected_discipline]

        fig = px.box(
            df,
            x="disciplines",
            y="height",
            color="gender",
            title="Relation entre la taille et le sexe dans les disciplines sportives",
            labels={
                "disciplines": "Disciplines",
                "height": "Taille (cm)",
                "gender": "Genre"
            },
            color_discrete_map={
                "Male": "blue",
                "Female": "red"
            }
        )
        fig.update_layout(
            xaxis_tickangle=45,
            boxmode="group",
            height=600,
            template="plotly_white"
        )
        return fig

    @app.callback(
        Output("graph7", "figure"),
        Input("discipline-dropdown", "value")
    )
    def update_graph(selected_discipline):
        return create_figure(height_athletes_df, selected_discipline)

    return html.Div([
        html.H1("Taille des athlètes par genre et discipline"),
        html.P("Choisir une discipline spécifique pour filtrer :"),
        dcc.Dropdown(
            id="discipline-dropdown",
            options=[{"label": "Toutes", "value": "all"}] +
                    [{"label": discipline, "value": discipline} for discipline in available_disciplines],
            value="all",
            style={
                'color': 'black',            
                'backgroundColor': 'white'    
            }
        ),
        dcc.Graph(id="graph7")
    ])
