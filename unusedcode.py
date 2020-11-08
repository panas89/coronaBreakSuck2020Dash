# ######################################################################################################################
# Components Utils
# ######################################################################################################################
import plotly.graph_objs as go
from assets.input_data import *
import random
import plotly as pltly
import sys
sys.path.append("..")

# ----------------------------------------------------------------------------------------------------------------------
def getClassBarChart(classes_topics_descr,classes_sub_classes):
    """Method to plot histogram of papers for each class, class name in x-axis."""
    x_axis_vals = [class_subclass.replace('_topic','').replace('_',' ').capitalize() for class_subclass in classes_sub_classes]
    y_axis_vals = []

    for class_subclass in classes_sub_classes:
        values = []
        for topic_num in range(len(classes_topics_descr[class_subclass])):
            values.append(np.sum(classes_topics_descr[class_subclass]['topic_'+str(topic_num)]['counts']))
        y_axis_vals.append(np.sum(values))                  

    fig = go.Figure(data=go.Bar(
                                x=x_axis_vals,
                                y=y_axis_vals,
                                marker_color =  colors
                            ),
                    layout=go.Layout(
                                    title=go.layout.Title(text= "Class distribution"),
                                    yaxis={'tickformat': ',d'},
                                    title_x=0.5,
                                    margin=dict(l=40, r=0, t=40, b=30),
                                    )
                    )

    return fig

# ----------------------------------------------------------------------------------------------------------------------
def getStackedBarChart(classes_topics_descr, classes_sub_classes, num_of_topics=20):
    """Method to plot grouped bar charts, have to loop first by topic then by class to have class name in x-axis."""

    format_class_subclass = lambda x: x.replace('_topic','').replace('_',' ').capitalize()
    x_axis_vals = [format_class_subclass(c_s) for c_s in classes_subclasses]
    y_axis_vals = []
    names = []

    for topic_num in range(num_of_topics):
        values = []
        name_values = []
        for class_subclass in classes_sub_classes:
            try:
                values.append(np.sum(classes_topics_descr[class_subclass]['topic_'+str(topic_num)]['counts']))
                name_values.append(classes_topics_descr[class_subclass]['topic_'+str(topic_num)]['name'])
            except:
                values.append(0)
        y_axis_vals.append(values)
        names.extend(list(np.unique(name_values)))


    bars = []
    for y_ax,name in zip(y_axis_vals,names):
        bars.append(
                    go.Bar(name=name,
                            x=x_axis_vals,
                            y=y_ax
                            )
                    )
                            

    fig = go.Figure(data=bars)

    return fig

# ----------------------------------------------------------------------------------------------------------------------
def wordCloudFigure(topic_descr):

    """Method to create a wordcloud."""

    words = topic_descr['keywords']
    length = len(words)
    colors = [pltly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(length)]
    frequency = [20]*len(words)
    percent = [1/len(words)]*len(words)

    data = go.Scatter(
                        x=random.sample(range(length), k=length),
                        y=random.sample(range(length), k=length),
                        mode='text',
                        text=words,
                        hovertext=['{0} - {1} - {2}'.format(w, f, format(p, '.2%')) for w, f, p in zip(words, frequency, percent)],
                        hoverinfo='text',
                        textfont={'size': frequency, 'color': colors}
                    )
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'title': topic_descr['name'],
                        'width': 20})

    fig = go.Figure(data=[data], layout=layout)
    return fig

# ######################################################################################################################
# Core Components
# ######################################################################################################################
import datetime
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

# ----------------------------------------------------------------------------------------------------------------------
topic_word_clouds = html.Div(
                            # [
                            # # dcc.Graph(figure=wordCloudFigure(topics_descr['topic_'+str(topic_num)]),
                            # #             style={'width': str(1.98*100/len(topics_descr))+'%',
                            # #                    'padding': '0px 0px 0px 0px',
                            # #                    'display': 'inline-block'})
                            # #         for topic_num in range(len(topics_descr))
                            # ]
                     id='topic-wcloud'
                     , style={'width': '70%',
                                'height': '100%',
                                'display': 'inline-block'}
                   )

# ----------------------------------------------------------------------------------------------------------------------
fig_wcloud = [dcc.Graph(figure=wordCloudFigure(topics_descr['topic_'+str(topic_num)]),
                                        style={'width': '30%',
                                               'padding': '0px 0px 0px 0px',
                                               'display': 'inline-block'})
                                    for topic_num in range(len(topics_descr))]

# ----------------------------------------------------------------------------------------------------------------------
proj_button = html.Div([dbc.Button("Show projections", color="primary", block=True)], 
                       style={'width': '100%',
                              'padding': '25px 50px 50px 50px',
                              'display': 'inline-block'}
                    )

# ----------------------------------------------------------------------------------------------------------------------
topic_vis = html.Div( html.Iframe(
                         id='topic-vis',
                         style={'width': '50%',
                         'text-align': 'center',
                         'height': '900px',
                         'stylesheet' : 'https://codepen.io/chriddyp/pen/bWLwgP.css'},
                         
                        )
                , style={'width': '110%',
                         'height': '100%',
                                 'text-align': 'center',
                                 'display': 'inline-block'})

# ----------------------------------------------------------------------------------------------------------------------
class_grouped_topic = html.Div(
                                id='classes-grouped-hist'
                                , style={'width': '50%',
                                        'padding': '25px 50px 50px 50px',
                                        'display': 'inline-block'}
                                )
# ----------------------------------------------------------------------------------------------------------------------
# TIME_DIFF = (df['publish_time'].max()-df['publish_time'].min()).days
pub_time = html.Div([
                    html.Label('Publication date'),
                    dcc.RangeSlider(
                        id='pub-date-slider',
                        min=0,
                        max=TIME_DIFF,
                        value=[0, TIME_DIFF],
                        marks={time_point:
                            dict(label=str(df['publish_time'].min() + datetime.timedelta(days=time_point))[:10],
                                    style={"transform": "rotate(45deg)"})
                            for time_point in range(0, TIME_DIFF+11, 11)},
                    ),
                ], style={'width': '100%',
                        'padding': '25px 50px 50px 50px',
                        'display': 'inline-block'})

# ######################################################################################################################
# Callbacks
# ######################################################################################################################
import pickle
import pyLDAvis

TOPIC_MODELLING_DIR = './data/topicmodels/
# ----------------------------------------------------------------------------------------------------------------------
def getVis(class_subclass):
    # read visualization
    with open(TOPIC_MODELLING_DIR + class_subclass.replace('_topic','') + '/vis.pickle', 'rb') as mod:
        vis = pickle.load(mod)

    return pyLDAvis.prepared_data_to_html(vis)

# ----------------------------------------------------------------------------------------------------------------------
def getGroupedHist(classes_topics_descr, classes_sub_classes):

    return [
            dcc.Graph(figure=getStackedBarChart(classes_topics_descr,classes_sub_classes))
            ]

# ----------------------------------------------------------------------------------------------------------------------
def getClassHist(classes_topics_descr, classes_sub_classes):

    return [
            dcc.Graph(figure=getClassBarChart(classes_topics_descr,classes_sub_classes))
            ]