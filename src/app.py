'''
 # Dash port of Shiny iris k-means example:
 # https://shiny.rstudio.com/gallery/kmeans-example.html
 # Source: https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/
 # @ Create Time: 2024-01-30 19:33:40.329463
 # Run this app with `python app.py` and
 # visit http://127.0.0.1:8050/ in your web browser.
'''
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, dcc, html
from sklearn import datasets
from sklearn.cluster import KMeans
import plotly as px

# Replace the existing dataset and related code with your data
data = {
    'Main_Category': ['Talent',
                      'Mentaliteit', 'Mentaliteit', 'Mentaliteit',
                      'Opleiding', 'Opleiding',
                      'Familie', 'Familie'],
    'Sub_Category': ['Talent',
                     'Motivatie', 'Tactiek', 'Wedstrijdspanning/concentratie',
                     'Opleidingsniveau', 'Vertrouwensband trainer en speler',
                     'Financiën', 'Steun en thuissituatie'],
    'Rank': [9, 8.9, 8.2, 7, 8.2, 8.5, 8.4, 8]
}

# Define colors for main categories
main_category_colors = ['red', 'green', 'purple', 'orange']
main_categories = ['Talent', 'Mentaliteit', 'Opleiding', 'Familie']

# Create subcategories list and corresponding ranks
subcategories = data['Sub_Category']
ranks = data['Rank']

# Replace the existing dataset and related code with your data
predefined_values = {subcategory: rank for subcategory, rank in zip(subcategories, ranks)}
predefined_values_list = [predefined_values[subcategory] for subcategory in subcategories]

# Convert your data to a DataFrame
df = pd.DataFrame(data)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    title="SuccesFactorenTennis",
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'],
    )

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

controls = dbc.Card(
    [
        html.Div(
            [
                html.H2('Subcategorieën', style={'textAlign': 'center'}),
                html.Hr(style={'borderWidth': '3px'}),
                html.Label("Hoe sterk ben je in deze onderdelen? Selecteer een waarde tussen de 1-10"),
                html.Hr(style={'borderWidth': '3px'}),
                *[html.Div(
                    [
                        dbc.Label(f"{subcategory}"),
                        # dbc.Input(id=f"{subcategory.lower()}", type="number", value=3),
                        html.Div(
                        dcc.Slider(min=1, max=10, step=1, value=1, id=f"{subcategory.lower()}"),
                        style={'padding-bottom': '15px'},
                        ),
                    ],
                ) for subcategory in subcategories],
                html.Button('Indienen', id='go-button', n_clicks=0, style={'margin-top': '25px'})
            ]
        ),
    ],
    body=True,
    style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '20%',
        'padding': '20px 10px',
        'background-color': '#f8f9fa',
        'width': '20%',
        'font-size': '20px',
        'overflowY': 'scroll', 
    },
)

app.layout = dbc.Container(
    [
        dbc.Row(
             [
                dbc.Col(controls, md=3, align='start', style={'overflowY': 'scroll',},
                ),      
                dbc.Col(
                    [
                        html.H2('Succesfactoren Tennis', style={'textAlign': 'center', 'marginTop': '49px', 'backgroundColor': 'white'}),
                        html.Hr(style={'borderWidth': '3px', 'position': 'sticky', 'top': 0, 'zIndex': 1000}),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id="bar-chart"), md=12),
                        ]),
                        dbc.Row([
                            dbc.Col(
                                            [
                                                html.Hr(style={'borderWidth': '3px'}),
                                                html.H3("Verbeterpunten", className="card-title"),
                                                html.Div(id='text-output'),
                                            ]
                            ),
                        ]),
                    ],
                    md=8,
                    align='start',
                ),
            ],
            align="center", style={'margin-bottom': '20px', 'font-size': '20px'},
        ),
    ],
    fluid=True,
    style={'zoom': 0.8}
)

