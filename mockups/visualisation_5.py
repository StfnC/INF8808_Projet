# Bubble plot. Axe des x: âge, axe des y: discipline. Couleur: type de médaille, taille: nb de médailles
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
DATA_PATH = '../data'

def load_data():
    medals_df = pd.read_csv(f'{DATA_PATH}/medals.csv')
    athletes_df = pd.read_csv(f'{DATA_PATH}/athletes.csv')
    return medals_df, athletes_df

def calculate_age(df: pd.DataFrame) -> pd.DataFrame:
    df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
    df['age'] = 2024 - df['birth_date'].dt.year
    return df

def clean_disciplines_column(df):
    df['disciplines'] = df['disciplines'].apply(
        lambda x: eval(x)[0] if isinstance(x, str) and x.startswith('[') else x
    )
    return df

def join_tables(medals_df: pd.DataFrame, athletes_df: pd.DataFrame) -> pd.DataFrame:
    medals_df['code'] = medals_df['code'].astype(str)
    athletes_df['code'] = athletes_df['code'].astype(str)
    return pd.merge(medals_df, athletes_df, on='code')

def create_visualization(medaled_athletes: pd.DataFrame):
    discipline_counts = medaled_athletes['disciplines'].value_counts()
    significant_disciplines = discipline_counts[discipline_counts >= 3].index.tolist()
    filtered_df = medaled_athletes[medaled_athletes['disciplines'].isin(significant_disciplines)]
    
    grouped = (
        filtered_df
        .groupby(["age", "disciplines", "medal_type"])
        .size()
        .reset_index(name="count")
    )
    
    fig = px.scatter(
        grouped,
        x="age",
        y="disciplines",
        size="count",
        color="medal_type",
        color_discrete_map={
            "Gold Medal": "#FFD700",
            "Silver Medal": "#C0C0C0",
            "Bronze Medal": "#CD7F32"
        },
        size_max=15,  
        opacity=0.7,
        hover_name="disciplines",
        hover_data={
            "age": True,
            "count": True,
            "medal_type": True,
            "disciplines": False  
        },
        title="Âge vs Discipline des Athlètes Médaillés",
        labels={
            "age": "Âge",
            "disciplines": "Discipline",
            "medal_type": "Type de médaille",
            "count": "Nombre de médailles"
        },
    )
    
    fig.update_traces(marker=dict(sizemode='area', line=dict(width=0.5, color='white')))
    fig.update_layout(
        plot_bgcolor='rgba(240, 240, 240, 0.5)',  
        height=800, 
        legend_title_text="Type de médaille",
        xaxis=dict(
            title="Âge",
            gridcolor='white',
            range=[15, 60], 
        ),
        yaxis=dict(
            title="Discipline",
            gridcolor='white',
            categoryorder='total ascending',
        )
    )
    
    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(220, 220, 220, 0.8)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(220, 220, 220, 0.8)'
        )
    )
    
    return fig



def preprocess():
    medals_df, athletes_df = load_data()
    athletes_df = calculate_age(athletes_df)
    combined_df = join_tables(medals_df, athletes_df)
    combined_df = clean_disciplines_column(combined_df)
    fig = create_visualization(combined_df)
    fig.show()

if __name__ == "__main__":
    preprocess()