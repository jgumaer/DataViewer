import dash
from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px

df = pd.read_csv("hard_fix_feb_7.csv")
states = df.State.unique().tolist()

df_graph = df.copy()
df_graph['Date'] = pd.to_datetime(df_graph['Year'].astype(str)  + df_graph['Month'], format='%Y%B')

fig = px.line(df_graph, x='Date', y='Total Disconnections', color='Utility Name')
fig.update_xaxes(rangeslider_visible=True)

app = dash.Dash(__name__)

app.layout = dbc.Container([
    dcc.Markdown('# Data Viewer Example', style={'textAlign':'center'}),
    dbc.Col([state_drop := dcc.Dropdown([x for x in sorted(df.State.unique())],
                                       placeholder='Select State',
                                       multi=False),
             utility_drop := dcc.Dropdown([x for x in sorted(df['Utility Name'].unique())],
                                         placeholder='Select Utility Provider',
                                          style={'display': 'block'},
                                         multi=True),
             year_drop := dcc.Dropdown([x for x in sorted(df.Year.unique())],
                                       multi=True,
                                       placeholder='Select Year',
                                      style={'display': 'none'})
            
            ]),
    time_series_chart := dcc.Graph(figure=fig),
    my_table := dash_table.DataTable(data=df.to_dict('records')),
    
    ])

@app.callback(
    Output(utility_drop, 'options'),
    Output(utility_drop, 'style'),
    Input(state_drop, 'value')
)
def change_utility_drop(state_v):
    
    if state_v:
        df_state = df.copy()
        df_state = df_state[df_state['State'].isin([state_v])]
        
        return df_state['Utility Name'].unique(), {'display': 'block'}
    
    else:
        return df['Utility Name'].unique(), {'display': 'block'}


@app.callback(
    Output(my_table,"data"),
    Input(state_drop, "value"),
    Input(utility_drop, "value"),
    Input(year_drop, "value")
)
def update_table(state_v, utility_v, year_v):
    dff = df.copy()
    
    if state_v:
        dff = dff[dff.State.isin([state_v])]
        
    if utility_v:
        dff = dff[dff['Utility Name'].isin(utility_v)]
        
    if year_v:
        dff = dff[dff.Year.isin(year_v)]
        
    return dff.to_dict('records')

@app.callback(
    Output(time_series_chart,"figure"),
    #Output(time_series_chart, "style"),
    Input(state_drop, "value"),
    Input(utility_drop, "value"),
    Input(year_drop, "value")
)
def update_graph(state_v, utility_v, year_v):
    dff_graph = df_graph.copy()
    
    if state_v:
        dff_graph = dff_graph[dff_graph.State.isin([state_v])]
        
    if utility_v:
        dff_graph = dff_graph[dff_graph['Utility Name'].isin(utility_v)]
        
    if year_v:
        dff_graph = dff_graph[dff_graph.Year.isin(year_v)]
        
    fig_update = px.line(dff_graph, x='Date', y='Total Disconnections', color='Utility Name')
    fig_update.update_xaxes(rangeslider_visible=True)
    
    return fig_update    


if __name__ == "__main__":
    app.run_server(debug=True)