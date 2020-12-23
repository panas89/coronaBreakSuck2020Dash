# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Relative imports
from app import app
from assets.input_data import *
from components import vis as rvis
from components.core_components import *
from callbacks.callbacks import getPubScatter, getKW_RE_plot, getMult_KW_scatter_plot

kws = [
    class_subclass2kws[list(class_subclass2kws.keys())[1]][20],
    class_subclass2kws[list(class_subclass2kws.keys())[1]][2],
]
kw_interest = class_subclass2kws[list(class_subclass2kws.keys())[1]]

# ======================================================================================================================
# APP LAYOUT
# ======================================================================================================================
layout = html.Div(
    children=[
        nre_dataset_dd, 
        nre_dataset_title,
        nre_prob_scat_plot,
        nre_class_subclass_dd,
        nre_kw_dd,
        nre_kws_plot,
        nre_mult_kws_plot
    ]
)

# ======================================================================================================================
# CALLBACKS
# ======================================================================================================================
@app.callback(
    Output('nre-dataset-title-v2', 'children'),
    [Input('nre-dataset-dd', 'value')])
def set_nre_dataset_title(dataset_name):
    
    if not dataset_name:
        return [None] 

    return [dataset_name.upper()]

# ----------------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output("nre_kw_dd", "options"),
     Output("nre_kw_dd", "value"),
     Output("nre-mult-kws-plot", "figure"),
     Output("nre-prob-scat-plot", "figure")],
    [Input("nre-class-subclass-dd", "value"),
     Input("nre-dataset-dd", "value")])
def update_output(class_sub_classes, filename):

    df = pd.read_csv(filename)

    df_new = rvis.preprocess_df(df)

    kws = []

    for class_sub in class_sub_classes:
        kws.extend(class_subclass2kws[class_sub])

    kws_dict = [{"label": kw, "value": kw} for kw in kws]

    return (
        kws_dict,
        kws,
        getMult_KW_scatter_plot(df_new, kw_interest=kws),
        getPubScatter(df_new, x="publish_time", y="probability", hover_name="keyword"),
    )

# ----------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output("nre-kws-plot", "figure"),
    [Input("nre_kw_dd", "value"),
     Input("nre-dataset-dd", "value")])
def update_output(kws, filename):

    df = pd.read_csv(filename)

    df_new = rvis.preprocess_df(df)

    return getKW_RE_plot(df_new, kws=kws)