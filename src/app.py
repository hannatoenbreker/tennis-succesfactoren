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


# Replace the existing dataset and related code with your data
data = {
    'Main_Category': ['Category A', 'Category A', 'Category A', 'Category A',
                      'Category B', 'Category B', 'Category B', 'Category B',
                      'Category C', 'Category C', 'Category C', 'Category C',
                      'Category D', 'Category D', 'Category D', 'Category D',
                      'Category E', 'Category E', 'Category E', 'Category E',
                      'Category F', 'Category F', 'Category F', 'Category F'],
    'Sub_Category': ['Subcategory 1', 'Subcategory 2', 'Subcategory 3', 'Subcategory 4',
                     'Subcategory 5', 'Subcategory 6', 'Subcategory 7', 'Subcategory 8',
                     'Subcategory 9', 'Subcategory 10', 'Subcategory 11', 'Subcategory 12',
                     'Subcategory 13', 'Subcategory 14', 'Subcategory 15', 'Subcategory 16',
                     'Subcategory 17', 'Subcategory 18', 'Subcategory 19', 'Subcategory 20',
                     'Subcategory 21', 'Subcategory 22', 'Subcategory 23', 'Subcategory 24'],
    'Rank': [8, 5, 7, 9, 4, 6, 3, 8, 2, 7, 6, 9, 1, 3, 5, 7, 2, 6, 8, 4, 1, 9, 4, 6]
}

# Define colors for main categories
main_category_colors = ['blue', 'green', 'red', 'purple', 'orange']
main_categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
subcategories = [f'Subcategory {i+1}' for i in range(15)]

# Predefined values for 5 main categories, each with 3 subcategories
predefined_values = {f'Subcategory {i+1}': 5 for i in range(15)}
predefined_values_list = [predefined_values[subcategory] for subcategory in subcategories]

# Convert your data to a DataFrame
df = pd.DataFrame(data)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    title="SuccesFactorsTennis",
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'],
    )

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

controls = dbc.Card(
    [
        html.Div(
            [
                html.Label("Subcategories"),
                *[html.Div(
                    [
                        dbc.Label(f"{subcategory}"),
                        dbc.Input(id=f"{subcategory.lower()}-cluster-count", type="number", value=3),
                    ]
                ) for subcategory in subcategories],
                html.Button('Go', id='go-button', n_clicks=0)
            ]
        ),
    ],
    body=True,
)
app.layout = dbc.Container(
    [
        html.H1("Succesfactoren tennis test"),
        html.Hr(),
        dbc.Row(
             [
                dbc.Col(controls, md=4, align='start', style={'overflow-y': 'scroll', 'max-height': '1000px', 'scrollbar-width': 'thin', 'scrollbar-color': 'darkgrey lightgrey',},
                ),      
                dbc.Col(
                    [
                        dbc.Row([
                            dbc.Col(dcc.Graph(id="bar-chart"), md=12),
                        ]),
                        dbc.Row([
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H4("Text Output", className="card-title"),
                                                html.Div(id='text-output'),
                                            ]
                                        )
                                    ]
                                ),
                                md=12,
                            ),
                        ]),
                    ],
                    md=8,
                    align='start',
                ),
            ],
            align="center", style={'margin-bottom': '20px'},
        ),
    ],
    fluid=True,
)


# Update the update_chart function to use your DataFrame
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('go-button', 'n_clicks')],
    [dash.dependencies.State(f'subcategory {i+1}-cluster-count', 'value') for i in range(15)]
)
def update_chart(n_clicks, *user_data):
    if n_clicks > 0 and all(value is not None for value in user_data):
        
        color = ["red", "red", "red", "green", "green", "green", "orange", "orange", "orange", "yellow", "yellow", "yellow", "purple", "purple", "purple", 
         "blue", "blue","blue","blue","blue","blue","blue","blue","blue","blue","blue","blue","blue","blue","blue"]
        user_values = list(user_data)

        # Create DataFrame with user and predefined data
        df = pd.DataFrame({
            'Main Category': main_categories * 6,
            'Subcategory': subcategories * 2,
            'Value': user_values + predefined_values_list,
            'Type': ['User'] * len(user_values) + ['Predefined'] * len(predefined_values),
            'Color': color
        })

        # Create separate traces for 'User' and 'Predefined'
        traces = []
        for typ, color in zip(['User', 'Predefined'], [main_category_colors[0], 'blue']):
            sub_df = df[df['Type'] == typ]
            traces.append(go.Bar(x=sub_df['Subcategory'], y=sub_df['Value'], name=typ, marker_color=sub_df['Color']))

        fig = go.Figure(data=traces)

        fig.update_layout(
            barmode='group',
            xaxis=dict(tickmode='array', tickvals=subcategories, ticktext=subcategories),
            title='Category Rankings Comparison',
            xaxis_title='Subcategory',
            yaxis_title='Ranking'
        )

        return fig
    else:
        # If the button is not clicked or any field is not filled, return an empty chart
        return {'data': [], 'layout': {}}

@app.callback(
    Output('text-output', 'children'),
    [Input('go-button', 'n_clicks')],
    [dash.dependencies.State(f'subcategory {i+1}-cluster-count', 'value') for i in range(15)]
)
def update_text(n_clicks, *user_data):
    if n_clicks > 0 and all(value is not None for value in user_data):
        # Assuming you want to display the subcategories with values smaller than the predefined values
        smaller_subcategories = [subcategories[i] for i, value in enumerate(user_data) if value < predefined_values_list[i]]
        
        if smaller_subcategories:
            text_output = html.Div([
                html.H4("Subcategories with Values Smaller than Predefined", className="card-title"),
                html.Ul([html.Li(subcategory) for subcategory in smaller_subcategories])
            ])
        else:
            text_output = html.Div("All values are equal or greater than the predefined values.")
        
        return text_output
    else:
        return ''

    
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)