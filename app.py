import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as gobs
import pandas as pd
import numpy as np
import datetime


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

df['publish_time'] = pd.to_datetime(df['publish_time'])
time_diff = (df['publish_time'].max()-df['publish_time'].min()).days
print(df.head(3))
print(str(df['publish_time'].min())[:10])
print(str(df['publish_time'].min()+ datetime.timedelta(days=1)))
print((df['publish_time'].max()-df['publish_time'].min()).days)
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
                      'padding': '25px 50px 75px 100px',
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
                      'padding': '25px 50px 75px 100px',
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
            ], style={'width': '100%','padding': '25px 50px 75px 100px'})


# INTERACTION
# ===========

# Your interaction goes here.


# APP LAYOUT
# ==========

app.layout = html.Div([
                        header,
                        class_loc,
                        pb_time
])

if __name__ == '__main__':
    app.run_server(debug=True)