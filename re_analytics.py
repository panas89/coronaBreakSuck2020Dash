# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import yaml
from components import vis as rvis

from assets.input_data import *

import plotly.express as px
import plotly.graph_objects as go

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


############################# reading all filenames for RE

import glob

filenames = glob.glob("data/relationship_extraction/*.csv")
meaningfull_filenames = [
    "Top 5-10\% High impact papers",
    "Semantic scholar COVID-19 papers",
    "COVID-19 Clinical Trials",
    "Top 5\% High impact papers",
]


############################# creating data structure from the yaml file (data dictionary)
data_path = "assets/Davids_interest_meshed.yaml"
with open(data_path) as f:
    data_yml = yaml.load(f, Loader=yaml.FullLoader)

# reorrganize the information
data_class_subclass = {}
classes = list(data_yml.keys())
classes.remove("disease_name")

for c in classes:
    data_class_subclass[c] = data_yml[c]["%s_common_name" % c]["kw"]

#############################

# =======================================================
# Plotly components
# =======================================================


def getPubScatter(df, x, y, hover_name):
    """Method to get publication scatter plot."""

    fig = px.scatter(df, x=x, y=y, hover_name=hover_name)
    fig.update_layout(
        title="Strength of discovered relationship along paper publication month",
        xaxis_title="Publish Time",
        yaxis_title="Probability",
        font=dict(
            family="Courier New, monospace",
            size=18,
        ),
    )

    return fig


kws = [
    data_class_subclass[list(data_class_subclass.keys())[1]][20],
    data_class_subclass[list(data_class_subclass.keys())[1]][2],
]
kw_interest = data_class_subclass[list(data_class_subclass.keys())[1]]


def getKW_RE_plot(df, kws):
    """Method to get line plot of kw relationship over time."""

    df_grps = rvis.preproces_for_kws_specific_plot(df, kws=kws)

    fig = go.Figure(
        data=go.Scatter(
            x=df_grps["publish_month"],
            y=df_grps["proba_mean"],
            error_y=dict(
                type="data",  # value of error bar given in data coordinates
                array=df_grps["proba_stderr"],
                visible=True,
            ),
        )
    )
    fig.update_layout(
        yaxis=dict(range=[0, 1]),
        title="coronavirus - keyword(s) relationship over time",
        xaxis_title="Month",
        yaxis_title="Strength",
        font=dict(
            family="Courier New, monospace",
            size=18,
        ),
    )
    return fig


def getMult_KW_scatter_plot(df, kw_interest):
    """Method to get multiple kwords scatter plot"""

    df_new_p = rvis.preprocess_for_multiple_kw_visualization(
        df, kw_interest=kw_interest
    )

    fig = px.scatter(
        df_new_p, x="publish_time", y="probability", color="keyword", size="probability"
    )
    fig.update_layout(
        yaxis=dict(range=[0, 1.1]),
        title="coronavirus - keyword relationship",
        xaxis_title="Publish Time",
        yaxis_title="Strength",
        font=dict(
            family="Courier New, monospace",
            size=18,
        ),
    )
    return fig


# ======================================================================================================================
# APP LAYOUT
# ======================================================================================================================
app.layout = html.Div(
    children=[
        html.H1(children="Relationship Extraction analytics"),
        html.Div(
            children="""
        Dash: A web application framework for Python.
    """
        ),
        dcc.Dropdown(
            options=[
                {"label": name, "value": filename}
                for name, filename in zip(meaningfull_filenames, filenames)
            ],
            value=filenames[0],
            multi=False,
            id="dd-files",
        ),
        dcc.Graph(
            id="re-prob-scat-plot",
            # figure=getPubScatter(df_new, x='publish_time',
            #                         y='probability', hover_name='keyword')
        ),
        dcc.Dropdown(
            options=[
                {"label": class_sub, "value": class_sub}
                for class_sub in list(data_class_subclass.keys())
            ],
            value=[list(data_class_subclass.keys())[0]],
            multi=True,
            id="dd-class_sub_class",
        ),
        dcc.Dropdown(
            options=[
                {"label": kw, "value": kw}
                for kw in data_class_subclass[list(data_class_subclass.keys())[0]]
            ],
            value=[data_class_subclass[list(data_class_subclass.keys())[0]][0]],
            multi=True,
            id="dd-kw",
        ),
        dcc.Graph(
            id="re-kws-plot",
            # figure=getKW_RE_plot(df_new, kws)
        ),
        dcc.Graph(
            id="re-mult-kws-plot",
            # figure=getMult_KW_scatter_plot(df_new,kw_interest)
        ),
    ]
)

# ======================================================================================================================
# CALLBACKS
# ======================================================================================================================
@app.callback(
    [
        Output("dd-kw", "options"),
        Output("dd-kw", "value"),
        Output("re-mult-kws-plot", "figure"),
        Output("re-prob-scat-plot", "figure"),
    ],
    [
        Input("dd-class_sub_class", "value"),
        Input("dd-files", "value"),
    ],
)
def update_output(class_sub_classes, filename):

    df = pd.read_csv(filename)

    df_new = rvis.preprocess_df(df)

    kws = []

    for class_sub in class_sub_classes:
        kws.extend(data_class_subclass[class_sub])

    kws_dict = [{"label": kw, "value": kw} for kw in kws]

    return (
        kws_dict,
        kws,
        getMult_KW_scatter_plot(df_new, kw_interest=kws),
        getPubScatter(df_new, x="publish_time", y="probability", hover_name="keyword"),
    )


@app.callback(
    Output("re-kws-plot", "figure"),
    [
        Input("dd-kw", "value"),
        Input("dd-files", "value"),
    ],
)
def update_output(kws, filename):

    df = pd.read_csv(filename)

    df_new = rvis.preprocess_df(df)

    return getKW_RE_plot(df_new, kws=kws)


if __name__ == "__main__":
    app.run_server(debug=True)