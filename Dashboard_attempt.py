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
        showticklabels=False
        tickvals=[]
       # ticktext=[(datetime(2003, 1, 1) + timedelta(days=30 * (x - 1))).strftime('%B %Y') for x in range(FIRST, LAST + 1)]
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

fig.show()





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
















####Deleted code####

start_date = datetime(2003, 1, 1)
end_date = datetime(2021, 12, 31)
num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1

start_date = datetime(2003, 1, 1)
end_date = datetime(2021, 12, 31)
num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1








# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])

if __name__ == '__main__':
    app.run_server(host='localhost',port=8005)




from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Hello World')
])
if __name__ == '__main__':
    app.run_server(host='localhost',port=8005)



# Run the app
if __name__ == '__main__':
    app.run(debug=True)



cmap = ListedColormap([
    '#08306b', '#08519c', '#2171b5', '#4292c6',
    '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
    '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a',
    '#ef3b2c', '#cb181d', '#a50f15', '#67000d',
])

fig = plt.figure(figsize=(10, 1))

ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()

col = PatchCollection([
    Rectangle((y, 0), 1, 1)
    for y in range(FIRST, LAST + 1)
])

# set data, colormap and color limits

col.set_array(ch4)
col.set_cmap(cmap)
col.set_clim(reference - LIM, reference + LIM)
ax.add_collection(col)

ax.set_ylim(0, 1)
ax.set_xlim(FIRST, LAST + 1)

#fig.savefig('C:/Users/bengo/OneDrive/Documents/GitHub/Climate_Coders/results/warming-stripes_plotly.png')

fig = py.plot_mpl(fig, filename="my first plotly plot")





