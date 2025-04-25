import pandas as pd
import plotly.express as px
from dash import dcc, html
from utils import DATA_PATH

def setup_viz_1(app):
    df = pd.read_csv(f'{DATA_PATH}/athletes.csv')

    df['Age'] = 2025 - pd.to_datetime(df['birth_date']).dt.year
    bins = list(range(df['Age'].min(), df['Age'].max() + 5, 5))
    labels = [f'{i}-{i+4}' for i in range(df['Age'].min(), df['Age'].max(), 5)]
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    df['Age Group'] = pd.Categorical(df['Age Group'], categories=labels, ordered=True)


    sport_to_category = {
        'Table Tennis': 'Sports de raquette',
        'Badminton': 'Sports de raquette',
        'Tennis': 'Sports de raquette',
        'Triathlon': '-athlon',
        'Modern Pentathlon': '-athlon',
        'Athletics': 'Athlétisme',
        'Canoe Sprint': 'Sport sur bateaux',
        'Rowing': 'Sport sur bateaux',
        'Surfing': 'Sport sur bateaux',
        'Sailing': 'Sport sur bateaux',
        'Canoe Slalom': 'Sport sur bateaux',
        'Swimming': 'Piscine',
        'Diving': 'Piscine',
        'Marathon Swimming': 'Piscine',
        'Artistic Swimming': 'Piscine',
        'Golf': 'Sports de précision',
        'Shooting': 'Sports de précision',
        'Archery': 'Sports de précision',
        'Water Polo': "Sports d'équipe",
        'Hockey': "Sports d'équipe",
        'Football': "Sports d'équipe",
        'Handball': "Sports d'équipe",
        'Basketball': "Sports d'équipe",
        'Rugby Sevens': "Sports d'équipe",
        'Beach Volleyball': "Sports d'équipe",
        '3x3 Basketball': "Sports d'équipe",
        'Volleyball': "Sports d'équipe",
        'Artistic Gymnastics': 'Gymnastique',
        'Rhythmic Gymnastics': 'Gymnastique',
        'Trampoline Gymnastics': 'Gymnastique',
        'Cycling BMX Freestyle': 'Cyclisme',
        'Cycling BMX Racing': 'Cyclisme',
        'Cycling Track': 'Cyclisme',
        'Cycling Mountain Bike': 'Cyclisme',
        'Cycling Road': 'Cyclisme',
        'Wrestling': 'Sports de combat',
        'Taekwondo': 'Sports de combat',
        'Boxing': 'Sports de combat',
        'Judo': 'Sports de combat',
        'Fencing': 'Sports de combat',
        'Sport Climbing': 'Autres sports',
        'Weightlifting': 'Autres sports',
        'Breaking': 'Autres sports',
        'Skateboarding': 'Autres sports',
        'Equestrian': 'Autres sports',
    }

    df['discipline'] = df['disciplines'].map(lambda x: x.translate({ord(i): None for i in "[']"}))
    df['Sport Category'] = df['discipline'].map(sport_to_category)

    fig = px.density_heatmap(
            df,
            x='Age Group',
            y='Sport Category',
            nbinsx=len(df['Age Group'].unique()),
            nbinsy=len(df['Sport Category'].unique()),
            histfunc='count',
            color_continuous_scale='Reds',
            title="Nombre d'athlètes par groupe d'âge et catégorie de sport",
            labels={
                'Sport Category': 'Catégorie de sports',
                'Age Group': "Groupe d'âge",
                'count': "Nombre d'athlètes"
            },
            height=600,
            category_orders={'Age Group': labels},
        )
        
    fig.update_layout(
        xaxis_title="Groupe d'âge",
        yaxis_title='Catégorie de sports',
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_colorbar_title="Nombre d'athlètes",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return html.Div([
        html.H3("Répartition par âge des athlètes par catégorie sportive"),
        dcc.Graph(figure=fig)
    ])

