
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_core_components as dcc
import dash_table

import sys
sys.path.append("..")
from assets.input_data import *

class_sub_class_dd = html.Div([
                html.Label('Class - Subclass'),
                dcc.Dropdown(
                    id='class-sub-class-drop-down',
                    options=[
                        {'label': class_sub_class.replace('_topic','').replace('_',' ').capitalize(),\
                             'value': class_sub_class} for class_sub_class in classes_sub_classes
                    ],
                    value='MTL'
                )  
            ], style={'width': '48%',
                      'padding': '25px 50px 75px 50px',
                      'display': 'inline-block'})

location_dd = html.Div([
                html.Label('Location'),
                dcc.Dropdown(
                    id='location-drop-down',
                    options=[
                        {'label': country, 'value': country} for country in location_country
                    ],
                    value='MTL'
                )  
            ], style={'width': '48%',
                      'padding': '25px 50px 75px 50px',
                      'display': 'inline-block'})

topic_dd = html.Div([
                html.Label('Topic'),
                dcc.Dropdown(
                    id='topic-drop-down',
                    options=[
                        {'label': topics_descr['topic_'+str(topic_num)]['name'], \
                             'value': topics_descr['topic_'+str(topic_num)]['name']} for topic_num in range(len(topics_descr))
                    ],
                    value='MTL'
                )  
            ], style={'width': '48%',
                      'padding': '25px 50px 75px 50px',
                      'display': 'inline-block'})

class_loc = html.Div(
                    [class_sub_class_dd,location_dd]
                    , style={'width': '100%',
                             'display': 'inline-block'})


pb_time = html.Div([
                html.Label('Publication date'),
                dcc.RangeSlider(
                    id='pub-date-slider',
                    min=0,
                    max=time_diff,
                    value=[0,10],
                    marks={time_point : \
                            str(df['publish_time'].min() \
                        + datetime.timedelta(days=time_point))[:10] \
                         for time_point in range(0,time_diff+11,11)},
                ),
            ], style={'width': '100%',
                      'padding': '25px 50px 50px 50px',
                      'display': 'inline-block'})

proj_button = html.Div([
                    dbc.Button("Show projections", color="primary", block=True)
                        ], style={'width': '100%',
                      'padding': '25px 50px 50px 50px',
                      'display': 'inline-block'})

print(class_sub_class)

topic_dist = html.Div([
                dcc.Graph(
                        figure=dict(
                            data=[
                                dict(
                                    x=topics_descr['topic_'+str(topic_num)]['times'],
                                    y=topics_descr['topic_'+str(topic_num)]['counts'],
                                    name=topics_descr['topic_'+str(topic_num)]['name']
                                ) for topic_num in range(len(topics_descr))
                            ],
                            layout=dict(
                                title=class_sub_class+' - Topic distribution',
                                showlegend=True,
                                legend=dict(
                                    x=0,
                                    y=1.0
                                ),
                                margin=dict(l=40, r=0, t=40, b=30)
                            )
                        ),
                        style={'height': 300},
                        id='topic-dist'
                    )  
            ], style={'width': '100%',
                'padding': '25px 50px 50px 50px',
                'display': 'inline-block'})

incident_cases = html.Div([
                dcc.Graph(
                        figure=dict(
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
                        ),
                        style={'height': 300},
                        id='covid-cases'
                    )  
            ], style={'width': '33%',
                'padding': '3px 5px 10px 10px',
                'display': 'inline-block'})

death_cases = html.Div([
                dcc.Graph(
                        figure=dict(
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
                        ),
                        style={'height': 300},
                        id='covid-deaths'
                    )  
            ], style={'width': '33%',
                'padding': '3px 5px 10px 10px',
                'display': 'inline-block'})

recovery_cases = html.Div([
                dcc.Graph(
                        figure=dict(
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
                        ),
                        style={'height': 300},
                        id='covid-recoveries'
                    )  
            ], style={'width': '33%',
                'padding': '3px 5px 10px 10px',
                'display': 'inline-block'})

inc_death_rec_plots = html.Div(
                                [incident_cases,
                                 death_cases,
                                 recovery_cases]
                        , style={'width': '100%',
                                 'padding': '25px 50px 50px 50px',
                                 'display': 'inline-block'})


topic_vis = html.Div([
                    html.Iframe(srcDoc=pyLDAvis.prepared_data_to_html(vis) 
                        ,style={'width': '100%',
                                'height': '100%',
                                'text-align': 'center',
                                'display': 'center'}
                        )
                    ]
                , style={'width': '100%',
                         'height': '1000px',
                                 'padding': '25px 50px 50px 50px',
                                 'text-align': 'center',
                                 'display': 'inline-block'})


paper_table = html.Div([
                    dash_table.DataTable(
                                        data=df[table_cols].to_dict('records'),
                                        columns=[{'id': c, 'name': c} for c in table_cols],
                                        page_size=10,

                                        style_cell={
                                                    'overflow': 'hidden',
                                                    'textOverflow': 'ellipsis',
                                                    'maxWidth': 0,
                                                },
                                                tooltip_data=[
                                                    {
                                                        column: {'value': str(value), 'type': 'markdown'}
                                                        for column, value in row.items()
                                                    } for row in df[table_cols].to_dict('rows')
                                                ],
                                        tooltip_duration=None,

                                        style_cell_conditional=[
                                            {
                                                'if': {'column_id': c},
                                                'textAlign': 'left'
                                            } for c in ['Date', 'Region']
                                        ],
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': 'rgb(248, 248, 248)'
                                            }
                                        ],
                                        style_header={
                                            'backgroundColor': 'rgb(230, 230, 230)',
                                            'fontWeight': 'bold'
                                        }
                                    )
                        ]
                , style={'width': '100%',
                         'height': '1000px',
                                 'padding': '25px 50px 50px 50px',
                                 'text-align': 'center',
                                 'display': 'inline-block'})

import plotly as pltly
import plotly.graph_objs as go
import random

def wordCloudFigure(topic_descr):

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



topic_word_clouds = html.Div([
                            dcc.Graph(figure=wordCloudFigure(topics_descr['topic_'+str(topic_num)]),
                                        style={'width': str(1.98*100/len(topics_descr))+'%',
                                               'padding': '0px 0px 0px 0px',
                                               'display': 'inline-block'})
                                    for topic_num in range(len(topics_descr))
                            ]
                    , style={'width': '100%',
                            'display': 'inline-block'})


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

class_stacked_topic = html.Div([
                                dcc.Graph(figure=getStackedBarChart(classes_topics_descr,classes_sub_classes))
                                ]
                        , style={'width': '100%',
                                'height': '100%',
                                'display': 'inline-block'})