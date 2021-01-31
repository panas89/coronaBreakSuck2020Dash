from app import app
import dash_core_components as dcc
import dash_html_components as html
from assets.styling import *
import base64
import os
from assets.input_data import DASH_DIR

IMG_DIR = os.path.join(DASH_DIR, 'assets/images/')
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

We utilize a Deep Learning open-source package, OpenNRE \[1\], to
- extract semantic relationships between two entities of interest within the covid-19 literature
- identify whether an entity of interest has a strong relationship with the word "coronavirus" (and/or its aliases)

Implementation: 
- We apply the package’s supervised sentence-level NRE model, which is a BERT model \[2\] trained using 56,000 sentences from WikiData \[3\]
- This NRE model outputs 
    1. the probability of two entities to be related
    2. the type of relationship (e.g. “X is the father of Y”)
- Among the 80+ possible relationship types, we consider only the most relevant one to our work, namely: "is related to".
- At last, we visualize the strength of relationship between select keywords and covid-19.

\[1\]	X. Han, T. Gao, Y. Yao, D. Ye, Z. Liu, and M. Sun, “OpenNRE: An open and extensible toolkit for neural relation extraction,” arXiv Prepr. arXiv1909.13078, 2019. 

\[2\]	J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training of deep bidirectional transformers for language understanding,” arXiv Prepr. arXiv1810.04805, 2018. 

\[3\]	D. Vrandečić and M. Krötzsch, “Wikidata: a free collaborative knowledgebase,” Commun. ACM, vol. 57, no. 10, pp. 78–85, 2014.
""",
    style=PAGE_STYLE)

# ######################################################################################################################
layout = html.Div([
    background_pic,
    content,
]
)
