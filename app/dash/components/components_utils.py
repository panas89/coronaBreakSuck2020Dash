import plotly.graph_objs as go
from assets.input_data import *
from collections import defaultdict
from assets.styling import *


# ######################################################################################################################
def format_class_subclass(x) -> str:
    return x.replace("_topic", "").replace("_", " ").capitalize()


# ----------------------------------------------------------------------------------------------------------------------


def getClassesSubclassesList(df) -> list:
    return [
        col
        for col in df.columns
        if "topic" in col and "kw" not in col and "common" not in col
    ]


# ----------------------------------------------------------------------------------------------------------------------
def resamplePubTimes(df, resample_type) -> (list, list):

    temp_df = df[["publish_time"]].groupby(df["publish_time"]).count()
    temp_df = temp_df.resample(resample_type).sum()

    dates = [date.strftime("%m-%d-%Y") for date in temp_df.index]
    counts = list(temp_df.values.reshape(1, -1)[0])

    return dates, counts


# ----------------------------------------------------------------------------------------------------------------------
def getClassesDescriptionMap(df, resample_type, CLASSES_SUBCLASSES) -> dict:
    """Cr"""
    classes_topics_descr = defaultdict(dict)
    for class_subclass in CLASSES_SUBCLASSES:
        for topic in df[class_subclass].unique():

            if topic == -1:
                continue

            select_rows = df[class_subclass] == topic
            dates, counts = resamplePubTimes(df[select_rows], resample_type)
            keywords = (
                df.loc[select_rows, class_subclass + "_kw"].unique()[0].split(", ")
            )

            classes_topics_descr[class_subclass]["topic_" + str(topic)] = {
                "name": "Topic " + str(topic + 1),
                "times": dates,
                "counts": counts,
                "keywords": keywords,
            }

    return classes_topics_descr


# ----------------------------------------------------------------------------------------------------------------------
def preprocCases(df, resample_type) -> (list, list):
    """Method that returns difference of cases every day and dates."""

    # Aggregate cases for each date
    non_date_cols = ["Province/State", "Country/Region", "Lat", "Long"]
    date_cols = [col for col in df.columns if col not in non_date_cols]
    dates = pd.to_datetime(date_cols)
    data = np.abs(pd.Series([0] + list(df[date_cols].sum(axis=0))).diff())[
        1:
    ]  # difference per day in cases , getting abs only positive values

    # Resample cases
    temp_df = pd.DataFrame(data=data.to_list(), index=dates.to_list())
    temp_df.fillna(0, inplace=True)
    temp_df = temp_df.resample(resample_type, label="right", closed="right").sum()

    dates = [date.strftime("%m-%d-%Y") for date in temp_df.index]
    data = list(temp_df.values.reshape(1, -1)[0])

    return (
        dates[:-2],
        data[:-2],
    )  ### omitting last 2 observations, as they are not as accurate in terms of numbers


# ----------------------------------------------------------------------------------------------------------------------
def getTopicsBarChart(classes_topics_descr, class_subclass):
    """Method to plot bar chart of topics"""
    x_axis_vals = [
        classes_topics_descr[class_subclass]["topic_" + str(num)]["name"]
        for num in sorted(
            [
                int(key.replace("topic_", ""))
                for key in classes_topics_descr[class_subclass].keys()
            ]
        )
    ]
    y_axis_vals = [
        np.sum(classes_topics_descr[class_subclass]["topic_" + str(num)]["counts"])
        for num in sorted(
            [
                int(key.replace("topic_", ""))
                for key in classes_topics_descr[class_subclass].keys()
            ]
        )
    ]

    fig = go.Figure(
        data=go.Bar(x=x_axis_vals, y=y_axis_vals, marker_color=BAR_COLORS[0]),
        layout=go.Layout(
            title=go.layout.Title(
                text="TOPIC DISTRIBUTION"
                + f" ({format_class_subclass(class_subclass)})"
            ),
            yaxis={"tickformat": ",d"},
            title_x=0.5,
            margin=dict(l=40, r=0, t=40, b=30),
        ),
    )

    return fig


# ----------------------------------------------------------------------------------------------------------------------
def getTopic2Kws(df, class_subclass):
    topic_col = f"{class_subclass}"
    topic_kw_col = f"{class_subclass}_kw"
    topic_kws_pairs = sorted(df.set_index([topic_col, topic_kw_col]).index.unique())

    return dict(
        (topic_num + 1, kws.split(", "))
        for topic_num, kws in topic_kws_pairs
        if topic_num != -1
    )
