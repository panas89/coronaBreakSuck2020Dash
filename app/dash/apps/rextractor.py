# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from components.core_components import *

from assets.extraction import RelationExtractor
from assets.input_data import *

from app import app

# ######################################################################################################################
# df = dataset2df[DATASET_NAMES[0]]

# corpus_text = ""
# for abstract in df.loc[:, "abstract"].values:
#     corpus_text += abstract

# initiate the extractor
rextractor = RelationExtractor("app/dash/assets/Davids_interest_meshed.yaml")

# ======================================================================================================================
# APP LAYOUT
# ======================================================================================================================
layout = html.Div(
    [
        rextractor_dataset,
        rextractor_input1,
        rextractor_input2,
        rextractor_outputTitle,
        rextractor_output,
    ]
)

# ======================================================================================================================
# CALLBACKS
# ======================================================================================================================
@app.callback(
    Output("rextractor-dataset-title-v2", "children"),
    [
        Input("rextractor-dataset-dd", "options"),
        Input("rextractor-dataset-dd", "value"),
    ],
)
def set_rextractor_dataset_title(options, value_chosen):

    dataset_title = [x["label"] for x in options if x["value"] == value_chosen][0]

    return [dataset_title.upper()]


@app.callback(
    Output("number-output", "children"),
    [
        Input("input-1", "value"),
        Input("input-2", "value"),
        Input("rextractor-dataset-dd", "value"),
    ],
)
def update_output(input1, input2, input3):
    df = pd.read_csv(input3, usecols=["abstract"])
    corpus_text = df["abstract"].str.cat()

    relation = rextractor.extract(corpus_text, input1, input2)
    if relation == None:
        return u"{} and {} have no association".format(input1, input2)
    else:
        return u"{} and {} {} association with coeff. {}".format(
            input1, input2, relation[2][0], str(np.round(relation[2][1], 6))
        )
