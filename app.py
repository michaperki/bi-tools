from dash import Dash, dash_table, dcc, html, callback, Output, Input
import pandas as pd
from collections import OrderedDict
from read_data import df
import plotly.express as px

dim = df.shape[0]

app = Dash(__name__)

app.layout = html.Div([
    # ---------------------------------------- #
    # Header
    html.H1(f'{dim} records'),
    # ---------------------------------------- #
    # Tabs
    dcc.Tabs(
        id="tab",
        value="table",
        children=[
            dcc.Tab(label="Table", value="table"),
            dcc.Tab(label="Histogram", value="histogram"),
        ],
    ),
    # ---------------------------------------- #
    # Contents
    html.Div(id="tabs-content"),

])

@callback(
    Output("tabs-content", "children"),
    Input("tab", "value")
)
def main_callback_logic(tab):
    dff = df.copy()

    if tab == "table":
        fig = dash_table.DataTable(
            data=dff.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            }
        )
    if tab == "histogram": 
        hist = px.histogram(dff, x='pf_r')
        fig = dcc.Graph(figure=hist)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)