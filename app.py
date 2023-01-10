from dash import Dash, dash_table, dcc, html
import pandas as pd
from collections import OrderedDict
from read_data import df

dim = df.shape[0]

app = Dash(__name__)

app.layout = html.Div([
    html.H1(f'{dim} records'),
    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            'whiteSpace': 'normal'
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)