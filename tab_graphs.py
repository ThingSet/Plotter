# -*- coding: utf-8 -*-

import argparse
import sqlite3
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

from app import opt

def content():
    return html.Div([
        dcc.Dropdown(
            id='data-sel-1',
            options=opt,
            multi=True,
        ),
        dcc.Graph(
            id='graph-1',
            style={'padding': '20px 0px 20px 0px'},
        ),

        dcc.Dropdown(
            id='data-sel-2',
            options=opt,
            multi=True,
        ),
        dcc.Graph(
            id='graph-2',
            style={'padding': '20px 0px 20px 0px'},
        ),
    ])


