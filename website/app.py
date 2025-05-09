from dash import Dash, html, dcc, Input, Output
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
        'title': "Les jeunes dominent",
        'description': "Les athlètes dans la vingtaine ont largement dominé les JO, avec une nette chute de représentation après la trentaine. Les sports collectifs, les sports de combat et l'athlétisme sont les disciplines les plus représentées.",
        'viz': setup_viz_1(app),
        'bg_color': '#2c3e50',
        'text_color': '#ecf0f1'
    },
    {
        'title': "Les jeunes dominent... partout dans le monde?",
        'description': "Lorsqu'on regarde la distribution des athlètes dans le monde, il est clair que les athlètes dans la vingtaine sont encore en majorité. On voit donc que la majorité des athlètes envoyés aux olympiques font des disciplines plus demandantes physiquement.",
        'viz': setup_viz_2(app),
        'bg_color': '#3498db',
        'text_color': '#ffffff'
    },
    {
        'title': "Pays différent, sports différents!",
        'description': "Certains pays ont remporté beaucoup plus de médailles olympiques que d'autres dans certaines disciplines. Un sport pourrait être plus pratiqué dans un pays en particulier à cause de sa culture sportive et des conditions météorologiques ou géographiques, par exemple.",
        'viz': setup_viz_3(app),
        'bg_color': '#e74c3c',
        'text_color': '#ffffff'
    },
    {
        'title': "Gym à 16 ans, tir à 50 : les médailles racontent tout",
        'description': "On voit que les médailles d'or se concentrent plus sur des disciplines dites traditionnelles comme l'athlétisme et la natation. \n "
        "À l'inverse, les médailles de bronze sont beaucoup plus dispersées entre les disciplines. \n "
        "Les sports moins physiques comme l'équitation ou le tir permettent des carrières plus longues, avec des médaillés dans la cinquantaine. Cela est l'inverse de certains sports comme la gymnastique.",
        'viz': setup_viz_5(app),
        'bg_color': '#2ecc71',
        'text_color': '#ffffff'
    },
    {
        'title': "Mais, qui sont réellement les meilleurs?", 
        'description': "Il est certe possible de qualifier le pays ayant remporté le plus médailles comme étant le gagnant des jeux olympiques. "
        "Cette méthode n'est toutefois pas réellement juste; le nombre de médailles gagnées en fonction du nombre d'athlètes envoyés nous donne une meilleure idée de quels pays ont le mieux performé en 2024.",
        'viz': setup_viz_6(app),
        'bg_color': '#9b59b6',
        'text_color': '#ffffff'
    },
    {
        'title': "Au sommet du sport",
        'description': "Une corrélation claire existe entre la grandeur des athlètes et le sport pratiqué. Cependant, on voit que la grandeur n'est pas aussi importante en badminton qu'en basketball par exemple. Comme quoi, tout le monde peut faire du sport!",
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
                        'width': '90%',
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
                                'fontSize': '3.5rem',
                                'marginBottom': '20px',
                                'fontFamily': 'Montserrat, sans-serif',
                                'fontWeight': '700'
                            }
                        ),
                        html.P(
                            section['description'],
                            style={
                                'fontSize': '2.5rem',
                                'marginBottom': '20px',
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
                                'boxShadow': '0 4px 20px rgba(0,0,0,0.2)',
                                'width': '100%',
                                
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
                html.Img(src=app.get_asset_url('logo.png')),
                html.H1(
                    "Analyses des Jeux Olympiques de Paris 2024",
                    style={
                        'fontSize': '6rem',
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
                        'fontSize': '5rem',
                        'maxWidth': '800px',
                        'marginBottom': '40px',
                        'fontFamily': 'Montserrat, sans-serif',
                        'fontWeight': '300',
                        'zIndex': 2, 
                    }
                ),
                html.P("Par: Stefan Cotargasanu, Jacob Ducas, Justine Ouellette, Marianna Prud'homme, Faneva Rakotoarivony et Saad Bouasla,",
                       style={
                        'fontSize': '2rem',
                        'maxWidth': '800px',
                        'marginBottom': '40px',
                        'fontFamily': 'Montserrat, sans-serif',
                        'fontWeight': '300',
                        'zIndex': 2, 
                       }),
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
        const sections = document.querySelectorAll('.parallax-section');
        function checkScroll() {
            sections.forEach(section => {
                const content = section.querySelector('.parallax-content');
                const sectionTop = section.getBoundingClientRect().top;
                const windowHeight = window.innerHeight;
                if (sectionTop < windowHeight * 0.75 && sectionTop > -windowHeight * 0.25) {
                    content.style.opacity = 1;
                    content.style.transform = 'translateY(0)';
                }
            });
        }
        checkScroll();
        window.addEventListener('scroll', checkScroll);
        return window.scrollY;
    }
    """,
    Output('scroll-position-store', 'data'),
    Input('main-container', 'children')
)


if __name__ == '__main__':
    app.run_server(debug=True)
    
