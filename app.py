import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as gobs
import dash_table
import pandas as pd
import numpy as np
import datetime
import pyLDAvis.gensim
import pickle


external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']


external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

# Server definition

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)

# HEADER
# ======

header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="coronaBreakSuck2020Dash",
    brand_href="#",
    color="primary",
    dark=True
)

# Data
# ==========

# read data.

df = pd.read_csv('./data/data.csv',parse_dates=True)

table_cols = ['title', 'abstract', 'publish_time', 
              'affiliations', 'location']

df['publish_time'] = pd.to_datetime(df['publish_time'])
time_diff = (df['publish_time'].max()-df['publish_time'].min()).days
print(df.head(3))
print(str(df['publish_time'].min())[:10])
print(str(df['publish_time'].min()+ datetime.timedelta(days=1)))
print((df['publish_time'].max()-df['publish_time'].min()).days)
print(df.columns)

# read visualization
with open('./data/vis.pickle', 'rb') as mod:
    vis = pickle.load(mod)

# COMPONENTS
# ==========

# Your components go here.

class_sub_class = html.Div([
                html.Label('Class - Subclass'),
                dcc.Dropdown(
                    id='class-sub-class-drop-down',
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montréal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value='MTL'
                )  
            ], style={'width': '48%',
                      'padding': '25px 50px 75px 50px',
                      'display': 'inline-block'})

location = html.Div([
                html.Label('Location'),
                dcc.Dropdown(
                    id='location-drop-down',
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montréal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value='MTL'
                )  
            ], style={'width': '48%',
                      'padding': '25px 50px 75px 50px',
                      'display': 'inline-block'})

class_loc = html.Div(
                    [class_sub_class,location]
                    , style={'width': '100%',
                             'display': 'inline-block'})


pb_time = html.Div([
                html.Label('Publication date'),
                dcc.RangeSlider(
                    id='pub-date-slider',
                    min=0,
                    max=time_diff,
                    value=[0,10],
                    marks={time_point : \
                            str(df['publish_time'].min() \
                        + datetime.timedelta(days=time_point))[:10] \
                         for time_point in range(0,time_diff+11,11)},
                ),
            ], style={'width': '100%',
                      'padding': '25px 50px 50px 50px',
                      'display': 'inline-block'})

proj_button = html.Div([
                    dbc.Button("Show projections", color="primary", block=True)
                        ], style={'width': '100%',
                      'padding': '25px 50px 50px 50px',
                      'display': 'inline-block'})

topic_dist = html.Div([
                dcc.Graph(
                        figure=dict(
                            data=[
                                dict(
                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                    350, 430, 474, 526, 488, 537, 500, 439],
                                    name='Topic 0',
                                    marker=dict(
                                        color='rgb(55, 83, 109)'
                                    )
                                ),
                                dict(
                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                    y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                                    299, 340, 403, 549, 499],
                                    name='Topic 1',
                                    marker=dict(
                                        color='rgb(26, 118, 255)'
                                    )
                                )
                            ],
                            layout=dict(
                                title='Topic distribution',
                                showlegend=True,
                                legend=dict(
                                    x=0,
                                    y=1.0
                                ),
                                margin=dict(l=40, r=0, t=40, b=30)
                            )
                        ),
                        style={'height': 300},
                        id='topic-dist'
                    )  
            ], style={'width': '100%',
                'padding': '25px 50px 50px 50px',
                'display': 'inline-block'})

incident_cases = html.Div([
                dcc.Graph(
                        figure=dict(
                            data=[
                                dict(
                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                    350, 430, 474, 526, 488, 537, 500, 439],
                                    name='Positive cases',
                                    marker=dict(
                                        color='rgb(55, 83, 109)'
                                    )
                                ),
                            ],
                            layout=dict(
                                title='New Covid cases',
                                showlegend=True,
                                legend=dict(
                                    x=0,
                                    y=1.0
                                ),
                                margin=dict(l=40, r=0, t=40, b=30)
                            )
                        ),
                        style={'height': 300},
                        id='covid-cases'
                    )  
            ], style={'width': '33%',
                'padding': '3px 5px 10px 10px',
                'display': 'inline-block'})

