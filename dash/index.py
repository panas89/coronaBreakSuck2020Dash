import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os
from assets.styling import *

from app import app
from apps import topicmodeling, about, homepage, nre

# ======================================================================================================================
# HEADER
# ======================================================================================================================
BASE_URL = "http://127.0.0.1:8050/"

header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href=os.path.join(BASE_URL, 'apps', 'homepage'))),
        dbc.NavItem(dbc.NavLink("Topic Modeling", href=os.path.join(BASE_URL, 'apps', 'topicmodeling'))),
        dbc.NavItem(dbc.NavLink("NRE", href=os.path.join(BASE_URL, 'apps', 'nre'))),
        dbc.NavItem(dbc.NavLink("About Us", href=os.path.join(BASE_URL, 'apps', 'about'))),
    ],
    brand="NLP For Covid-19 Publications",
    brand_href=os.path.join(BASE_URL, 'apps', 'homepage'),
    color=NAV_BAR_COLOR,
    dark=True
)

# ======================================================================================================================
# APP LAYOUT
# ======================================================================================================================
app.layout = html.Div([
    header,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# ======================================================================================================================
# Callbacks
# ======================================================================================================================
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/topicmodeling':
        return topicmodeling.layout
    elif pathname == '/apps/about':
        return about.layout
    elif pathname == '/apps/nre':
        return nre.layout
    else:
        return homepage.layout

# ######################################################################################################################
if __name__ == '__main__':
    app.run_server(debug=True)