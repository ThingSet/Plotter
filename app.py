# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

con = sqlite3.connect("data/solarbox.db")
df = pd.read_sql_query("SELECT * from Solarbox;", con)
meas = list(df.columns.values)
meas.remove('index')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='LibreSolar Data Visualization'),
    html.Div('Choose a value to display'),
    dcc.Dropdown(
        id='meas-dropdown',
        options= [dict(label=item, value=item) for item in meas],
        value='SOC'
    ),
    dcc.Graph(id='solarbox')
], className="container")

@app.callback(Output('solarbox', 'figure'),
              [Input('meas-dropdown', 'value')])

def update_graph(selected_dropdown_value):
    return {
        'data': [{
            'x': df.index,
            'y': df[selected_dropdown_value],
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
        'layout': {
            'margin': {
                'l': 100,
                'r': 100,
                'b': 30,
                't': 30
            }
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)