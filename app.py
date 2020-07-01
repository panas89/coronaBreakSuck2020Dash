import flask
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as gobs
from components.core_components import *

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
                        topic_dist,
                        topic_word_clouds,
                        inc_death_rec_plots,
                        topic_vis,
                        topic_dd,
                        paper_table
                        ])

if __name__ == '__main__':
    app.run_server(debug=True)