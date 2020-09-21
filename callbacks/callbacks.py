from assets.input_data import *
from components.core_components import *
from components.components_utils import *

# ######################################################################################################################
def getTopicFig(class_subclass, topics_descr):
    
    return dict(
                    data=[
                        dict(
                            x=topics_descr['topic_'+str(topic_num)]['times'],
                            y=topics_descr['topic_'+str(topic_num)]['counts'],
                            name=topics_descr['topic_'+str(topic_num)]['name']
                        ) for topic_num in range(len(topics_descr))
                    ],
                    layout=dict(
                        title= format_class_subclass(class_subclass) + ' - Topic time distribution',
                        showlegend=True,
                        yaxis={'tickformat': ',d'},
                        legend=dict(
                            x=0,
                            y=1.0
                        ),
                        margin=dict(l=40, r=0, t=40, b=30),
                        colorway=COLORS
                    )
                )

# ----------------------------------------------------------------------------------------------------------------------
def getTopicsHist(classes_topics_descr, class_subclass):

    return getTopicsBarChart(classes_topics_descr, class_subclass)

# ----------------------------------------------------------------------------------------------------------------------
def getPapers(class_subclass, topics, df):
    list_of_topics_ind = [int(topic[-1])-1 for topic in topics]
    df_papers = df.loc[df[class_subclass].isin(list_of_topics_ind),TABLE_COLS].reset_index(drop=True)

    return [dash_table.DataTable(
                            data=df_papers.to_dict('records'),
                            columns=[{'id': col, 
                                      'name': col,
                                      'clearable': True, 
                                      'renamable': True, 
                                      'hideable': True, 
                                      'deletable': True} 
                                     for col in TABLE_COLS
                                     ],
                            page_size=20,
                            export_format='xlsx',
                            export_headers='display',
                            editable=True,
                            css=[
                                    {"selector": ".column-header--delete svg", "rule": 'display: "none"'},
                                    {"selector": ".column-header--delete::before", "rule": 'content: "X"'}
                                ],
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
                                        } for row in df_papers[TABLE_COLS].to_dict('rows')
                                    ],
                            tooltip_duration=None,

                            style_cell_conditional=[
                                {
                                    'if': {'column_id': col},
                                    'textAlign': 'left'
                                } for col in ['Date', 'Region']
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

# ----------------------------------------------------------------------------------------------------------------------
def getDropDownTopics(classes_topics_descr, class_subclass):
    return [
            {'label': classes_topics_descr[class_subclass]['topic_'+str(topic_num)]['name'],
             'value': classes_topics_descr[class_subclass]['topic_'+str(topic_num)]['name']} 
            for topic_num in range(len(classes_topics_descr[class_subclass]))
            ]



