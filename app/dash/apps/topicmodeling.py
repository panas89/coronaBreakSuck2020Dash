from dash.dependencies import Input, Output, State
from components.core_components import *
from components.components_utils import *
from assets.input_data import *
from assets.styling import *
from callbacks.callbacks import *

import dash_bootstrap_components as dbc
import flask
import dash
from app import app


# ======================================================================================================================
# HEADER
# ======================================================================================================================
# header = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True),
#                 dbc.DropdownMenuItem("Page 2", href="#"),
#                 dbc.DropdownMenuItem("Page 3", href="#"),
#             ],
#             nav=True,
#             in_navbar=True,
#             label="More",
#         ),
#     ],
#     brand="Trending Topics in Covid-19 Publications",
#     brand_href="#",
#     color='#5EAAF5',#"primary",
#     dark=True
# )

# ======================================================================================================================
# APP LAYOUT
# ======================================================================================================================

layout = html.Div(
    [
        # header,
        dataset,
        class_loc_date,  # 'class-subclass-drop-down', 'location-drop-down', 'pub-start/end-date'
        topics_bar,  # 'topics-bar'
        topic_kws_table,  # 'topic_kws_table'
        time_radio_buttons,  # 'time-radio-buttons'
        topic_time_dist,  # 'topic-time-dist'
        inc_death_rec_plots,  # 'covid-cases', 'covid-deaths', 'covid-recoveries'
        topic_table_heading,
        topic_dd,  # 'topic-drop-down'
        paper_table,  # 'table-papers'
    ]
)

# ======================================================================================================================
# CALLBACKS
# ======================================================================================================================
# ----------------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output("dataset-title", "children")],
    [
        Input("dataset-drop-down", "value"),
    ],
)
def set_dataset_title(value_chosen):

    dataset_title = value_chosen

    return [dataset_title.upper()]


# ----------------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output("class-subclass-drop-down", "options")],
    [
        Input("dataset-drop-down", "value"),
    ],
)
def set_dataset_title(dataset_name):

    df = dataset2df[dataset_name]

    classes_subclasses = getClassesSubclassesList(df)

    options_classes_subclasses = getDropDownClassesSubclasses(classes_subclasses)

    return options_classes_subclasses


# ----------------------------------------------------------------------------------------------------------------------
@app.callback(
    [
        Output("location-drop-down", "options"),
    ],
    [
        Input("dataset-drop-down", "value"),
        Input("pub-start-date", "date"),
        Input("pub-end-date", "date"),
    ],
)
def set_dataset_title(dataset_name, start_date, end_date):

    df = dataset2df[dataset_name]

    df_dates = df.loc[df["publish_time"].between(start_date, end_date), :].reset_index(
        drop=True
    )

    locations = ["Worldwide"] + df_dates["location"].unique().tolist()

    options_location = getDropDownLocations(locations)

    return [
        options_location,
    ]


# ----------------------------------------------------------------------------------------------------------------------
@app.callback(
    [
        Output("topic-time-dist", "figure"),
        Output("topics-bar", "figure"),
        Output("topic-kws-table", "children"),
    ],
    [
        Input("dataset-drop-down", "value"),
        Input("class-subclass-drop-down", "value"),
        Input("pub-start-date", "date"),
        Input("pub-end-date", "date"),
        Input("time-radio-buttons", "value"),
        Input("location-drop-down", "value"),
    ],
)
def update_by_subclass(
    dataset_name, class_subclass, start_date, end_date, date_resample_type, location
):

    df = dataset2df[dataset_name]

    # filter by location
    if location != "Worldwide":
        df = df.loc[df["location"] == location, :].reset_index(drop=True)

    # filter by date period
    df_dates = df.loc[df["publish_time"].between(start_date, end_date), :].reset_index(
        drop=True
    )

    classes_subclasses = getClassesSubclassesList(df_dates)

    classes_topics_descr = getClassesDescriptionMap(
        df_dates, date_resample_type, classes_subclasses
    )

    topics_descr = classes_topics_descr[class_subclass]

    fig_topic_time_dist = getTopicFig(class_subclass, topics_descr)

    topics_bar = getTopicsHist(classes_topics_descr, class_subclass)

    topic_kws_table = getTopicKwsTable(df, class_subclass)

    return fig_topic_time_dist, topics_bar, topic_kws_table