death_cases = html.Div([
                dcc.Graph(
                        figure=dict(
                            data=[
                                dict(
                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                    350, 430, 474, 526, 488, 537, 500, 439],
                                    name='Deaths',
                                    marker=dict(
                                        color='rgb(55, 83, 109)'
                                    )
                                ),
                            ],
                            layout=dict(
                                title='New Covid deaths',
                                showlegend=True,
                                legend=dict(
                                    x=0,
                                    y=1.0
                                ),
                                margin=dict(l=40, r=0, t=40, b=30)
                            )
                        ),
                        style={'height': 300},
                        id='covid-deaths'
                    )  
            ], style={'width': '33%',
                'padding': '3px 5px 10px 10px',
                'display': 'inline-block'})

recovery_cases = html.Div([
                dcc.Graph(
                        figure=dict(
                            data=[
                                dict(
                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                    350, 430, 474, 526, 488, 537, 500, 439],
                                    name='Recoveries',
                                    marker=dict(
                                        color='rgb(55, 83, 109)'
                                    )
                                ),
                            ],
                            layout=dict(
                                title='New Covid recoveries',
                                showlegend=True,
                                legend=dict(
                                    x=0,
                                    y=1.0
                                ),
                                margin=dict(l=40, r=0, t=40, b=30)
                            )
                        ),
                        style={'height': 300},
                        id='covid-recoveries'
                    )  
            ], style={'width': '33%',
                'padding': '3px 5px 10px 10px',
                'display': 'inline-block'})

inc_death_rec_plots = html.Div(
                                [incident_cases,
                                 death_cases,
                                 recovery_cases]
                        , style={'width': '100%',
                                 'padding': '25px 50px 50px 50px',
                                 'display': 'inline-block'})


topic_vis = html.Div([
                    html.Iframe(srcDoc=pyLDAvis.prepared_data_to_html(vis) 
                        ,style={'width': '100%',
                                'height': '100%',
                                'text-align': 'center',
                                'display': 'center'}
                        )
                    ]
                , style={'width': '100%',
                         'height': '1000px',
                                 'padding': '25px 50px 50px 50px',
                                 'text-align': 'center',
                                 'display': 'inline-block'})


paper_table = html.Div([
                    dash_table.DataTable(
                                        data=df[table_cols].to_dict('records'),
                                        columns=[{'id': c, 'name': c} for c in table_cols],
                                        page_size=10,

                                        style_cell={
                                                    'overflow': 'hidden',
                                                    'textOverflow': 'ellipsis',
                                                    'maxWidth': 0,
                                                },
                                                tooltip_data=[
                                                    {
                                                        column: {'value': str(value), 'type': 'markdown'}
                                                        for column, value in row.items()
                                                    } for row in df[table_cols].to_dict('rows')
                                                ],
                                        tooltip_duration=None,

                                        style_cell_conditional=[
                                            {
                                                'if': {'column_id': c},
                                                'textAlign': 'left'
                                            } for c in ['Date', 'Region']
                                        ],
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': 'rgb(248, 248, 248)'
                                            }
                                        ],
                                        style_header={
                                            'backgroundColor': 'rgb(230, 230, 230)',
                                            'fontWeight': 'bold'
                                        }
                                    )
                        ]
                , style={'width': '100%',
                         'height': '1000px',
                                 'padding': '25px 50px 50px 50px',
                                 'text-align': 'center',
                                 'display': 'inline-block'})

# INTERACTION
# ===========

# Your interaction goes here.


# APP LAYOUT
# ==========

app.layout = html.Div([
                        header,
                        class_loc,
                        pb_time,
                        proj_button,
                        topic_dist,
                        inc_death_rec_plots,
                        topic_vis,
                        paper_table
])

if __name__ == '__main__':
    app.run_server(debug=True)