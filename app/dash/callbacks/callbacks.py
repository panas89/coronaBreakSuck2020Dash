# Misc
import ast
from datetime import datetime as dt

# Relative imports
from assets.input_data import *
from assets.styling import *
from components.core_components import *
from components.components_utils import *
from components import vis as rvis

# Plotly
import plotly.express as px
import plotly.graph_objects as go

# ======================================================================================================================
# TOPIC MODELING
# ======================================================================================================================
def createTopicModelingDf(
    file_path, cols_to_read=COLS_TO_READ, max_date=MAX_DATE
) -> pd.DataFrame:

    # Load data
    df = pd.read_csv(file_path, parse_dates=["publish_time"], usecols=cols_to_read)

    # Create DOI col
    # df['doi'] = ['https://doi.org/'+str(doi) for doi in df['doi'] if doi!=np.nan]

    # Create date col
    df["date"] = [date.strftime("%m-%d-%Y") for date in df["publish_time"]]

    # Fix unknown/wrong publication datetimes to today
    df.loc[df["publish_time"] > max_date, "publish_time"] = max_date

    return df


# ----------------------------------------------------------------------------------------------------------------------
def getTopicFig(class_subclass, topics_descr):

    return dict(
        data=[
            dict(
                x=[
                    dt.strptime(date, "%m-%d-%Y")
                    for date in topics_descr["topic_" + str(topic_num)]["times"]
                ],
                y=topics_descr["topic_" + str(topic_num)]["counts"],
                name=topics_descr["topic_" + str(topic_num)]["name"],
            )
            for topic_num in range(len(topics_descr))
        ],
        layout=dict(
            title="TOPIC TIME EVOLUTION"
            + f" ({format_class_subclass(class_subclass)})",
            showlegend=True,
            yaxis={"tickformat": ",d"},
            xaxis_tickformat="%d %B (%a)<br>%Y",
            legend=dict(x=0, y=1.0),
            margin=dict(l=40, r=0, t=40, b=30),
            colorway=TIME_COLORS,
        ),
    )


# ----------------------------------------------------------------------------------------------------------------------
def getTopicsHist(classes_topics_descr, class_subclass):

    return getTopicsBarChart(classes_topics_descr, class_subclass)


# ----------------------------------------------------------------------------------------------------------------------
def getPapers(class_subclass, topics, df):
    list_of_topics_ind = [int(topic[-1]) - 1 for topic in topics]

    # Format table entries
    df.publish_time = df.publish_time.dt.strftime("%Y-%m-%d")
    # df.affiliations_country = df.affiliations_country.apply(
    #     lambda x: ', '.join(x.split(',')) if x is not np.nan else x)
    df_papers = df.loc[
        df[class_subclass].isin(list_of_topics_ind), TABLE_COLS
    ].reset_index(drop=True)

    return [
        dash_table.DataTable(
            data=df_papers.to_dict("records"),
            columns=[
                {
                    "id": col,
                    "name": " ".join(col.split("_")).title(),
                    "clearable": True,
                    "renamable": True,
                    "hideable": True,
                    "deletable": True,
                }
                for col in TABLE_COLS
            ],
            tooltip_data=[
                {
                    column: {"value": str(value), "type": "markdown"}
                    for column, value in row.items()
                }
                for row in df_papers[TABLE_COLS].to_dict("rows")
            ],
            style_cell_conditional=[
                {"if": {"column_id": col}, "textAlign": "left"}
                for col in ["Date", "Region"]
            ],
            **STYLE_TABLE,
        )
    ]


