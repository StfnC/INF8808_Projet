from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

DATA_PATH = './data'

def load_data():
    medals_df = pd.read_csv(f'{DATA_PATH}/medals_total.csv')
    athletes_df = pd.read_csv(f'{DATA_PATH}/athletes.csv')
    return medals_df, athletes_df

def clean_up_medals(medals_df: pd.DataFrame) -> pd.DataFrame:
    return medals_df.drop(columns=['Gold Medal', 'Silver Medal', 'Bronze Medal'])

def total_athletes_per_country(df: pd.DataFrame) -> pd.DataFrame:
    country_df = df['country_code'].value_counts().reset_index()
    country_df.columns = ['country_code', 'total_athletes']
    return country_df.sort_values(by='total_athletes', ascending=False)

def calculate_efficiency_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df['efficiency_score'] = (df['Total'] * np.log(df['total_athletes'])) / df['total_athletes']
    df['norm_efficiency'] = (df['efficiency_score'] - df['efficiency_score'].min()) / \
        (df['efficiency_score'].max() - df['efficiency_score'].min())
    return df

def create_visualization(combined_df: pd.DataFrame):
    app = Dash(__name__)
    top_countries = combined_df.nlargest(25, 'Total')
    
    fig = px.scatter(top_countries,
                    x='total_athletes',
                    y='Total',
                    color='norm_efficiency',
                    size='Total',
                    hover_name='country',
                    text='country_code',
                    color_continuous_scale='Hot',
                    labels={
                        'total_athletes': 'Nombre d\'athlètes',
                        'Total': 'Total des médailles',
                        'norm_efficiency': 'Efficacité',
                    },
                    title="Efficacité des médailles : Total des médailles vs Nombre d'athlètes (Top 25 pays)",
                    trendline="ols")  

    fig.update_layout(
        height=800, 
        autosize=True,
        margin=dict(l=50, r=50, b=100, t=100, pad=4)
    )
    fig.update_traces(
        marker=dict(opacity=0.8, line=dict(width=0.5, color='DarkSlateGrey')),
        textposition='top center',
        selector=dict(mode='markers+text')
    )
    
    for trace in fig.data:
        if trace.mode == 'lines':
            trace.line.color = 'rgba(255, 0, 0, 0.7)'  
            trace.line.width = 3
            trace.line.dash = 'dash'
            trace.name = 'Tendance'
    
    fig.update_layout(
        xaxis_title="Nombre d\'athlètes",
        yaxis_title="Total des médailles",
        coloraxis_colorbar=dict(title="Efficacité"),
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    for trace in fig.data:
        if trace.mode == 'markers+text':
            trace.hovertemplate = '<b>%{hovertext}</b><br>' \
                                 'Nombre d\'athlètes: %{x}<br>' \
                                 'Total de médailles: %{y}<br>' \
                                 'Efficacité: %{marker.color:.2f}'
    
    app.layout = html.Div([
        dcc.Graph(figure=fig,
                  style={'height': '90vh'})
    ])
    
    app.run(debug=True)

def preprocess():
    medals_df, athletes_df = load_data()
    medals_df = clean_up_medals(medals_df)
    athletes_df = total_athletes_per_country(athletes_df)
    combined_df = pd.merge(medals_df, athletes_df, on='country_code', how='inner')
    combined_df = calculate_efficiency_metrics(combined_df)
    create_visualization(combined_df)

if __name__ == "__main__":
    preprocess()

def setup_viz_6(app):
    medals_df, athletes_df = load_data()
    medals_df = clean_up_medals(medals_df)
    athletes_df = total_athletes_per_country(athletes_df)
    combined_df = pd.merge(medals_df, athletes_df, on='country_code', how='inner')
    combined_df = calculate_efficiency_metrics(combined_df)

    top_countries = combined_df.nlargest(25, 'Total')

    def create_figure(filtered_df):
        fig = px.scatter(filtered_df,
                         x='total_athletes',
                         y='Total',
                         color='norm_efficiency',
                         size='Total',
                         hover_name='country',
                         text='country_code',
                         color_continuous_scale='Hot',
                         labels={
                             'total_athletes': "Nombre d'athlètes",
                             'Total': "Total des médailles",
                             'norm_efficiency': "Efficacité"
                         },
                         title="Efficacité des médailles : Total vs Nombre d'athlètes (Top 25)",
                         trendline="ols")

        fig.update_layout(height=800, autosize=True, margin=dict(l=50, r=50, b=100, t=100))
        fig.update_traces(marker=dict(opacity=0.8, line=dict(width=0.5, color='DarkSlateGrey')),
                          textposition='top center',
                          selector=dict(mode='markers+text'))
        for trace in fig.data:
            if trace.mode == 'lines':
                trace.line.color = 'rgba(255, 0, 0, 0.7)'
                trace.line.width = 3
                trace.line.dash = 'dash'
                trace.name = 'Tendance'
            elif trace.mode == 'markers+text':
                trace.hovertemplate = '<b>%{hovertext}</b><br>' \
                                      'Nombre d\'athlètes: %{x}<br>' \
                                      'Total de médailles: %{y}<br>' \
                                      'Efficacité: %{marker.color:.2f}'

        return fig

    @app.callback(
        Output("graph6", "figure"),
        Input("country-dropdown", "value")
    )
    def update_graph(selected_country):
        if selected_country == "all":
            df = top_countries
        else:
            df = top_countries[top_countries['country_code'] == selected_country]
        return create_figure(df)

    return html.Div([
        html.H1("Efficacité des Médailles"),
        html.P("Filtrer par pays"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": "Tous", "value": "all"}] +
                    [{"label": row['country'], "value": row['country_code']} for _, row in top_countries.iterrows()],
            value="all"
        ),
        dcc.Graph(id="graph6")
    ])
