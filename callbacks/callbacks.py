
from assets.input_data import *
from components.core_components import *
from components.components_utils import *

def getTopicFig(class_sub_class,topics_descr):
    
    return dict(
                    data=[
                        dict(
                            x=topics_descr['topic_'+str(topic_num)]['times'],
                            y=topics_descr['topic_'+str(topic_num)]['counts'],
                            name=topics_descr['topic_'+str(topic_num)]['name']
                        ) for topic_num in range(len(topics_descr))
                    ],
                    layout=dict(
                        title=class_sub_class.replace('topic','').replace('_',' ').capitalize() + ' - Topic time distribution',
                        showlegend=True,
                        yaxis={'tickformat': ',d'},
                        legend=dict(
                            x=0,
                            y=1.0
                        ),
                        margin=dict(l=40, r=0, t=40, b=30),
                        colorway =   colors
                    )
                )

def getGroupedHist(classes_topics_descr,classes_sub_classes):

    return [
            dcc.Graph(figure=getStackedBarChart(classes_topics_descr,classes_sub_classes))
            ]

def getClassHist(classes_topics_descr,classes_sub_classes):

    return [
            dcc.Graph(figure=getClassBarChart(classes_topics_descr,classes_sub_classes))
            ]

def getTopicsHist(classes_topics_descr,class_sub_class):

    return getTopicsBarChart(classes_topics_descr,class_sub_class)

def getVis(class_sub_class):
    # read visualization
    with open(TOPIC_MODELLING_PATH+class_sub_class.replace('_topic','')+'/vis.pickle', 'rb') as mod:
        vis = pickle.load(mod)

    return pyLDAvis.prepared_data_to_html(vis)


# fig_wcloud = [dcc.Graph(figure=wordCloudFigure(topics_descr['topic_'+str(topic_num)]),
    #                                     style={'width': '30%',
    #                                            'padding': '0px 0px 0px 0px',
    #                                            'display': 'inline-block'})
    #                                 for topic_num in range(len(topics_descr))]s


def getPapers(class_sub_class,topic,df):
    df_papers = df.loc[df[class_sub_class]==int(topic[-1])-1,table_cols].reset_index(drop=True)

    return [dash_table.DataTable(
                                        data=df_papers.to_dict('records'),
                                        columns=[{'id': c, 'name': c} for c in table_cols],
                                        page_size=10,
                                        filter_action='native',

                                        style_cell={
                                                    'overflow': 'hidden',
                                                    'textOverflow': 'ellipsis',
                                                    'maxWidth': 0,
                                                },
                                                tooltip_data=[
                                                    {
                                                        column: {'value': str(value), 'type': 'markdown'}
                                                        for column, value in row.items()
                                                    } for row in df_papers[table_cols].to_dict('rows')
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

def getDropDownTopics(classes_topics_descr,class_sub_class):
    return [
                {'label': classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['name'], \
                 'value': classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['name']} for topic_num in range(len(classes_topics_descr[class_sub_class]))
            ]