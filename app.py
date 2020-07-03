import flask
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as gobs
from components.core_components import *
from components.components_utils import *
import sys
sys.path.append("..")
from assets.input_data import *
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
                        class_stacked_topic,
                        proj_button,
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
     Output('topic-vis', 'srcDoc')],
    [Input('class-sub-class-drop-down', 'value')])
def update_figure(class_sub_class):

    topics_descr = classes_topics_descr[class_sub_class]

    fig_dist = dict(
                data=[
                    dict(
                        x=topics_descr['topic_'+str(topic_num)]['times'],
                        y=topics_descr['topic_'+str(topic_num)]['counts'],
                        name=topics_descr['topic_'+str(topic_num)]['name']
                    ) for topic_num in range(len(topics_descr))
                ],
                layout=dict(
                    title=class_sub_class.replace('topic','').replace('_',' ').capitalize() + ' - Topic distribution',
                    showlegend=True,
                    legend=dict(
                        x=0,
                        y=1.0
                    ),
                    margin=dict(l=40, r=0, t=40, b=30)
                )
            )

    # fig_wcloud = [dcc.Graph(figure=wordCloudFigure(topics_descr['topic_'+str(topic_num)]),
    #                                     style={'width': '30%',
    #                                            'padding': '0px 0px 0px 0px',
    #                                            'display': 'inline-block'})
    #                                 for topic_num in range(len(topics_descr))]

    # read visualization
    with open(TOPIC_MODELLING_PATH+class_sub_class.replace('_topic','')+'/vis.pickle', 'rb') as mod:
        vis = pickle.load(mod)


    vis_obj = pyLDAvis.prepared_data_to_html(vis)

    return fig_dist,vis_obj


@app.callback(
    [Output('table-papers', 'children'),
     Output('topic-drop-down', 'options')],
    [Input('class-sub-class-drop-down', 'value'),
     Input('topic-drop-down', 'value')])
def update_by_topic(class_sub_class,topic):

    topics_descr = classes_topics_descr[class_sub_class]

    df_papers = df.loc[df[class_sub_class]==int(topic[-1])-1,table_cols].reset_index(drop=True)

    children = [dash_table.DataTable(
                                        data=df_papers.to_dict('records'),
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
                                    )]

    options =[
                {'label': classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['name'], \
                 'value': classes_topics_descr[class_sub_class]['topic_'+str(topic_num)]['name']} for topic_num in range(len(classes_topics_descr[class_sub_class]))
            ]

    return children,options


if __name__ == '__main__':
    app.run_server(debug=True)