
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from assets.extraction import RelationExtractor
from assets.input_data import *

from app import app

# ######################################################################################################################
df = dataset2df[DATASET_NAMES[0]]

corpus_text = ''
for abstract in df.loc[:2,'abstract'].values:
    corpus_text += abstract

# initiate the extractor
# rextractor = RelationExtractor("assets/Davids_interest_meshed.yaml")

# ======================================================================================================================
# APP LAYOUT
# ======================================================================================================================
layout = html.Div(
    [
        dcc.Input(id="input-1", type="text", value='electroconvulsive', debounce=True),
        dcc.Input(id="input-2", type="text", value='COVID-19', debounce=True),
        html.Div(id="number-output"),
    ]
)

# ======================================================================================================================
# CALLBACKS
# ======================================================================================================================
@app.callback(
    Output("number-output", "children"),
    [Input("input-1", "value"), Input("input-2", "value")],
)
def update_output(input1, input2):
    relation = None #rextractor.extract(corpus_text, input1, input2)
    if relation == None:
        return u'{} and {} have no association'.format(input1, input2)
    else:
        return u'{} and {} {} association with coeff. {}'.format(input1, input2, relation[2][0], str(relation[2][1]))

