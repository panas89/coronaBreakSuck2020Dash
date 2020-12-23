from app import app
import dash_core_components as dcc
import dash_html_components as html
from assets.styling import *
import base64
import os

IMG_DIR = 'assets/images/'
PAGE_STYLE = {'width': '100%',
              'padding': '50px 50px 50px 50px',
              'display': 'inline-block'}
# ######################################################################################################################
# COMPONENTS
# ======================================================================================================================

image_filename = os.path.join(IMG_DIR, 'home_img.jpg')
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

background_pic = html.Div([
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                style={
                        'width': '100%',
                        'height': '100%',
                        'filter': 'brightness(50%)'
                    }),
                    html.Div(
                        html.H2('''Discover the trending topics and relationships in the covid-19 literature with NLP.
                                '''),
                        style={'position': 'absolute',
                            'top': '50%',
                            'left': '50%',
                            'transform': 'translate(-50%, -50%)',
                            'color': 'white'
                            }

                    )],
                    style={'width': '100%',
                        'position': 'relative',
                        # 'padding': '25px 50px 50px 25px',
                        'text-align': 'center',
                        'display': 'inline-block'}
                )

# ----------------------------------------------------------------------------------------------------------------------
content = dcc.Markdown("""

## **Content**

##### 1) Topic Modeling:
We use unsupervised Machine Learning to 
- discover the various topics discussed in thousands of scientific publications about covid-19
- plot the evolution of topics throughout time and,
- compare that to the time evolution of covid cases, deaths and recoveries. 

In this context, 
- a "covid paper" is a scientific publication whose abstract contains at least one of our hand-picked terms related to covid-19
- each topic is defined by a distinct collection of keywords pulled out from a subset of abstracts
- all the topics are "learned" using Latent Dirichlet Allocation modeling, optimized on topic coherence score.

##### 2) Neural Relation Extraction (NRE):

- yo
- yo

""",
    style=PAGE_STYLE)

# ######################################################################################################################
layout = html.Div([
    background_pic,
    content,
]
)
