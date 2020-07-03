
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_core_components as dcc
import dash_table

from .components_utils import *

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
                    value='disease_comorbidity_topic'
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
                    # options=[
                    #     {'label': classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['name'], \
                    #          'value': classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['name']} for topic_num in range(len(classes_topics_descr[class_sub_class]))
                    # ],
                    value='Topic 1'
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


topic_dist = html.Div([
                dcc.Graph(
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

topic_dist_vis = html.Div(
                    [topic_dist,topic_vis]
                    , style={'width': '100%',
                             'display': 'inline-block'})


paper_table = html.Div(                    
                            id='table-papers'
                , style={'width': '100%',
                         'height': '1000px',
                                 'padding': '25px 50px 50px 50px',
                                 'text-align': 'center',
                                 'display': 'inline-block'})


# topic_word_clouds = html.Div(
#                             # [
#                             # # dcc.Graph(figure=wordCloudFigure(topics_descr['topic_'+str(topic_num)]),
#                             # #             style={'width': str(1.98*100/len(topics_descr))+'%',
#                             # #                    'padding': '0px 0px 0px 0px',
#                             # #                    'display': 'inline-block'})
#                             # #         for topic_num in range(len(topics_descr))
#                             # ]
#                      id='topic-wcloud'
#                      , style={'width': '70%',
#                                 'height': '100%',
#                                 'display': 'inline-block'}
#                    )


class_stacked_topic = html.Div([
                                dcc.Graph(figure=getStackedBarChart(classes_topics_descr,classes_sub_classes))
                                ]
                        , style={'width': '100%',
                                'height': '100%',
                                'display': 'inline-block'})