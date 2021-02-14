import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os
from assets.styling import *

from app import app
from apps import topicmodeling, about, homepage, nre, rextractor

# ======================================================================================================================
# HEADER
# ======================================================================================================================
port = int(os.environ.get("PORT", 5000))

if port == 5000:
    BASE_URL = "http://0.0.0.0:5000"
else:
    BASE_URL = "http://covidinsights.herokuapp.com"

header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink("Home", href=os.path.join(BASE_URL, "apps", "homepage"))
        ),
        dbc.NavItem(
            dbc.NavLink(
                "Topic Modeling", href=os.path.join(BASE_URL, "apps", "topicmodeling")
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                "Relationship Extraction Live tool",
                href=os.path.join(BASE_URL, "apps", "rextractor"),
            )
        ),
        dbc.NavItem(dbc.NavLink("NRE", href=os.path.join(BASE_URL, "apps", "nre"))),
        dbc.NavItem(
            dbc.NavLink("About Us", href=os.path.join(BASE_URL, "apps", "about"))
        ),
    ],
    brand="NLP For Covid-19 Publications",
    brand_href=os.path.join(BASE_URL, "apps", "homepage"),
    color=NAV_BAR_COLOR,
    dark=True,
)

# ======================================================================================================================
# APP LAYOUT
# ======================================================================================================================
app.layout = html.Div(
    [header, dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# ======================================================================================================================
# Callbacks
# ======================================================================================================================
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/apps/topicmodeling":
        return topicmodeling.layout
    elif pathname == "/apps/about":
        return about.layout
    elif pathname == "/apps/nre":
        return nre.layout
    elif pathname == "/apps/rextractor":
        return rextractor.layout
    else:
        return homepage.layout


# ######################################################################################################################
if __name__ == "__main__":
    # app.run_server(debug=True, host="0.0.0.0", port=port)
    app.run_server(debug=False, host="0.0.0.0", port=port)