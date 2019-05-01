# -*- coding: utf-8 -*-

import argparse
import sqlite3
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

# local files
import tab_graphs, tab_dashboard, tab_setup

parser = argparse.ArgumentParser()
parser.add_argument("db", help="Path to SQLite database file.")
parser.add_argument("--table", help="Name of the table in the database (default: ThingSet)", default="ThingSet")
args = parser.parse_args()

con = sqlite3.connect(args.db)
df = pd.read_sql_query("SELECT * from " + args.table + ";", con)
meas = list(df.columns.values)
meas.remove('index')
opt = [dict(label=item, value=item) for item in meas]

app = dash.Dash(__name__)
#app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.config['suppress_callback_exceptions']=True

app.layout = html.Div(children=[
    #html.H1(children='Libre Solar ThingSet Interface'),
    dcc.Tabs(id="tabs-example", value='tab-dashboard', children=[
        dcc.Tab(label='Dashboard', value='tab-dashboard'),
        dcc.Tab(label='Graphs', value='tab-graphs'),
        dcc.Tab(label='Setup', value='tab-setup'),
    ], style={'padding': '20px 0px 20px 0px'}),
    html.Div(id='tabs-content')
], className="container")


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-graphs':
        return tab_graphs.content()
    elif tab == 'tab-dashboard':
        return tab_dashboard.content()
    elif tab == 'tab-setup':
        return tab_setup.content()


@app.callback(
    Output('output-boolean', 'children'),
    [Input('my-daq-booleanswitch', 'on')])
def update_output_switch(on):
    print(str(on))
    return 'The switch is {}.'.format(on)

@app.callback(
    Output('numeric-input-output', 'children'),
    [Input('my-numeric-input', 'value')])
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
                    'l': 30,
                    'r': 30,
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
                    'l': 30,
                    'r': 30,
                    'b': 30,
                    't': 30
                }
            }
        }

if __name__ == '__main__':
    app.run_server(debug=True)