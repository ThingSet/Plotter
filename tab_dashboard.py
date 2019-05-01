# -*- coding: utf-8 -*-

import argparse
import sqlite3
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

def content():
    return html.Div([
        html.Div([
        ], className="three columns"),
        html.Div([
        ], className="nine columns"),

        html.Div([
        ], className="twelve columns"),
    ], className="row")


