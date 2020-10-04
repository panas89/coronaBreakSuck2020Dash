from assets.input_data import *
from components.core_components import *
from components.components_utils import *
from datetime import datetime as dt

import ast

# ######################################################################################################################


def getTopicFig(class_subclass, topics_descr):

    return dict(
        data=[
            dict(
                x=[dt.strptime(date, '%m-%d-%Y') for date in topics_descr['topic_'+str(topic_num)]['times']],
                y=topics_descr['topic_'+str(topic_num)]['counts'],
                name=topics_descr['topic_'+str(topic_num)]['name']
            ) for topic_num in range(len(topics_descr))
        ],
        layout=dict(
            title=format_class_subclass(
                class_subclass) + ' - Topic time distribution',
            showlegend=True,
            yaxis={'tickformat': ',d'},
            xaxis_tickformat = '%d %B (%a)<br>%Y',
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=40, b=30),
            colorway=TIME_COLORS
        )
    )

# ----------------------------------------------------------------------------------------------------------------------


def getTopicsHist(classes_topics_descr, class_subclass):

    return getTopicsBarChart(classes_topics_descr, class_subclass)

# ----------------------------------------------------------------------------------------------------------------------


def getPapers(class_subclass, topics, df):
    list_of_topics_ind = [int(topic[-1])-1 for topic in topics]

    # Format table entries
    df.publish_time = df.publish_time.dt.strftime('%Y-%m-%d')
    df.affiliations_country = df.affiliations_country.apply(
        lambda x: ', '.join(x.split(',')) if x is not np.nan else x)
    df_papers = df.loc[df[class_subclass].isin(
        list_of_topics_ind), TABLE_COLS].reset_index(drop=True)

    return [dash_table.DataTable(
        data=df_papers.to_dict('records'),
        columns=[{'id': col,
                  'name': ' '.join(col.split('_')).title(),
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
        css=[{"selector": "button",
              "rule": f"""outline: none; 
                      border: none; 
                      background: {TABLE_ROW_COLOR}; 
                      font-size: 16px"""},
            {"selector": ".dash-spreadsheet-menu-item", 
            "rule": "padding-right: 10px; padding-bottom: 10px; outline: none"},
             {"selector": ".column-header--delete svg",
              "rule": 'display: "none"'},
             {"selector": ".column-header--delete::before",
              "rule": 'content: "X"'}
             ],
        filter_action='native',
        # style_data={'border': '0px'},
        style_cell={
            'overflow': 'hidden',
            'font_family': TABLE_FONT_FAMILY,
            'font-size': TABLE_FONT_SIZE,
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
        },
        tooltip_data=[
            {
                column: {'value': str(
                    value), 'type': 'markdown'}
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
                'if': {'row_index': 'even'},
                'backgroundColor': TABLE_ROW_COLOR
            }
        ],
        style_header={
            'backgroundColor': TABLE_HEADER_COLOR,
            'fontWeight': 'bold'
        }
    )
    ]

def getRelations(df_relation_f):
    """
    This function returns the Dash element (table) about the entity relations with coronavirus. 
    
    :param df_relation_f (dataframe: stores the entity relationships with coronavirus.  
    """
    # Clean up the relation columns
    rs = []
    for x in df_relation_f['relations'].tolist():
        if isinstance(x, str):
            rx = ast.literal_eval(x)

            # create content string
            ss = []
            for c in rx:
                s = "%s('%s', %.3f)"%(c[1],c[2][0],c[2][1])
                ss.append(s)
            rx = ", ".join(ss)
        else:
            rx = None
        rs.append(rx)
    df_relation_f['relations'] = rs
    
    # Create the Dash table object
    table = [dash_table.DataTable(
        data=df_relation_f.to_dict('records'),
        columns=[{'id': col,
                  'name': ' '.join(col.split('_')).title(),
                  'clearable': True,
                  'renamable': True,
                  'hideable': True,
                  'deletable': True}
                 for col in RELATION_TABLE_COLS
                 ],
        page_size=20,
        export_format='xlsx',
        export_headers='display',
        editable=True,
        css=[{"selector": "button",
              "rule": f"""outline: none; 
                      border: none; 
                      background: {TABLE_ROW_COLOR}; 
                      font-size: 16px"""},
            {"selector": ".dash-spreadsheet-menu-item", 
            "rule": "padding-right: 10px; padding-bottom: 10px; outline: none"},
             {"selector": ".column-header--delete svg",
              "rule": 'display: "none"'},
             {"selector": ".column-header--delete::before",
              "rule": 'content: "X"'}
             ],
        filter_action='native',
        # style_data={'border': '0px'},
        style_cell={
            'overflow': 'hidden',
            'font_family': TABLE_FONT_FAMILY,
            'font-size': TABLE_FONT_SIZE,
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
        },
        tooltip_data=[
            {
                column: {'value': str(
                    value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df_relation_f[RELATION_TABLE_COLS].to_dict('rows')
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
                'if': {'row_index': 'even'},
                'backgroundColor': TABLE_ROW_COLOR
            }
        ],
        style_header={
            'backgroundColor': TABLE_HEADER_COLOR,
            'fontWeight': 'bold'
        }
    )
    ]
    
    return table

# ----------------------------------------------------------------------------------------------------------------------


def getDropDownTopics(classes_topics_descr, class_subclass):
    return [
        {'label': classes_topics_descr[class_subclass]['topic_'+str(topic_num)]['name'],
         'value': classes_topics_descr[class_subclass]['topic_'+str(topic_num)]['name']}
        for topic_num in range(len(classes_topics_descr[class_subclass]))
    ]

# ----------------------------------------------------------------------------------------------------------------------


def getTopicKwsTable_v2(df, class_subclass):
    topic2kws = getTopic2Kws(df, class_subclass)
    fig = go.Figure(data=[go.Table(header=dict(values=[f'Topic {topic_num}' for topic_num in topic2kws.keys()]),
                                   cells=dict(values=[kws for kws in topic2kws.values()]))
                          ])

    return fig

# ----------------------------------------------------------------------------------------------------------------------
def getTopicKwsTable(df, class_subclass):

    topic2kws = getTopic2Kws(df, class_subclass)
    topic2kws = dict((f'Topic {topic_num}', kws)
                     for topic_num, kws in topic2kws.items())
    table = dash_table.DataTable(
        id='table_2',
        columns=[{"name": topic,
                  "id": topic}
                 for topic in topic2kws.keys()],
        data=pd.DataFrame.from_dict(topic2kws).to_dict('records'),
        style_data={'border': '0px'},
        style_table={
            'overflowX': 'auto',
            # 'maxWidth': 0,
        },
        style_as_list_view=True,

        style_cell={
            'height': 'auto',
            'font_family': TABLE_FONT_FAMILY,
            'font-size': TABLE_FONT_SIZE,
            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            'whiteSpace': 'normal'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': TABLE_ROW_COLOR
            }
        ],
        style_header={
            'backgroundColor': TABLE_HEADER_COLOR,
            'fontWeight': 'bold',
        }
    )

    return table

# ----------------------------------------------------------------------------------------------------------------------
def createCovidIncidentsFig(dates, data, incident_name) -> dict:
    """Method to get covid incidents timeseries"""
    return dict(
                data=[
                    dict(
                        x=[dt.strptime(date, '%m-%d-%Y') for date in dates],
                        y=data,
                        name=incident_name,
                        marker=dict(
                            color='rgb(55, 83, 109)'
                        )
                    ),
                ],
                layout=dict(
                    title=f'New Covid {incident_name}',
                    showlegend=True,
                    legend=dict(
                        x=0,
                        y=1.0
                    ),
                    margin=dict(l=40, r=0, t=40, b=30)
                )
            )