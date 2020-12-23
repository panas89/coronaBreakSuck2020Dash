import os 
import base64
from app import app
import dash_html_components as html
import dash_bootstrap_components as dbc
from assets.styling import *

IMG_DIR = 'assets/images/'

# ######################################################################################################################
# HELPER FUNCTIONS
# ======================================================================================================================

def create_html_card(image_filename, name, description, linkedin_url):
    image_filepath = os.path.join(IMG_DIR, image_filename)
    encoded_image = base64.b64encode(open(image_filepath, 'rb').read())

    card = dbc.Card(
        [
            dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image.decode()), top=True),
            dbc.CardBody(
                [
                    html.H5(name),
                    html.P(description),
                    html.A(dbc.Button("LinkedIn", 
                            style={
                                'background-color': BUTTON_BACKGROUND_COLOR,
                                'color': BUTTON_COLOR,
                                'border': 'none'
                            }),
                           href=linkedin_url, 
                           target='_blank'
                    ),
                ]
            ),
        ],
    )

    html_card = html.Div(card, 
                         style={"width": "30%", 
                                "padding": "20px 20px 20px 20px", 
                                'display': 'inline-block'}
                ) 

    return html_card

# ======================================================================================================================
# ABOUT US INFO
# ======================================================================================================================

vasilis_card_info = dict(
    image_filename='vasilis_img.jpeg',
    name= 'Vasilis Stylianou, PhD',
    description= 'stylianouvasilis@gmail.com', 
    linkedin_url= 'https://www.linkedin.com/in/vasilis-stylianou-phd-165012106/'
)

panayiotis_card_info = dict(
    image_filename='panayiotis_img.jpeg',
    name= 'Panayiotis Petousis, PhD',
    description= 'panayiotispetousis@gmail.com', 
    linkedin_url= 'https://www.linkedin.com/in/panayiotis-petousis-a37a2751/'
)

johnny_card_info = dict(
    image_filename='johnny_img.jpeg',
    name= 'King Chung Ho, PhD',
    description= 'johnny5550822@g.ucla.edu', 
    linkedin_url= 'https://www.linkedin.com/in/kingchungho/'
)


# ======================================================================================================================
# APP LAYOUT
# ======================================================================================================================
layout = html.Div(
            [
                create_html_card(**panayiotis_card_info),
                create_html_card(**vasilis_card_info),
                create_html_card(**johnny_card_info),
            ],
            style={
                "padding": "25px 25px 25px 25px", 
                "text-align": "center",
                'display': 'inline-block'},
        )