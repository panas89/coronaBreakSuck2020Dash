from datetime import datetime as dt

import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


from .components_utils import *
from assets.input_data import *

# ######################################################################################################################
class_subclass_dd = html.Div([
    html.Label('Medical Category'),
    dcc.Dropdown(
        id='class-subclass-drop-down',
        options=[dict(label=format_class_subclass(c_s), value=c_s)
                 for c_s in CLASSES_SUBCLASSES],
        value='risk_factor_topic'
    )
], style={'width': '25%',
'verticalAlign': 'middle',
          'padding': '25px 50px 25px 50px',
          'display': 'inline-block'})

location_dd = html.Div([
    html.Label('Location'),
    dcc.Dropdown(
        id='location-drop-down',
        options=[dict(label=country, value=country)
                 for country in LOCATIONS_COUNTRIES],
        value='MTL'
    )
], style={'width': '25%',
'verticalAlign': 'middle',
          'padding': '25px 50px 25px 50px',
          'display': 'inline-block'})

pub_start_date = html.Div([
    html.Div('Start Date'),
    dcc.DatePickerSingle(
        id='pub-start-date',
        min_date_allowed=dt(2020, 1, 1),
        max_date_allowed=MAX_DATE,
        initial_visible_month=dt(2020, 1, 1),
        date=str(dt(2020, 1, 1))
    ),
],
    style={'width': '25%',
    'verticalAlign': 'middle',
           'padding': '25px 50px 25px 50px',
           'display': 'inline-block'})

pub_end_date = html.Div([
                        html.Div('End Date'),
                        dcc.DatePickerSingle(
                            id='pub-end-date',
                            min_date_allowed=dt(2020, 1, 1),
                            max_date_allowed=MAX_DATE,
                            initial_visible_month=MAX_DATE,
                            date=str(MAX_DATE)
                        ),
                        ],
                        style={'width': '25%',
                                'verticalAlign': 'middle',
                               'padding': '25px 50px 25px 50px',
                               'display': 'inline-block'})

class_loc_date = html.Div([class_subclass_dd,
                           location_dd,
                           pub_start_date,
                           pub_end_date],
                          style={'width': '100%',
                                 'verticalAlign': 'middle',
                                 'display': 'inline-block'}
                          )

# ----------------------------------------------------------------------------------------------------------------------
topics_bar = html.Div([
    dcc.Graph(
        style={'height': 300},
        id='topics-bar'
    )
], style={'width': '100%',
          'padding': '25px 300px 25px 300px',
          'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
topic_kws_table = html.Div(
    id='topic-kws-table',
    style={'width': '100%',
           'padding': '25px 50px 50px 25px',
           'text-align': 'center',
           'display': 'inline-block'})


# ----------------------------------------------------------------------------------------------------------------------
time_radio_buttons = html.Div([
    html.Label('Sampling Frequency', style={'padding': '0px 50px 0px 50px'}),
    dcc.RadioItems(
        id='time-radio-buttons',
        options=[
            # {'label': 'Daily', 'value': 'D'},
            {'label': 'Weekly',
             'value': 'W'},
            {'label': 'Monthly',
             'value': 'M'}
        ],
        value='W',
        labelStyle={'padding': '10px 50px 0px 50px',
                    'display': 'inline-block'},
    )
],
    style={'width': '100%',
          'padding': '25px 50px 0px 50px',
           'display': 'inline-block'},

)

# ----------------------------------------------------------------------------------------------------------------------
topic_time_dist = html.Div([
    dcc.Graph(
        # style={'height': 300},
        id='topic-time-dist',
    )
], style={'width': '100%',
          'height': '100%',
          'padding': '0px 50px 25px 50px',
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

death_cases = html.Div([
    dcc.Graph(
        style={'height': 300},
        id='covid-deaths'
    )
], style={'width': '33%',
          'padding': '3px 5px 10px 10px',
          'display': 'inline-block'})

recovery_cases = html.Div([
    dcc.Graph(
        style={'height': 300},
        id='covid-recoveries'
    )
], style={'width': '33%',
          'padding': '3px 5px 10px 10px',
          'display': 'inline-block'})

inc_death_rec_plots = html.Div(
    [incident_cases,
     death_cases,
     recovery_cases],
    style={'width': '100%',
           'padding': '25px 50px 50px 50px',
           'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
topic_table_heading = html.Div([
    html.H1('Topic Modeling'),
    html.P('This table shows the topics identified in each research publication. You can filter the table by selecting a specific topic.'),],
    style={'width': '100%',
           #'height': '1000px',
           'padding': '5px 50px',
           'text-align': 'center',
           'display': 'inline-block',
          'font-size': TABLE_FONT_SIZE}
)

# ----------------------------------------------------------------------------------------------------------------------
topic_dd = html.Div([
    html.Label('Selected Topic(s)'),
    dcc.Dropdown(
        id='topic-drop-down',
        value=['Topic 1'],
        multi=True
    )
], style={'width': '25%',
          'padding': '5px 50px 25px 50px',
          'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
paper_table = html.Div(
    id='table-papers',
    style={'width': '100%',
           #'height': '1000px',
           'padding': '25px 50px 100px 50px',
           'text-align': 'center',
           'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
relation_table_heading = html.Div([
    html.H1('Entity Relationships'),
    html.P('This table shows the relationships (the relationship type & strength between 0.0 and 1.0) of the coronvavirus and different entities obtained by the research papers. The entity relations are extrarcted using the Opennre package (http://opennre.thunlp.ai/#/sent_re).'),],
    style={'width': '100%',
           #'height': '1000px',
           'padding': '5px 50px',
           'text-align': 'center',
           'display': 'inline-block',
          'font-size': TABLE_FONT_SIZE},
)

# ----------------------------------------------------------------------------------------------------------------------
relation_table = html.Div(
    id='relation-table',
    style={'width': '100%',
           #'height': '1000px',
           'padding': '5px 50px 100px 50px',
           'text-align': 'center',
           'display': 'inline-block'})
