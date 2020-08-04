import plotly as pltly
import plotly.graph_objs as go
import random

import sys
sys.path.append("..")
from assets.input_data import *

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


def getStackedBarChart(classes_topics_descr,classes_sub_classes,num_of_topics=20):
    """Method to plot grouped bar charts, have to loop first by topic then by class to have class name in x-axis."""
    x_axis_vals = [class_sub_class.replace('_topic','').replace('_',' ').capitalize() for class_sub_class in classes_sub_classes]
    y_axis_vals = []
    names = []

    for topic_num in range(num_of_topics):
        values = []
        name_values = []
        for class_sub_class in classes_sub_classes:
            try:
                values.append(np.sum(classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['counts']))
                name_values.append(classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['name'])
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


def getClassBarChart(classes_topics_descr,classes_sub_classes):
    """Method to plot histogram of papers for each class, class name in x-axis."""
    x_axis_vals = [class_sub_class.replace('_topic','').replace('_',' ').capitalize() for class_sub_class in classes_sub_classes]
    y_axis_vals = []

    for class_sub_class in classes_sub_classes:
        values = []
        for topic_num in range(len(classes_topics_descr[class_sub_class])):
            values.append(np.sum(classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['counts']))
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

def getTopicsBarChart(classes_topics_descr,class_sub_class):
    """Method to plot bar chart of topics"""
    x_axis_vals = [classes_topics_descr[class_sub_class]['topic_'+str(num)]['name'] for num,_ in enumerate(classes_topics_descr[class_sub_class])]
    y_axis_vals = [np.sum(classes_topics_descr[class_sub_class]['topic_'+str(num)]['counts']) for num,_ in enumerate(classes_topics_descr[class_sub_class])]

    fig = go.Figure(data=go.Bar(
                                x=x_axis_vals,
                                y=y_axis_vals,
                                marker_color =  colors
                            ),
                    layout=go.Layout(
                                    title=go.layout.Title(text= class_sub_class.replace('_topic','').replace('_',' ').capitalize() + " - Topic distribution"),
                                    yaxis={'tickformat': ',d'},
                                    title_x=0.5,
                                    margin=dict(l=40, r=0, t=40, b=30)
                                )
                    )

    return fig


# def getTopicsBarChart(classes_topics_descr,class_sub_class):
#     """Method to topics histogram, to have topic's name in x-axis."""
#     x_axis_vals = [class_sub_class.replace('_topic','').replace('_',' ').capitalize() for class_sub_class in classes_sub_classes]
#     y_axis_vals = []

#     for class_sub_class in classes_sub_classes:
#     values = []
#     for topic_num in range(len(classes_topics_descr[class_sub_class])):
#         values.append(np.sum(classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['counts']))
#     y_axis_vals.append(np.sum(values))                  

#     fig = go.Figure(data=go.Bar(
#                                 x=x_axis_vals,
#                                 y=y_axis_vals
#                             )
#                     )

#     return fig

def getRecoveriesFig(dates_rec,rec_data):
    """Method to get recoveries timeseries"""
    return dict(
                data=[
                    dict(
                        x=dates_rec,
                        y=rec_data,
                        name='Recoveries',
                        marker=dict(
                            color='rgb(55, 83, 109)'
                        )
                    ),
                ],
                layout=dict(
                    title='New Covid recoveries',
                    showlegend=True,
                    legend=dict(
                        x=0,
                        y=1.0
                    ),
                    margin=dict(l=40, r=0, t=40, b=30)
                )
            )


def getIncFig(dates_inc,inc_data):
    """Method to get incident timeseries"""
    return dict(
                data=[
                    dict(
                        x=dates_inc,
                        y=inc_data,
                        name='Positive cases',
                        marker=dict(
                            color='rgb(55, 83, 109)'
                        )
                    ),
                ],
                layout=dict(
                    title='New Covid cases',
                    showlegend=True,
                    legend=dict(
                        x=0,
                        y=1.0
                    ),
                    margin=dict(l=40, r=0, t=40, b=30)
                )
            )

def getDeathFig(dates_death,death_data):
    """Method to get incident timeseries"""
    return dict(
                data=[
                    dict(
                        x=dates_death,
                        y=death_data,
                        name='Deaths',
                        marker=dict(
                            color='rgb(55, 83, 109)'
                        )
                    ),
                ],
                layout=dict(
                    title='New Covid deaths',
                    showlegend=True,
                    legend=dict(
                        x=0,
                        y=1.0
                    ),
                    margin=dict(l=40, r=0, t=40, b=30)
                )
            )