# ----------------------------------------------------------------------------------------------------------------------
@app.callback(
    [
        Output("covid-cases", "figure"),
        Output("covid-deaths", "figure"),
        Output("covid-recoveries", "figure"),
    ],
    [
        Input("time-radio-buttons", "value"),
        Input("location-drop-down", "value"),
    ],
)
def update_by_deaths_inc_rec(date_resample_type, location):

    # filter by location
    if location != "Worldwide":
        df_inc_loc = df_inc.loc[
            df_inc["Country/Region"] == location.replace("United States", "US"), :
        ].reset_index(drop=True)
        df_death_loc = df_death.loc[
            df_death["Country/Region"] == location.replace("United States", "US"), :
        ].reset_index(drop=True)
        df_rec_loc = df_rec.loc[
            df_rec["Country/Region"] == location.replace("United States", "US"), :
        ].reset_index(drop=True)
    else:
        df_inc_loc = df_inc
        df_death_loc = df_death
        df_rec_loc = df_rec

    # date_resample_type = 'mva'
    dates_inc, inc_data = preprocCases(df=df_inc_loc, resample_type=date_resample_type)
    dates_death, death_data = preprocCases(
        df=df_death_loc, resample_type=date_resample_type
    )
    dates_rec, rec_data = preprocCases(df=df_rec_loc, resample_type=date_resample_type)

    rec_fig = createCovidIncidentsFig(dates_rec, rec_data, "Recoveries")
    inc_fig = createCovidIncidentsFig(dates_inc, inc_data, "Cases")
    death_fig = createCovidIncidentsFig(dates_death, death_data, "Deaths")

    return rec_fig, inc_fig, death_fig


# -----------------------------------------------Callback for the topic table-------------------------------------------
@app.callback(
    [
        Output("table-papers", "children"),
        Output("topic-drop-down", "options"),
    ],
    [
        Input("dataset-drop-down", "value"),
        Input("class-subclass-drop-down", "value"),
        Input("topic-drop-down", "value"),
        Input("pub-start-date", "date"),
        Input("pub-end-date", "date"),
        Input("time-radio-buttons", "value"),
        Input("location-drop-down", "value"),
    ],
)
def update_by_topic(
    dataset_name,
    class_subclass,
    topics,
    start_date,
    end_date,
    date_resample_type,
    location,
):

    df = dataset2df[dataset_name]

    # filter by location
    if location != "Worldwide":
        df = df.loc[df["location"] == location, :].reset_index(drop=True)

    df_dates = df.loc[df["publish_time"].between(start_date, end_date), :].reset_index(
        drop=True
    )

    classes_subclasses = getClassesSubclassesList(df_dates)

    classes_topics_descr = getClassesDescriptionMap(
        df_dates, date_resample_type, classes_subclasses
    )

    children = getPapers(class_subclass, topics, df_dates)

    options_topics = getDropDownTopics(classes_topics_descr, class_subclass)

    values = [i["value"] for i in options_topics]

    return (
        children,
        options_topics,
    )


# -----------------------------------------------Callback for the topic table-------------------------------------------
# @app.callback(
#     [Output('relation-table', 'children'),],
#     [Input('pub-start-date', 'date'),
#      Input('pub-end-date', 'date'),])
# def update_by_relation(start_date, end_date):
#     """
#     This callback function handles the rendering logic of the corronavirus and entity relationships.
#     """
#     # get the df particular for certain dates
#     df_dates = df_relations.loc[df['publish_time'].between(start_date, end_date),:].reset_index(drop=True)

#     # Get the Dash data table
#     df_relation_f = df_dates.loc[:, RELATION_TABLE_COLS]

#     # assign
#     children = getRelations(df_relation_f)

#     return children

# ######################################################################################################################
# if __name__ == '__main__':
#     app.run_server(debug=True)#, host='0.0.0.0')