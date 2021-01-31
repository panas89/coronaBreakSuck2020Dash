# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import yaml
from components import vis as rvis
import pandas as pd
import numpy as np

# from assets.input_data import *

import plotly.express as px
import plotly.graph_objects as go

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


############################# reading all filenames for RE

import glob

filenames = glob.glob("app/dash/data/relationship_extraction/*.csv")
meaningfull_filenames = [
    "Top 5-10\% High impact papers",
    "Semantic scholar COVID-19 papers",
    "COVID-19 Clinical Trials",
    "Top 5\% High impact papers",
]


############################# creating data structure from the yaml file (data dictionary)
data_path = "app/dash/assets/Davids_interest_meshed.yaml"
with open(data_path) as f:
    data_yml = yaml.load(f, Loader=yaml.FullLoader)

# reorrganize the information
data_class_subclass = {}
classes = list(data_yml.keys())
classes.remove("disease_name")

for c in classes:
    data_class_subclass[c] = data_yml[c]["%s_common_name" % c]["kw"]

print(classes)

#############################

# =======================================================
# Plotly components
# =======================================================


def getPubScatter(df, x, y, hover_name):
    """Method to get publication scatter plot."""

    fig = px.scatter(
        df, x=x, y=y, hover_name=hover_name, color=y, color_discrete_map="Viridis"
    )
    fig.update_layout(
        title="Keyword to COVID-19 association",
        xaxis_title="",
        yaxis_title="Strength of association",
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
        yaxis=dict(range=[0, 1.1]),
        title="Medical category to COVID-19 association",
        xaxis_title="",
        yaxis_title="Strength of association",
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
        title="(Medical category,keyword) to COVID-19 association",
        xaxis_title="",
        yaxis_title="Strength of association",
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
        html.H1(children="Relationship Extraction Analysis"),
        html.Div(
            children="""
        In additional to topic modeling, we are also interested to investigate how certain keywords (e.g., kidney) are related to Coronavirus disease (Covid-19) based on the scientific discoveries from the literature. Relation extraction is a natural language processing (NLP) task that is to extract relations (e.g., “founder of”) between two entities. For example, pneumonia is highly related to Covid-19 because it is one of the infections that is caused by Covid-19. 

In here, we utilized a relationship extraction package, OpenNRE [1], to identify the strength of relationship (i.e., “is related to”) between a keyword and Covid-19. The OpenNRE consisted of classification models that were trained with open-source annotated relationship datas using deep learning techniques. The strength of the relationship has a scale of 0 (no relation) to 1 (completely related). See Below for several “strength” plots that show the relationship of a keyword with Covid-19 along time.


Reference:
1. https://github.com/thunlp/OpenNRE
    """
        ),
        html.H4(children="Select Dataset"),
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
        html.H4(children="Medical Category"),
        dcc.Dropdown(
            options=[
                {"label": class_sub, "value": class_sub}
                for class_sub in list(data_class_subclass.keys())
            ],
            value=[list(data_class_subclass.keys())[0]],
            multi=True,
            id="dd-class_sub_class",
        ),
        html.H4(children="Keywords"),
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

    df_new = pd.read_csv(filename, date_parser=True)
    df_new["publish_time"] = pd.to_datetime(df_new["publish_time"])

    # df_new = rvis.preprocess_df(df)

    kws = []

    for class_sub in class_sub_classes:
        kws.extend(
            [
                kw
                for kw in data_class_subclass[class_sub]
                if kw in df_new["keyword"].tolist()
            ]
        )

    kws = list(np.unique(kws))

    kws_dict = [{"label": kw, "value": kw} for kw in kws]

    return (
        kws_dict,
        kws,
        getMult_KW_scatter_plot(df_new, kw_interest=kws),
        getPubScatter(
            df_new.dropna(subset=["keyword"]),
            x="publish_time",
            y="probability",
            hover_name="keyword",
        ),
    )


@app.callback(
    Output("re-kws-plot", "figure"),
    [
        Input("dd-kw", "value"),
        Input("dd-files", "value"),
    ],
)
def update_output(kws, filename):

    df_new = pd.read_csv(filename, date_parser=True)
    df_new["publish_time"] = pd.to_datetime(df_new["publish_time"])

    # df_new = rvis.preprocess_df(df)

    return getKW_RE_plot(df_new, kws=kws)


if __name__ == "__main__":
    app.run_server(debug=True)