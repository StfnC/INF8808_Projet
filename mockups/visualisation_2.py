import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import ast
import plotly.express as px

continent_map = {
    'africa': ['algeria', 'angola', 'benin', 'botswana', 'burkina faso', 'burundi', 'cabo verde', 'cameroon', 'central african republic', 'chad', 'comoros', 'congo', 'democratic republic of the congo', 'djibouti', 'egypt', 'equatorial guinea', 'eritrea', 'eswatini', 'ethiopia', 'gabon', 'gambia', 'ghana', 'guinea', 'guinea-bissau', 'ivory coast', 'kenya', 'lesotho', 'liberia', 'libya', 'madagascar', 'malawi', 'mali', 'mauritania', 'mauritius', 'morocco', 'mozambique', 'namibia', 'niger', 'nigeria', 'rwanda', 'sao tome and principe', 'senegal', 'seychelles', 'sierra leone', 'somalia', 'south africa', 'south sudan', 'sudan', 'tanzania', 'togo', 'tunisia', 'uganda', 'zambia', 'zimbabwe', "côte d'ivoire", 'sao tome & principe', 'dr congo', 'centr afric re', 'united republic of tanzania'],
    'asia': ['afghanistan', 'armenia', 'azerbaijan', 'bahrain', 'bangladesh', 'bhutan', 'brunei darussalam', 'cambodia', 'china', "people's republic of china", "democratic people's republic of korea", 'georgia', 'india', 'indonesia', 'iran', 'iraq', 'israel', 'japan', 'jordan', 'kazakhstan', 'korea', 'republic of korea', 'kuwait', 'kyrgyzstan', "lao people's democratic republic", 'lebanon', 'malaysia', 'maldives', 'mongolia', 'myanmar', 'nepal', 'oman', 'pakistan', 'palestine', 'philippines', 'qatar', 'saudi arabia', 'singapore', 'sri lanka', 'syrian arab republic', 'taipei', 'chinese taipei', 'tajikistan', 'thailand', 'timor-leste', 'turkmenistan', 'united arab emirates', 'uzbekistan', 'vietnam', 'yemen', 'ua emirates', 'ir iran', 'syria', 'dpr korea', 'hong kong, china', 'türkiye', 'lao pdr', 'democratic republic of timor-leste', 'islamic republic of iran'],
    'europe': ['albania', 'andorra', 'austria', 'belarus', 'belgium', 'bosnia and herzegovina', 'bulgaria', 'croatia', 'cyprus', 'czechia', 'denmark', 'estonia', 'finland', 'france', 'germany', 'greece', 'hungary', 'iceland', 'ireland', 'italy', 'latvia', 'liechtenstein', 'lithuania', 'luxembourg', 'malta', 'monaco', 'montenegro', 'netherlands', 'north macedonia', 'norway', 'poland', 'portugal', 'moldova', 'romania', 'russia', 'san marino', 'serbia', 'slovakia', 'slovenia', 'spain', 'sweden', 'switzerland', 'ukraine', 'united kingdom', 'great britain', 'republic of moldova', 'kosovo', 'bosnia & herzegovina'],
    'north america': ['antigua and barbuda', 'bahamas', 'barbados', 'belize', 'canada', 'costa rica', 'cuba', 'dominica', 'dominican republic', 'el salvador', 'grenada', 'guatemala', 'haiti', 'honduras', 'jamaica', 'mexico', 'nicaragua', 'panama', 'saint kitts and nevis', 'saint lucia', 'st vincent and the grenadines', 'trinidad and tobago', 'united states of america', 'united states', 'virgin islands, us', 'virgin islands, british', 'puerto rico', 'cayman islands', 'stvincent&grenadines', 'bermuda', 'aruba', 'virgin islands, b'],
    'south america': ['argentina', 'bolivia', 'brazil', 'chile', 'colombia', 'ecuador', 'guyana', 'paraguay', 'peru', 'suriname', 'uruguay', 'venezuela'],
    'oceania': ['australia', 'cook islands', 'fiji', 'kiribati', 'marshall islands', 'federated states of micronesia', 'nauru', 'new zealand', 'palau', 'papua new guinea', 'samoa', 'solomon islands', 'tonga', 'tuvalu', 'vanuatu', 'micronesia', 'guam', 'american samoa'],
    'other': ['ain', 'refugee olympic team']
}

def map_country_to_continent(country):
    for continent, countries in continent_map.items():
        if country in countries:
            return continent
    return 'unknown'  

