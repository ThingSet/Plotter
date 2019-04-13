# -*- coding: utf-8 -*-

import argparse
import sqlite3
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

parser = argparse.ArgumentParser()
parser.add_argument("db", help="Path to SQLite database file.")
parser.add_argument("--table", help="Name of the table in the database (default: ThingSet)", default="ThingSet")
args = parser.parse_args()

con = sqlite3.connect(args.db)
df = pd.read_sql_query("SELECT * from " + args.table + ";", con)
meas = list(df.columns.values)
meas.remove('index')
opt = [dict(label=item, value=item) for item in meas]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True

app.layout = html.Div(children=[
    html.H1(children='Libre Solar ThingSet Interface'),
    dcc.Tabs(id="tabs-example", value='tab-data', children=[
        dcc.Tab(label='Data', value='tab-data'),
        dcc.Tab(label='Configuration', value='tab-conf'),
    ]),
    html.Div(id='tabs-content')
], className="container")


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-data':
        return html.Div([
            dcc.Dropdown(
                id='data-sel-1',
                options=opt,
                multi=True
            ),
            dcc.Graph(id='graph-1'),

            dcc.Dropdown(
                id='data-sel-2',
                options=opt,
                multi=True
            ),
            dcc.Graph(id='graph-2'),
        ])
    elif tab == 'tab-conf':
        return html.Div([
            html.Div([
                daq.BooleanSwitch(
                    id='my-daq-booleanswitch',
                    label='Send boolean value',
                    on=True
                )],
                style={'padding': '20px 0px 20px 0px'}
            ),
            html.Div(id='output-boolean', style={'align':'center'}),
            daq.NumericInput(
                id='my-numeric-input',
                label='Set numeric value',
                value=0,
                style={'padding': '20px 0px 20px 0px'}
            ),
            html.Div(id='numeric-input-output')
        ])


@app.callback(
    dash.dependencies.Output('output-boolean', 'children'),
    [dash.dependencies.Input('my-daq-booleanswitch', 'on')])
def update_output_switch(on):
    print(str(on))
    return 'The switch is {}.'.format(on)

@app.callback(
    dash.dependencies.Output('numeric-input-output', 'children'),
    [dash.dependencies.Input('my-numeric-input', 'value')])
def update_output(value):
    return 'The value is {}.'.format(value)

@app.callback(Output('graph-1', 'figure'),
              [Input('data-sel-1', 'value')])
def update_graph(selected_dropdown_value):
    if not selected_dropdown_value:
        pass
    else:
        return {
            'data': [{
                'x': df.time,
                'y': df[value],
                'name': value,
                'line': {
                    'width': 3,
                    'shape': 'spline'
                }
            } for value in selected_dropdown_value],
            'layout': {
                'margin': {
                    'l': 100,
                    'r': 100,
                    'b': 30,
                    't': 30
                }
            }
        }

@app.callback(Output('graph-2', 'figure'),
              [Input('data-sel-2', 'value')])
def update_graph(selected_dropdown_value):
    if not selected_dropdown_value:
        pass
    else:
        return {
            'data': [{
                'x': df.time,
                'y': df[value],
                'name': value,
                'line': {
                    'width': 3,
                    'shape': 'spline'
                }
            } for value in selected_dropdown_value],
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