from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd

import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

#import cdstoolbox as ct
#import chart_studio.plotly as py

import chart_studio.plotly as py


##### Figure #####


df = pd.read_csv('https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/monthly_data.csv' )

#df2 = pd.read_fwf(
#    'C:/Users/bengo/OneDrive - Nexus365/ffs.txt',
#    index_col=0,
#    usecols=(0, 1),
#    names=['year', 'anomaly'],
#    header=None,
#)


df = df.dropna()

df = df[['date', 'ch4']]
df = df.groupby(['date']).mean()

#df[['ch4']] = df[['ch4']]*100000

df = df.assign(row_number=range(len(df)))




FIRST = 0
LAST = 226  # inclusive


# Reference period for the center of the color scale

FIRST_REFERENCE = 0
LAST_REFERENCE = 226
LIM = 0.01 # degrees

df = df.set_index('row_number')

ch4 = df.loc[FIRST:LAST, 'ch4'].dropna()
reference = ch4.loc[FIRST_REFERENCE:LAST_REFERENCE].mean()


df = df[[ 'ch4']]



fig = go.Figure()

fig.update_layout(
    width=800,
    height=350,
    xaxis=dict(
        title='Monthly Methane Levels',
        range=[FIRST, LAST + 1],
        showgrid=False,
        zeroline=False,
        showticklabels=True,
        tickmode='array',
        showticklabels=False,
        tickvals=[]
    ),
    yaxis=dict(
        range=[0, 1],
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        tickvals=[]
    )
)


x_values = np.arange(FIRST, LAST + 1)
y_values = np.zeros_like(x_values)
z_values = np.array(ch4)

fig.add_trace(
    go.Heatmap(
        x=x_values,
        y=y_values,
        z=z_values,
        colorscale='rdbu_r',
        showscale=False
    )
)

fig.add_trace(
    go.Heatmap(
        x=x_values,
        y=y_values,
        z=z_values,
        colorscale='rdbu_r',
        showscale=False,
        hovertemplate='Month: %{text}<br>Methane Levels: %{z}<extra></extra>',
        text=[(datetime(2003, 1, 1) + timedelta(days=30 * (x - 1))).strftime('%B %Y') for x in range(FIRST, LAST + 1)]
    )
)






####Dashboard####
app = Dash(__name__)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}


app.layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Methane Map', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Methane Graph', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Health Map', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Health Graph', value='tab-4', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

@callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Map of Methane Levels, overlayed with energy plant and hospital locations')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Methane data visualisations'),
                dcc.Graph( id='Methane Stripes', figure=fig)
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Map of Mortalities from respiratory diseases and gas leaks')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Health data visualisations')
        ])



if __name__ == '__main__':
    app.run_server(host='localhost',port=8005)














