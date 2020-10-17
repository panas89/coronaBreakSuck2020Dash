BAR_COLORS = ['#5497ac'] #['#4285F4']

# Nav Bar
NAV_BAR_COLOR = '#001b2d'

# Buttons
BUTTON_BACKGROUND_COLOR = NAV_BAR_COLOR
BUTTON_COLOR = 'white'

# Tables
TABLE_HEADER_BACKGROUND_COLOR = NAV_BAR_COLOR #'#9BCAF7'
TABLE_HEADER_COLOR = 'white'
TABLE_ROW_COLOR = '#E6EFF9'
TABLE_FONT_FAMILY = 'Arial' #'Sans-serif'
TABLE_FONT_SIZE = '18px'

# Time Series
TIME_COLORS = ['#000000',
'#5D43D2',
'#4380D2',
'#43B8D2',
'#43D2A2',
'#D2CE43',
'#D9AC32',
'#E76115',
'#F03412'
]



STYLE_TABLE = dict(
        page_size=20,
        export_format='xlsx',
        export_headers='display',
        editable=True,
        css=[{"selector": "button",
              "rule": f"""outline: none; 
                      border: none; 
                      background: {BUTTON_BACKGROUND_COLOR}; 
                      color: {BUTTON_COLOR};
                      font-size: 16px;
                      padding: 5px 15px 5px 15px;
                      border-radius: 5px
                      """},
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
        style_data_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': TABLE_ROW_COLOR
            }
        ],
        style_header={
            'backgroundColor': TABLE_HEADER_BACKGROUND_COLOR,
            'color': TABLE_HEADER_COLOR,
        },
        # style_cell_conditional=[
        #     {
        #         'if': {'column_id': col},
        #         'textAlign': 'left'
        #     } for col in ['Date', 'Region']
        # ],
        tooltip_duration=None,
    )