def load_data():
    athletes_df = pd.read_csv('../data/athletes.csv')
    athletes_df['country'] = athletes_df['country_long'].str.lower()
    athletes_df['continent'] = athletes_df['country'].apply(map_country_to_continent)
    athletes_df['Age'] = 2025 - pd.to_datetime(athletes_df['birth_date']).dt.year
    bins = list(range(athletes_df['Age'].min(), athletes_df['Age'].max() + 5, 5))
    labels = [f'{i}-{i+4}' for i in range(athletes_df['Age'].min(), athletes_df['Age'].max(), 5)]
    athletes_df['Age Group'] = pd.cut(athletes_df['Age'], bins=bins, labels=labels, right=False)
    return athletes_df

def group_by_country_and_age(df):
    grouped_df = df.groupby(['country', 'Age Group']).size().reset_index(name='Count')
    return grouped_df

def clean_data(df):
    df = df[['name', 'country', 'continent', 'Age', 'Age Group']]
    return df

def continents(df):
    continents = df['continent'].unique()
    return continents


def vis_2():
    df = pd.read_csv('../data/athletes.csv')
    
    def safe_eval(val):
        try:
            return ast.literal_eval(val) if isinstance(val, str) else val
        except (ValueError, SyntaxError):
            print(f"Erreur d'évaluation : {val}")
            return []
    
    df['country'] = df['country_long'].str.lower()
    df['continent'] = df['country'].apply(map_country_to_continent)
    df['Age'] = 2025 - pd.to_datetime(df['birth_date']).dt.year
    bins = list(range(df['Age'].min(), df['Age'].max() + 5, 5))
    labels = [f'{i}-{i+4}' for i in range(df['Age'].min(), df['Age'].max(), 5)]
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    grouped_df = df.groupby(['country', 'Age Group']).size().reset_index(name='Count')

    df = df[['name', 'country', 'continent', 'Age', 'Age Group']]

    continents = df['continent'].unique()

    for continent in continents:
        continent_df = df[df['continent'] == continent]
        grouped_df = continent_df.groupby(['country', 'Age Group']).size().reset_index(name='Count')
        pivot_df = grouped_df.pivot(index='country', columns='Age Group', values='Count')
        pivot_df = pivot_df.fillna(0)
        plt.figure(figsize=(20, 10))
        sns.heatmap(pivot_df, cmap='Reds', linewidths=0.5)
        plt.title(f'Number of athletes by age and country in {continent}')
        plt.show()

def vis_2_plotly():
    df = pd.read_csv('../data/athletes.csv')
    
    df['country'] = df['country_long'].str.lower()
    df['continent'] = df['country'].apply(map_country_to_continent)
    df['Age'] = 2025 - pd.to_datetime(df['birth_date']).dt.year
    bins = list(range(df['Age'].min(), df['Age'].max() + 5, 5))
    labels = [f'{i}-{i+4}' for i in range(df['Age'].min(), df['Age'].max(), 5)]
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    all_data = {}
    continents = df['continent'].unique()
    
    for continent in continents:
        continent_df = df[df['continent'] == continent]
        grouped_df = continent_df.groupby(['country', 'Age Group']).size().reset_index(name='Count')
        pivot_df = grouped_df.pivot(index='country', columns='Age Group', values='Count').fillna(0)
        pivot_df = pivot_df.reset_index()
        melted_df = pd.melt(pivot_df, id_vars=['country'], var_name='Age Group', value_name='Count')
        all_data[continent] = melted_df
    
    fig = px.density_heatmap(
        all_data[continents[0]],  
        x='Age Group',
        y='country',
        z='Count',
        color_continuous_scale='Reds',
        title=f'Number of athletes by age and country in {continents[0].capitalize()}',
        labels={'country': 'Country', 'Age Group': 'Age Group', 'Count': 'Number of Athletes'},
        height=600,
        width=1000
    )
    
    fig.update_layout(
        xaxis_title='Age Group',
        yaxis_title='Country',
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_colorbar_title='Count',
        updatemenus=[{
            'buttons': [
                {
                    'label': continent.capitalize(),
                    'method': 'update',
                    'args': [
                        {'z': [all_data[continent]['Count']],
                         'y': [all_data[continent]['country']],
                         'x': [all_data[continent]['Age Group']],
                         'title': f'Number of athletes by age and country in {continent.capitalize()}'
                        }
                    ]
                } for continent in continents
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0.1,
            'y': 1.15
        }]
    )
    
    fig.show()
vis_2_plotly()