import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from .components_utils import *
from assets.input_data import *

# ######################################################################################################################
class_subclass_dd = html.Div([
                html.Label('Class - Subclass'),
                dcc.Dropdown(
                    id='class-subclass-drop-down',
                    options=[dict(label=format_class_subclass(c_s), value=c_s) for c_s in CLASSES_SUBCLASSES],
                    value='risk_factor_topic'
                )  
            ], style={'width': '48%',
                      'padding': '25px 50px 75px 50px',
                      'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
location_dd = html.Div([
                html.Label('Location'),
                dcc.Dropdown(
                    id='location-drop-down',
                    options=[dict(label=country, value=country) for country in LOCATIONS_COUNTRIES],
                    value='MTL'
                )  
            ], style={'width': '48%',
                      'padding': '25px 50px 75px 50px',
                      'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
topic_dd = html.Div([
                html.Label('Topic'),
                dcc.Dropdown(
                    id='topic-drop-down',
                    value=['Topic 1'],
                    multi=True
                )  
            ], style={'width': '48%',
                      'padding': '25px 50px 75px 50px',
                      'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
class_loc = html.Div([class_subclass_dd, location_dd], 
                     style={'width': '100%', 
                            'display': 'inline-block'}
                     )

# ----------------------------------------------------------------------------------------------------------------------
# pub_time = html.Div([
#                 html.Label('Publication date'),
#                 dcc.RangeSlider(
#                     id='pub-date-slider',
#                     min=0,
#                     max=max_week,
#                     value=[0,max_week],
#                     marks={week : dict(label = date.strftime("%m-%d-%Y"), style = {"transform": "rotate(45deg)"})\
#                            for week, date in enumerate(pd.date_range(start='01-01-2020', end=max_date, freq='W'), start=1)},
#                 ),
#             ], style={'width': '100%',
#                       'padding': '25px 50px 50px 50px',
#                       'display': 'inline-block'})

import datetime
pub_time = html.Div([
                html.Label('Publication date'),
                dcc.RangeSlider(
                    id='pub-date-slider',
                    min=0,
                    max=TIME_DIFF,
                    value=[0,TIME_DIFF],
                    marks={time_point : \
                            dict(label = str(df['publish_time'].min() + datetime.timedelta(days=time_point))[:10],
                                 style = {"transform": "rotate(45deg)"})\
                         for time_point in range(0,TIME_DIFF+11,11)},
                ),
            ], style={'width': '100%',
                      'padding': '25px 50px 50px 50px',
                      'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
time_radio_buttons = html.Div([
                                dcc.RadioItems(
                                                options=[
                                                    # {'label': 'Daily', 'value': 'D'},
                                                    {'label': 'Weekly', 'value': 'W'},
                                                    {'label': 'Monthly', 'value': 'M'}
                                                ],
                                                value='W',
                                                labelStyle={'padding': '25px 50px 50px 50px',
                                                            'display': 'inline-block'},
                                                style={'width': '100%',
                                                        'padding': '25px 50px 50px 50px',
                                                        'display': 'inline-block'},
                                                id='time-radio-buttons'
                                                 )  
                                ]
                                )

# ----------------------------------------------------------------------------------------------------------------------
topic_time_dist = html.Div([
                    dcc.Graph(
                            style={'height': 300},
                            id='topic-time-dist',
                        )  
                ], style={'width': '100%',
                    'padding': '25px 50px 50px 50px',
                    'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
topic_dist = html.Div([
                dcc.Graph(
                        style={'height': 300},
                        id='topic-dist'
                    )  
            ], style={'width': '50%',
                'padding': '25px 50px 50px 50px',
                'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
incident_cases = html.Div([
                    dcc.Graph(
                            style={'height': 300},
                            id='covid-cases'
                        )  
                ], style={'width': '33%',
                    'padding': '3px 5px 10px 10px',
                    'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
death_cases = html.Div([
                dcc.Graph(
                        style={'height': 300},
                        id='covid-deaths'
                    )  
            ], style={'width': '33%',
                'padding': '3px 5px 10px 10px',
                'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
recovery_cases = html.Div([
                    dcc.Graph(
                            style={'height': 300},
                            id='covid-recoveries'
                        )  
                ], style={'width': '33%',
                    'padding': '3px 5px 10px 10px',
                    'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
inc_death_rec_plots = html.Div(
                        [incident_cases,
                            death_cases,
                            recovery_cases],
                        style={'width': '100%',
                               'padding': '25px 50px 50px 50px',
                               'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
paper_table = html.Div(                    
                    id='table-papers',
                    style={'width': '100%',
                         'height': '1000px',
                                 'padding': '25px 50px 50px 50px',
                                 'text-align': 'center',
                                 'display': 'inline-block'})