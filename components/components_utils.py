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
                values.append(classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['counts'].sum())
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
