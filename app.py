import flask
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as gobs
from components.core_components import *
from components.components_utils import *
# import sys
# sys.path.append("..")
from assets.input_data import *
from callbacks.callbacks import *
from dash.dependencies import Input, Output
import dash_dangerously_set_inner_html
import plotly


external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']


external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

# Server definition

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)

# HEADER
# ======

header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="coronaBreakSuck2020Dash",
    brand_href="#",
    color="primary",
    dark=True
)

# Data
# ==========

# read data.



# COMPONENTS
# ==========

# Your components go here.


# INTERACTION
# ===========

# Your interaction goes here.

# APP LAYOUT
# ==========

app.layout = html.Div([
                        header,
                        class_loc,
                        pb_time,
                        class_grouped_topic,
                        proj_button,
                        time_radio_buttons,
                        topic_dist_vis,
                        # topic_word_clouds,
                        inc_death_rec_plots,
                        # topic_vis,
                        topic_dd,
                        paper_table
                        ])


# Callbacks
# =========


@app.callback(
    [Output('topic-dist', 'figure'),
     Output('topic-vis', 'srcDoc'),
     Output('classes-grouped-hist', 'children')],
    [Input('class-sub-class-drop-down', 'value'),
     Input('pub-date-slider', 'value'),
     Input('time-rb', 'value')])
def update_by_subclass(class_sub_class,times,time_resample_type):

    times = pd.to_datetime([str(df['publish_time'].min() \
                        + datetime.timedelta(days=time_point))[:10] \
                         for time_point in times])

    df_times = df.loc[df['publish_time'].between(times[0],times[1]),:].reset_index(drop=True)

    classes_topics_descr = getClassesDescriptionMap(df_times,time_resample_type)

    topics_descr = classes_topics_descr[class_sub_class]

    fig_dist = getTopicFig(class_sub_class,topics_descr)

    vis_obj = getVis(class_sub_class)

    grouped_hist = getGroupedHist(classes_topics_descr,classes_sub_classes)

    return fig_dist,vis_obj,grouped_hist


@app.callback(
    [Output('table-papers', 'children'),
     Output('topic-drop-down', 'options')],
    [Input('class-sub-class-drop-down', 'value'),
     Input('topic-drop-down', 'value'),
     Input('pub-date-slider', 'value'),
     Input('time-rb', 'value')])
def update_by_topic(class_sub_class,topic,times,time_resample_type):

    times = pd.to_datetime([str(df['publish_time'].min() \
                        + datetime.timedelta(days=time_point))[:10] \
                         for time_point in times])

    df_times = df.loc[df['publish_time'].between(times[0],times[1]),:].reset_index(drop=True)

    classes_topics_descr = getClassesDescriptionMap(df_times,time_resample_type)

    children = getPapers(class_sub_class,topic,df_times)

    options = getDropDownTopics(classes_topics_descr,class_sub_class)

    return children,options


@app.callback(
    [Output('covid-cases', 'figure'),
     Output('covid-deaths', 'figure'),
     Output('covid-recoveries', 'figure')],
    [Input('time-rb', 'value')])
def update_by_deaths_inc_rec(time_resample_type):

    dates_inc , inc_data = preprocCases(df=df_inc,resample_type=time_resample_type)
    dates_death , death_data = preprocCases(df=df_death,resample_type=time_resample_type)
    dates_rec , rec_data = preprocCases(df=df_rec,resample_type=time_resample_type)
    

    rec_fig = getRecoveriesFig(dates_rec,rec_data)
    inc_fig = getIncFig(dates_inc,inc_data)
    death_fig = getDeathFig(dates_death,death_data)

    return rec_fig,inc_fig,death_fig


if __name__ == '__main__':
    app.run_server(debug=True)