import flask
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from components.core_components import *
from components.components_utils import *
from assets.input_data import *
from callbacks.callbacks import *

# ######################################################################################################################
# SERVER DEFINITION
# ======================================================================================================================
external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']
external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

server = flask.Flask(__name__)

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)

# ======================================================================================================================
# HEADER
# ======================================================================================================================
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

# ======================================================================================================================
# APP LAYOUT
# ======================================================================================================================

app.layout = html.Div([
                        header,
                        class_loc,  # 'class-subclass-drop-down', 'location-drop-down' 
                        pub_time,  # 'pub-date-slider'
                        topic_dist,  # 'topic-dist'
                        time_radio_buttons,  # 'time-radio-buttons'
                        topic_time_dist,  # 'topic-time-dist'
                        inc_death_rec_plots,  # 'covid-cases', 'covid-deaths', 'covid-recoveries'
                        topic_dd,  # 'topic-drop-down'
                        paper_table  # 'table-papers'
                        ])

# ======================================================================================================================
# CALLBACKS
# ======================================================================================================================
@app.callback(
    [Output('topic-time-dist', 'figure'),
     Output('topic-dist', 'figure')],
    [Input('class-subclass-drop-down', 'value'),
     Input('pub-date-slider', 'value'),
     Input('time-radio-buttons', 'value')])
def update_by_subclass(class_subclass, dates, date_resample_type):

    dates = pd.to_datetime([str(df['publish_time'].min() + datetime.timedelta(days=date))[:10]
                            for date in dates])

    df_dates = df.loc[df['publish_time'].between(dates[0], dates[1]),:].reset_index(drop=True)

    classes_topics_descr = getClassesDescriptionMap(df_dates, date_resample_type)

    topics_descr = classes_topics_descr[class_subclass]

    fig_topic_time_dist = getTopicFig(class_subclass, topics_descr)

    topics_dist = getTopicsHist(classes_topics_descr, class_subclass)

    return fig_topic_time_dist, topics_dist 

# ----------------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output('table-papers', 'children'),
     Output('topic-drop-down', 'options')],
    [Input('class-subclass-drop-down', 'value'),
     Input('topic-drop-down', 'value'),
     Input('pub-date-slider', 'value'),
     Input('time-radio-buttons', 'value')])
def update_by_topic(class_subclass,topics, dates, date_resample_type):

    dates = pd.to_datetime([str(df['publish_time'].min() + datetime.timedelta(days=date))[:10] 
                            for date in dates])

    df_dates = df.loc[df['publish_time'].between(dates[0], dates[1]),:].reset_index(drop=True)

    classes_topics_descr = getClassesDescriptionMap(df_dates, date_resample_type)

    children = getPapers(class_subclass, topics, df_dates)

    options = getDropDownTopics(classes_topics_descr,class_subclass)

    values = [i['value'] for i in options]

    return children, options

# ----------------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output('covid-cases', 'figure'),
     Output('covid-deaths', 'figure'),
     Output('covid-recoveries', 'figure')],
    [Input('time-radio-buttons', 'value')])
def update_by_deaths_inc_rec(date_resample_type):

    dates_inc , inc_data = preprocCases(df=df_inc, resample_type=date_resample_type)
    dates_death , death_data = preprocCases(df=df_death, resample_type=date_resample_type)
    dates_rec , rec_data = preprocCases(df=df_rec, resample_type=date_resample_type)
    
    rec_fig = getRecoveriesFig(dates_rec, rec_data)
    inc_fig = getIncFig(dates_inc, inc_data)
    death_fig = getDeathFig(dates_death, death_data)

    return rec_fig,inc_fig,death_fig


# ######################################################################################################################
if __name__ == '__main__':
    app.run_server(debug=True)#, host='0.0.0.0')