# ----------------------------------------------------------------------------------------------------------------------
def getRelations(df_relation_f):
    """
    This function returns the Dash element (table) about the entity relations with coronavirus.

    :param df_relation_f (dataframe: stores the entity relationships with coronavirus.
    """
    # Clean up the relation columns
    rs = []
    for x in df_relation_f["relations"].tolist():
        if isinstance(x, str):
            rx = ast.literal_eval(x)

            # create content string
            ss = []
            for c in rx:
                s = "%s('%s', %.3f)" % (c[1], c[2][0], c[2][1])
                ss.append(s)
            rx = ", ".join(ss)
        else:
            rx = None
        rs.append(rx)
    df_relation_f["relations"] = rs

    # Create the Dash table object
    table = [
        dash_table.DataTable(
            data=df_relation_f.to_dict("records"),
            columns=[
                {
                    "id": col,
                    "name": " ".join(col.split("_")).title(),
                    "clearable": True,
                    "renamable": True,
                    "hideable": True,
                    "deletable": True,
                }
                for col in RELATION_TABLE_COLS
            ],
            tooltip_data=[
                {
                    column: {"value": str(value), "type": "markdown"}
                    for column, value in row.items()
                }
                for row in df_relation_f[RELATION_TABLE_COLS].to_dict("rows")
            ],
            **STYLE_TABLE,
        )
    ]

    return table


# ----------------------------------------------------------------------------------------------------------------------
def getDropDownTopics(classes_topics_descr, class_subclass):

    return [
        {
            "label": classes_topics_descr[class_subclass]["topic_" + str(topic_num)][
                "name"
            ],
            "value": classes_topics_descr[class_subclass]["topic_" + str(topic_num)][
                "name"
            ],
        }
        for topic_num in range(len(classes_topics_descr[class_subclass]))
    ]


# ----------------------------------------------------------------------------------------------------------------------
def getDropDownLocations(locations):

    return [
        dict(label=country, value=country)
        for country in locations
        if isinstance(country, str)
    ]


# ----------------------------------------------------------------------------------------------------------------------
def getTopicKwsTable_v2(df, class_subclass):
    topic2kws = getTopic2Kws(df, class_subclass)
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[f"Topic {topic_num}" for topic_num in topic2kws.keys()]
                ),
                cells=dict(values=[kws for kws in topic2kws.values()]),
            )
        ]
    )

    return fig


# ----------------------------------------------------------------------------------------------------------------------
def getTopicKwsTable(df, class_subclass):

    topic2kws = getTopic2Kws(df, class_subclass)
    topic2kws = dict(
        (f"Topic {topic_num}", kws) for topic_num, kws in topic2kws.items()
    )
    table = dash_table.DataTable(
        id="table_2",
        columns=[{"name": topic, "id": topic} for topic in topic2kws.keys()],
        data=pd.DataFrame.from_dict(topic2kws).to_dict("records"),
        style_data={"border": "0px"},
        style_table={
            "overflowX": "auto",
            # 'maxWidth': 0,
        },
        style_as_list_view=True,
        style_cell={
            "height": "auto",
            "font_family": TABLE_FONT_FAMILY,
            "font-size": TABLE_FONT_SIZE,
            "minWidth": "180px",
            "width": "180px",
            "maxWidth": "180px",
            "whiteSpace": "normal",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": TABLE_ROW_COLOR}
        ],
        style_header={
            "backgroundColor": TABLE_HEADER_BACKGROUND_COLOR,
            "color": TABLE_HEADER_COLOR,
        },
    )

    return table


# ----------------------------------------------------------------------------------------------------------------------
def createCovidIncidentsFig(dates, data, incident_name) -> dict:
    """Method to get covid incidents timeseries"""
    return dict(
        data=[
            dict(
                x=[dt.strptime(date, "%m-%d-%Y") for date in dates],
                y=data,
                name=incident_name,
                marker=dict(color="rgb(55, 83, 109)"),
            ),
        ],
        layout=dict(
            title=f"New Covid {incident_name}",
            showlegend=True,
            legend=dict(x=0, y=1.0),
            margin=dict(l=40, r=0, t=40, b=30),
        ),
    )


# ======================================================================================================================
# RELATION EXTRACTION
# ======================================================================================================================
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


# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
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