# Update the update_chart function to use your DataFrame
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('go-button', 'n_clicks')],
    [dash.dependencies.State(f'{subcategory.lower()}', 'value') for subcategory in subcategories]

)
def update_chart(n_clicks, *user_data):
    if n_clicks > 0 and all(value is not None for value in user_data):
        
        # Define colors for legend based on main categories
        legend_colors = {'Talent': '#FFA15A', 'Mentaliteit': '#EF553B', 'Opleiding': '#00CC96', 'Familie': '#AB63FA'}

        colors = ["#FFA15A", "#EF553B", "#EF553B", "#EF553B", "#00CC96", "#00CC96", "#AB63FA", "#AB63FA", 
         "#636EFA", "#636EFA","#636EFA","#636EFA","#636EFA","#636EFA","#636EFA","#636EFA"]

        user_values = list(user_data)

        # Create DataFrame with user and predefined data
        df = pd.DataFrame({
            'Main Category': main_categories * 4,
            'Subcategory': subcategories * 2,
            'Value': user_values + predefined_values_list,
            'Type': ['User'] * len(user_values) + ['Predefined'] * len(predefined_values),
            'Color': colors
        })

        # Create separate traces for 'User' and 'Predefined'
        traces = []
        for typ, color in zip(['User', 'Predefined'], [main_category_colors[0], '#636EFA']):
            sub_df = df[df['Type'] == typ]
            traces.append(go.Bar(x=sub_df['Subcategory'], y=sub_df['Value'], name=typ, marker_color=sub_df['Color'], showlegend=False,  text=sub_df['Value'],  # Display rank values as text above each bar
                textposition='auto',))

        fig = go.Figure(data=traces)

        # Add legend to the chart with legend groups for each main category
        for main_category, color in legend_colors.items():
            fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color=color, symbol='square'), showlegend=True,
                                     name=main_category))

        fig.update_layout(
            barmode='group',
            xaxis=dict(tickmode='array', tickvals=subcategories, ticktext=subcategories),
            title='Vergelijking subcategorieën drempelwaarde',
            xaxis_title='Subcategorie',
            yaxis_title='Score'
        )
        fig.update_layout(
            title_font_size=24,
            xaxis=dict(tickfont=dict(size=14)),
            yaxis=dict(tickfont=dict(size=14)),
            legend=dict(title_font=dict(size=16), font=dict(size=14)),
        )

        return fig
    else:
        # If the button is not clicked or any field is not filled, return an empty chart
        return {'data': [], 'layout': {}}


# Define texts for each subcategory
subcategory_texts = {
    'Talent': 'Snelle vezels in je spieren op jonge leeftijd ontwikkelen zodat je dat talent benut. Een fysieke trainer hebben is hiervoor belangrijk. Verder heb je talent of je hebt het niet.',
    'Motivatie': 'Plezier behouden, progressie boeken, wedstrijd winnen, sociale contacten in het tennis behouden.',
    'Tactiek': 'Veel wedstrijden spelen om tennis-tactisch te verbeteren. Daarnaast trainen op vaste patronen in de rally.',
    'Wedstrijdspanning/concentratie': 'Leg de focus op HOE je de wedstrijd wil winnen en niet dat je de wedstrijd MOET winnen',
    'Opleidingsniveau': 'Zoek uit op welk vlak jij extra hulp nodig hebt: technisch/tactisch/fysiek. Zoek hiervoor de juiste mensen',
    'Vertrouwensband trainer en speler': 'Wees eerlijk, zorg voor transparantie tussen de ouders, spelers en trainers.',
    'Financiën': 'Probeer sponsoren te zoeken. Het blijkt dat de invloed niet heel groot is, maar toch kan dit helpen.',
    'Steun en thuissituatie': 'Laat als speler zien dat je ervooro wilt gaan. Ouders hebben er dan ook meer voor over. Daarnaast moeten ouders goed onderzoeken en leren way een speler nodig heeft van de ouders. Hier zijn lessen voor beschikbaar.',
}

@app.callback(
    Output('text-output', 'children'),
    [Input('go-button', 'n_clicks')],
    [dash.dependencies.State(f'{subcategory.lower()}', 'value') for subcategory in subcategories]
)
def update_text(n_clicks, *user_data):
    if n_clicks > 0 and all(value is not None for value in user_data):
        # Assuming you want to display the subcategories with values smaller than the predefined values
        smaller_subcategories = [subcategories[i] for i, value in enumerate(user_data) if value < predefined_values_list[i]]
        
        if smaller_subcategories:
            text_output = html.Div([
                html.H4("Bij de volgende categorieën heb je onder de drempelwaarde gescoord: ", className="card-title"),
                html.Ul([
                    html.Li([html.B(subcategory), f": {subcategory_texts[subcategory]}" ]) for subcategory in smaller_subcategories
                ]),
                html.Hr(),
                html.H4("Showstoppers: "),
                html.Ul([
                    html.Li("Het plezier verliezen in de sport."),
                    html.Li("Een slechte instelling hebben, je moet het willen."),
                    html.Li("Slechte ondersteuning van ouders."),
                    html.Li("Te weinig financien hebben voor de sport."),
                    html.Li("Een ongezonde levensstijl hebben waarbij slecht eten, te weinig slaap en alcohol centraal staat.")
                ]),
            ])
        else:
            text_output = html.Div([
                html.H4("Alle categorieen zijn op goed niveau!"),
                html.Hr(),
                html.H4("Showstoppers: "),
                html.Ul([
                    html.Li("Het plezier verliezen in de sport."),
                    html.Li("Een slechte instelling hebben, je moet het willen."),
                    html.Li("Slechte ondersteuning van ouders."),
                    html.Li("Te weinig financien hebben voor de sport."),
                    html.Li("Een ongezonde levensstijl hebben waarbij slecht eten, te weinig slaap en alcohol centraal staat.")
                ]),
                ])
        
        return text_output
    else:
        return html.Div("Vul de subcategorie velden in om je resultaten te zien.")

    
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)