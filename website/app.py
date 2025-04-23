from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from visualisation_1 import setup_viz_1
from visualisation_2 import setup_viz_2
from visualisation_3 import setup_viz_3
from visualisation_5 import setup_viz_5
from visualisation_6 import setup_viz_6 
from visualisation_7 import setup_vis_7

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap'
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

parallax_sections = [
    {
        'title': "bla bla bla",
        'description': "bla bla bla",
        'viz': setup_viz_1(app),
        'bg_color': '#2c3e50',
        'text_color': '#ecf0f1'
    },
    {
        'title': "bla bla bla",
        'description': "bla bla bla",
        'viz': setup_viz_2(app),
        'bg_color': '#3498db',
        'text_color': '#ffffff'
    },
    {
        'title': "bla bla bla",
        'description': "bla bla bla",
        'viz': setup_viz_3(app),
        'bg_color': '#e74c3c',
        'text_color': '#ffffff'
    },
    {
        'title': "bla bla bla",
        'description': "bla bla bla",
        'viz': setup_viz_5(app),
        'bg_color': '#2ecc71',
        'text_color': '#ffffff'
    },
    {
        'title': "bla bla bla", 
        'description': "bla bla bla",
        'viz': setup_viz_6(app),
        'bg_color': '#9b59b6',
        'text_color': '#ffffff'
    },
    {
        'title': "bla bla bla",
        'description': "bla bla bla",
        'viz': setup_vis_7(app),
        'bg_color': '#1abc9c',
        'text_color': '#ffffff'
    }
]

parallax_children = []
for i, section in enumerate(parallax_sections):
    parallax_children.extend([
        html.Div(
            id=f'section-{i}',
            className='parallax-section',
            style={
                'height': '100vh',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'backgroundColor': section['bg_color'],
                'color': section['text_color'],
                'padding': '40px',
                'position': 'relative',
                'overflow': 'hidden',
                'textAlign': 'center'
            },
            children=[
                html.Div(
                    id=f'content-{i}',
                    className='parallax-content',
                    style={
                        'maxWidth': '1000px',
                        'margin': '0 auto',
                        'opacity': 0,
                        'transform': 'translateY(50px)',
                        'transition': 'all 0.8s ease-out',
                        'zIndex': 2
                    },
                    children=[
                        html.H2(
                            section['title'],
                            style={
                                'fontSize': '3rem',
                                'marginBottom': '20px',
                                'fontFamily': 'Montserrat, sans-serif',
                                'fontWeight': '700'
                            }
                        ),
                        html.P(
                            section['description'],
                            style={
                                'fontSize': '1.2rem',
                                'marginBottom': '40px',
                                'fontFamily': 'Montserrat, sans-serif',
                                'fontWeight': '300',
                                'lineHeight': '1.6'
                            }
                        ),
                        html.Div(
                            style={
                                'backgroundColor': 'rgba(84, 84, 84, 1)',
                                'padding': '20px',
                                'borderRadius': '8px',
                                'boxShadow': '0 4px 20px rgba(0,0,0,0.2)'
                            },
                            children=[section['viz']]
                        )
                    ]
                )
            ]
        ),
        html.Div(style={'height': '5px', 'backgroundColor': '#f8f9fa'}) if i < len(parallax_sections)-1 else None
    ])

app.layout = html.Div(
    id='main-container',
    style={'backgroundColor': '#f8f9fa'},
    children=[
        html.Div(
            style={
                'height': '100vh',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'backgroundColor': '#2c3e50',
                'color': 'white',
                'textAlign': 'center',
                'position': 'relative',
                'overflow': 'hidden'
            },
            children=[
                html.H1(
                    "Analyses des Jeux Olympiques de Paris 2024",
                    style={
                        'fontSize': '4rem',
                        'marginBottom': '20px',
                        'fontFamily': 'Montserrat, sans-serif',
                        'fontWeight': '700',
                        'textShadow': '2px 2px 4px rgba(0,0,0,0.3)',
                        'zIndex': 2
                    }
                ),
                html.P(
                    "Une exploration de l'histoire et des tendances olympiques basée sur les données",
                    style={
                        'fontSize': '1.5rem',
                        'maxWidth': '800px',
                        'marginBottom': '40px',
                        'fontFamily': 'Montserrat, sans-serif',
                        'fontWeight': '300',
                        'zIndex': 2
                    }
                ),
                html.Div(
                    "Faites défiler pour explorer",
                    style={
                        'position': 'absolute',
                        'bottom': '40px',
                        'left': '50%',
                        'transform': 'translateX(-50%)',
                        'animation': 'bounce 2s infinite',
                        'zIndex': 2
                    }
                )
            ]
        ),
        
        *parallax_children,
        
        html.Div(style={'display': 'none'}, children=[
            dcc.Markdown("""
                <style>
                    @keyframes bounce {
                        0%, 20%, 50%, 80%, 100% {transform: translateY(0) translateX(-50%);}
                        40% {transform: translateY(-20px) translateX(-50%);}
                        60% {transform: translateY(-10px) translateX(-50%);}
                    }
                    
                    .parallax-section {
                        scroll-snap-align: start;
                    }
                    
                    body {
                        scroll-snap-type: y proximity;
                        overflow-y: scroll;
                    }
                </style>
            """)
        ]),
        
        dcc.Store(id='scroll-position-store')
    ]
)

app.clientside_callback(
    """
    function() {
        // This will run when the page loads
        const sections = document.querySelectorAll('.parallax-section');
        
        function checkScroll() {
            sections.forEach(section => {
                const content = section.querySelector('.parallax-content');
                const sectionTop = section.getBoundingClientRect().top;
                const windowHeight = window.innerHeight;
                
                // If section is in view
                if (sectionTop < windowHeight * 0.75 && sectionTop > -windowHeight * 0.25) {
                    content.style.opacity = 1;
                    content.style.transform = 'translateY(0)';
                }
            });
        }
        
        // Run once on load
        checkScroll();
        
        // Then run on scroll
        window.addEventListener('scroll', checkScroll);
        
        return window.scrollY;
    }
    """,
    Output('scroll-position-store', 'data'),
    Input('main-container', 'children')
)


if __name__ == '__main__':
    app.run_server(debug=True)
    