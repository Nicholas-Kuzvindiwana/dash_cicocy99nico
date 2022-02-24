from ast import Return
from sre_parse import State
#from tkinter.tix import CheckList
from click import option
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from plotly import graph_objects as go

#FOR IMPORTING JSON file
import urllib.request
import json


url="http://127.0.0.1:5000/cicosy"
df = pd.read_json(url)
dff=df.groupby('OrderDate',as_index=False)[['Sales','Revenue','Quantity','Profit']].sum()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server= app.server
PLOTLY_LOGO='logo.png' 

app.layout=dbc.Container([
    dbc.Row ([
        dbc.Col(html.H1(
            dbc.Badge(
                "CICOSY SALES DASHBOARD",
                color="white",
                 className='text-center text-primary mb-4')
                         
            )      
        )
        
    ]),

    dbc.Row([
        dbc.Col([
            html.P(
                dbc.Badge(
                    "Select ",
                    pill=True,
                    color="primary",
                    className="me-4",
                )
            ),
            dcc.Dropdown(
                id='names',
                value='Region',
                multi=False,
                 options=[{'value': x, 'label': x} 
                         for x in ['Category', 'Region', 'Ship Mode','Sub-Category']],
            ),
            

            
            dcc.Graph(id='line-fig',figure={},clickData=None, hoverData=None)           
                                  
         
        ],width={'size':4}) ,
        dbc.Col([
            html.P(
                dbc.Badge(
                   "Sales value",
                   color="white",
                   text_color="primary",
                   className="border me-6",
                )
            ), 
            dcc.Dropdown(
                id='Revenue',
                value='Revenue',
                multi=False,
                options=[{'value': x, 'label': x} 
                         for x in ['Quantity', 'Profit', 'Revenue', 'Sales']],
            ),
            dcc.Graph(id='pie-chart', figure={}),
            

        ],width={'size':4, 'offset':0, 'order':2}),

        dbc.Col([
             dbc.DropdownMenu(
            label="export to",
            size="lg",
            children=[dbc.Badge("PDF",color="White",text_color="primary",pill=True,className="border me-6"),
                     dbc.Badge("PRINT",color="White",text_color="primary",pill=True,className="border me-6"),
                     dbc.Badge("E-MAIL",color="White",text_color="primary",pill=True,className="border me-6")],

            className="mb-3"),dcc.Graph(id="liner-chart"),
        ],width={'size':3, 'offset':0, 'order':3}),

        
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='Values',
                value='Revenue',
                multi=False,
                options=[{'value': x, 'label': x} 
                         for x in ['Quantity', 'Profit', 'Revenue', 'Sales']],
            ),dcc.Graph(id='time-series', figure={}),

        ],width={'size':6})
         
        
    

    ])
],fluid=True,)

##Connecting the components
@app.callback(
    Output('line-fig','figure'),
    [Input('names','value'),
    Input('Revenue','value')]
)
def update_graph(names,Revenue):
    fig=px.bar(df,x=names,y=Revenue, title="bar charts",hover_data=[Revenue, names], color=Revenue)
    return fig
    
@app.callback(
    Output("pie-chart", "figure"),
    [Input("names", "value"), 
    Input("Revenue", "value")]
)

def generate_chart(names, Revenue):
   fig2 = px.pie(df, values=Revenue, names=names,color_discrete_sequence=px.colors.sequential.RdBu, hole=.2 )
   return fig2
@app.callback(
    Output("time-series", "figure"),
    [Input('Values', "value")]
)
def display_time_series(Revenue):
    fig3 = px.line(dff, x='OrderDate', y=Revenue)
    return fig3

@app.callback(
    Output("liner-chart", "figure"), 
     [Input('names','value'),
    Input('Revenue','value')])
def update_line_chart(names, Revenue):
    fig4 =px.violin(df, x=names, y=Revenue,)
    return fig4






if __name__=='__main__':
    app.run_server(debug=True, port=8000)
