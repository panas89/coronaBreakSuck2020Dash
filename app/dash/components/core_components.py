from datetime import datetime as dt

import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from .components_utils import *
from assets.styling import *
from assets.input_data import topic_dataset_name2path, nre_dataset_name2path

# ======================================================================================================================
# TOPIC MODELING
# ======================================================================================================================
dataset_dd = html.Div(
    [
        html.Label("Select Dataset (hover over name for description)"),
        dcc.Dropdown(
            id="dataset-drop-down",
            options=[
                dict(
                    label=name,
                    value=name,
                    title=topic_dataset_name2description[name],
                )
                for name in topic_dataset_name2path.keys()
            ],
            placeholder="Select Dataset",
            value=list(topic_dataset_name2path.keys())[0],
            persistence=True,
            persistence_type="local",
            clearable=False,
            multi=False,
        ),
    ],
    style={
        "width": "50%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

dataset_title = html.H1(
    id="dataset-title",
    style={
        "text-align": "center",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
    },
)
dataset = html.Div([dataset_dd, dataset_title])

# ----------------------------------------------------------------------------------------------------------------------
class_subclass_dd = html.Div(
    [
        html.Label("Medical Category"),
        dcc.Dropdown(
            id="class-subclass-drop-down",
            # options=[
            #     dict(label=format_class_subclass(c_s), value=c_s)
            #     for c_s in CLASSES_SUBCLASSES
            # ],
            value="risk_factor_topic",
            persistence=True,
            persistence_type="local",
            clearable=False,
        ),
    ],
    style={
        "width": "25%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

location_dd = html.Div(
    [
        html.Label("Location"),
        dcc.Dropdown(
            id="location-drop-down",
            # options=[
            #     dict(label=country, value=country)
            #     for country in LOCATIONS_COUNTRIES
            #     if isinstance(country, str)
            # ],
            value="Worldwide",
            persistence=True,
            persistence_type="local",
        ),
    ],
    style={
        "width": "25%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

pub_start_date = html.Div(
    [
        html.Div("Start Date"),
        dcc.DatePickerSingle(
            id="pub-start-date",
            min_date_allowed=dt(2019, 1, 1),
            max_date_allowed=MAX_DATE,
            initial_visible_month=dt(2020, 1, 1),
            date=str(dt(2020, 1, 1)),
            persistence=True,
            persistence_type="local",
        ),
    ],
    style={
        "width": "25%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

pub_end_date = html.Div(
    [
        html.Div("End Date"),
        dcc.DatePickerSingle(
            id="pub-end-date",
            min_date_allowed=dt(2020, 1, 1),
            max_date_allowed=MAX_DATE,
            initial_visible_month=MAX_DATE,
            date=str(MAX_DATE),
            persistence=True,
            persistence_type="local",
        ),
    ],
    style={
        "width": "25%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

class_loc_date = html.Div(
    [class_subclass_dd, location_dd, pub_start_date, pub_end_date],
    style={"width": "100%", "verticalAlign": "middle", "display": "inline-block"},
)

# ----------------------------------------------------------------------------------------------------------------------
topics_bar = html.Div(
    [dcc.Graph(style={"height": 300}, id="topics-bar")],
    style={
        "width": "100%",
        "padding": "25px 300px 25px 300px",
        "display": "inline-block",
    },
)

topics_bar = dcc.Loading(id="loading-topics-bar", children=[topics_bar], type="circle")
# -----------------------------------------`-----------------------------------------------------------------------------
topic_kws_table = html.Div(
    id="topic-kws-table",
    style={
        "width": "100%",
        "padding": "25px 50px 50px 25px",
        "text-align": "center",
        "display": "inline-block",
    },
)

topic_kws_table = dcc.Loading(
    id="loading-topic-kws-table", children=[topic_kws_table], type="circle"
)

# ----------------------------------------------------------------------------------------------------------------------
time_radio_buttons = html.Div(
    [
        html.Label("Sampling Frequency", style={"padding": "0px 50px 0px 50px"}),
        dcc.RadioItems(
            id="time-radio-buttons",
            options=[
                # {'label': 'Daily', 'value': 'D'},
                {"label": "Weekly", "value": "W"},
                {"label": "Monthly", "value": "M"},
            ],
            value="W",
            labelStyle={"padding": "10px 50px 0px 50px", "display": "inline-block"},
            persistence=True,
            persistence_type="local",
        ),
    ],
    style={"width": "100%", "padding": "25px 50px 0px 50px", "display": "inline-block"},
)

# ----------------------------------------------------------------------------------------------------------------------
topic_time_dist = html.Div(
    [
        dcc.Graph(
            # style={'height': 300},
            id="topic-time-dist",
        )
    ],
    style={
        "width": "100%",
        "height": "100%",
        "padding": "0px 50px 25px 50px",
        "display": "inline-block",
    },
)

topic_time_dist = dcc.Loading(
    id="loading-topic-time-dist", children=[topic_time_dist], type="circle"
)

# ----------------------------------------------------------------------------------------------------------------------
incident_cases = html.Div(
    [dcc.Graph(style={"height": 300}, id="covid-cases")],
    style={"width": "33%", "padding": "3px 5px 10px 10px", "display": "inline-block"},
)

death_cases = html.Div(
    [dcc.Graph(style={"height": 300}, id="covid-deaths")],
    style={"width": "33%", "padding": "3px 5px 10px 10px", "display": "inline-block"},
)

recovery_cases = html.Div(
    [dcc.Graph(style={"height": 300}, id="covid-recoveries")],
    style={"width": "33%", "padding": "3px 5px 10px 10px", "display": "inline-block"},
)

inc_death_rec_plots = html.Div(
    [incident_cases, death_cases, recovery_cases],
    style={
        "width": "100%",
        "padding": "25px 50px 50px 50px",
        "display": "inline-block",
    },
)

inc_death_rec_plots = dcc.Loading(
    id="loading-inc-death-rec-plots", children=[inc_death_rec_plots], type="circle"
)

# ----------------------------------------------------------------------------------------------------------------------
topic_table_heading = html.Div(
    [
        html.H1("PUBLICATIONS GROUPED BY TOPIC"),
        # html.P('This table shows the topics identified in each research publication. You can filter the table by selecting a specific topic.'),
    ],
    style={
        "width": "100%",
        #'height': '1000px',
        "padding": "5px 50px",
        "text-align": "center",
        "display": "inline-block",
        "font-size": TABLE_FONT_SIZE,
    },
)

# ----------------------------------------------------------------------------------------------------------------------
topic_dd = html.Div(
    [
        html.Label("Selected Topic(s)"),
        dcc.Dropdown(
            id="topic-drop-down",
            value=["Topic 1"],
            multi=True,
            persistence=True,
            persistence_type="local",
        ),
    ],
    style={"width": "25%", "padding": "5px 50px 25px 50px", "display": "inline-block"},
)

# ----------------------------------------------------------------------------------------------------------------------
paper_table = html.Div(
    id="table-papers",
    style={
        "width": "100%",
        #'height': '1000px',
        "padding": "25px 50px 100px 50px",
        "text-align": "center",
        "display": "inline-block",
    },
)

paper_table = dcc.Loading(
    id="loading-paper-table", children=[paper_table], type="circle"
)
# ----------------------------------------------------------------------------------------------------------------------
# relation_table_heading = html.Div([
#     html.H1('Entity Relationships'),
#     html.P('This table shows the relationships (the relationship type & strength between 0.0 and 1.0) of the coronvavirus and different entities obtained by the research papers. The entity relations are extrarcted using the Opennre package (http://opennre.thunlp.ai/#/sent_re).'),],
#     style={'width': '100%',
#            #'height': '1000px',
#            'padding': '5px 50px',
#            'text-align': 'center',
#            'display': 'inline-block',
#           'font-size': TABLE_FONT_SIZE},
# )

# # ----------------------------------------------------------------------------------------------------------------------
# relation_table = html.Div(
#     id='relation-table',
#     style={'width': '100%',
#            #'height': '1000px',
#            'padding': '5px 50px 100px 50px',
#            'text-align': 'center',
#            'display': 'inline-block'})

# ======================================================================================================================
# NRE
# ======================================================================================================================
nre_dataset_dd = html.Div(
    [
        html.Label("Select Dataset (hover over name for description)"),
        dcc.Dropdown(
            id="nre-dataset-dd",
            options=[
                dict(label=name, value=path, title=nre_dataset_name2description[name])
                for name, path in nre_dataset_name2path.items()
            ],
            placeholder="Select Dataset",
            value=list(nre_dataset_name2path.values())[0],
            persistence=True,
            persistence_type="local",
            clearable=False,
            multi=False,
        ),
    ],
    style={
        "width": "50%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

nre_dataset_title = html.H1(
    id="nre-dataset-title-v2",
    style={
        "text-align": "center",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
    },
)

nre_dataset = html.Div([nre_dataset_dd, nre_dataset_title])

# ----------------------------------------------------------------------------------------------------------------------
nre_class_subclass_dd = html.Div(
    [
        html.H4(children="Medical Category"),
        dcc.Dropdown(
            options=[
                {"label": class_sub, "value": class_sub}
                for class_sub in list(class_subclass2kws.keys())
            ],
            value=[list(class_subclass2kws.keys())[0]],
            multi=True,
            id="nre-class-subclass-dd",
        ),
    ],
    style={
        "width": "100%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

# ----------------------------------------------------------------------------------------------------------------------
nre_kw_dd = html.Div(
    [
        html.H4(children="Keywords"),
        dcc.Dropdown(
            options=[
                {"label": kw, "value": kw}
                for kw in class_subclass2kws[list(class_subclass2kws.keys())[0]]
            ],
            value=[class_subclass2kws[list(class_subclass2kws.keys())[0]][0]],
            multi=True,
            id="nre_kw_dd",
        ),
    ],
    style={
        "width": "100%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

# ----------------------------------------------------------------------------------------------------------------------
nre_prob_scat_plot = dcc.Graph(
    id="nre-prob-scat-plot",
    style={
        "width": "100%",
        "height": "100%",
        "padding": "0px 50px 25px 50px",
        "display": "inline-block",
    },
)

# ----------------------------------------------------------------------------------------------------------------------
nre_kws_plot = dcc.Graph(
    id="nre-kws-plot",
    style={
        "width": "100%",
        "height": "100%",
        "padding": "0px 50px 25px 50px",
        "display": "inline-block",
    },
)

# ----------------------------------------------------------------------------------------------------------------------
nre_mult_kws_plot = dcc.Graph(
    id="nre-mult-kws-plot",
    style={
        "width": "100%",
        "height": "100%",
        "padding": "0px 50px 25px 50px",
        "display": "inline-block",
    },
)

# ======================================================================================================================
# Rextractor
# ======================================================================================================================
rextractor_dataset_dd = html.Div(
    [
        html.Label("Select Dataset (hover over name for description)"),
        dcc.Dropdown(
            id="rextractor-dataset-dd",
            options=[
                dict(label=name, value=path, title="nre_dataset_name2description[name]")
                for name, path in topic_dataset_name2path.items()
            ],
            placeholder="Select Dataset",
            value=list(topic_dataset_name2path.values())[0],
            persistence=True,
            persistence_type="local",
            clearable=False,
            multi=False,
        ),
    ],
    style={
        "width": "50%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

rextractor_dataset_title = html.H1(
    id="rextractor-dataset-title-v2",
    style={
        "text-align": "center",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
    },
)

rextractor_dataset = html.Div([rextractor_dataset_dd, rextractor_dataset_title])


# ----------------------------------------------------------------------------------------------------------------------
rextractor_input1 = html.Div(
    [
        html.H4("First Keyword"),
        dcc.Input(id="input-1", type="text", value="fever", debounce=True),
    ],
    style={
        "width": "48%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

# ----------------------------------------------------------------------------------------------------------------------
rextractor_input2 = html.Div(
    [
        html.H4("Second Keyword"),
        dcc.Input(id="input-2", type="text", value="COVID-19", debounce=True),
    ],
    style={
        "width": "48%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

# ----------------------------------------------------------------------------------------------------------------------
rextractor_outputTitle = html.Div(
    [
        html.Div([html.H4("Output: ")]),
    ],
    style={
        "width": "48%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)

# ----------------------------------------------------------------------------------------------------------------------
rextractor_output = html.Div(
    id="number-output",
    style={
        "width": "100%",
        "verticalAlign": "middle",
        "padding": "25px 50px 25px 50px",
        "display": "inline-block",
    },
)