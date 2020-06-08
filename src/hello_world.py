#encoding: utf-8
import dash
from flask import Flask
import dash_core_components as doc
import dash_html_components as html
import dash_table
import numpy as np 
import plotly.graph_objs as go
from db_schemes import Messdaten
from sqlalchemy import create_engine, func, desc
from datetime import datetime, timedelta
from dash.dependencies import Output, Input
from sqlalchemy.orm import Session


server = Flask(__name__)
app = dash.Dash(__name__, server=server)

consumption_x = np.arange(24)
consumption_y = np.array([2,1,1,0,0,0,1,4,4,3,3,7,8,5,3,2,1,2,6,6,3,3,2,2])*4
production_x = np.arange(24)
production_y = np.array([0,0,0,0,0,0,0,0.9,3.5,7.4,12.3,16.4,18.6,19.2,18.4,15.8,11.7,6.7,2.3,0.2,0,0,0,0])
assert(len(consumption_x)==len(consumption_y))
assert(len(production_x)==len(production_y))
days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
food = ["Spargel-Eiersalat", "Pizza", "Nudelsalat", 'Ofengemüse', 'Uhl Bestellen', 'Reissalat', 'Bananenbrot']

#read db config from db_config.txt
connection = None
with open('src/db_config.txt', 'r') as fo:
    connection = fo.read().strip()

# engine = create_engine(connection)
# data = [[x,y] for x,y in engine.execute('SELECT uhrzeit, wechselstrom_leistung FROM messdaten WHERE wechselrichter_id=4')]
data = [[0,0] for _ in range(25)]
t = [d[0] for d in data]
p = [max(d[1]/100.0,0) for d in data]
consumption_y = [xx for xx in consumption_y] + [0]*(len(p)-24)

app.title = 'Photovoltaik Dashboard'
app.layout=html.Div(children=[
        html.Div([
            doc.Graph(
                id = "updated_graph"),
            doc.Interval(
                id = 'graph_update',
                interval = 3600000,
                n_intervals = 0
                )
        ]),
        html.Div(children=[
            dash_table.DataTable(
                id = "essen",
                columns = [{"name":i, "id":i} for i in days],
                data = [{k:v for k,v in zip(days,food)}]
            )
        ]),
    ])

@app.callback(Output('updated_graph', 'figure'), 
            [Input('graph_update', 'n_intervals')])
def update_graph(n):
    #read db config from db_config.txt
    connection = None
    with open('src/db_config.txt', 'r') as fo:
        connection = fo.read().strip()

    engine = create_engine(connection)
    query = "SELECT uhrzeit, SUM(wechselstrom_leistung) FROM messdaten WHERE uhrzeit >= TO_TIMESTAMP('" 
    base_time = datetime.now() - timedelta(365,0,0,0,0,0)
    query = query + base_time.strftime("%Y-%m-%d %H:%M:%S") + "', 'YYYY-MM-DD HH24:MI:SS') GROUP BY uhrzeit ORDER BY uhrzeit;" 
    print(query)

    data = [[x,y] for x,y in engine.execute(query)]
    t = [d[0] for d in data]
    p = [max(d[1]/100.0,0) for d in data]

    data = [go.Scatter(
        x = t,
        y = p,
        name = "production"
    )]

    layout = go.Layout(
        title = 'Selbst Aktualisierender Plot',
        xaxis = {
            "title":"Zeit",
            "rangeselector":{
                "buttons":[
                    {"count":2, "label":"2 Tage", "step":"day", "stepmode":"backward"},
                    {"count":7, "label":"7 Tage", "step":"day", "stepmode":"backward"},
                    {"count":1, "label":"1 Monat", "step":"month", "stepmode":"backward"},
                    {"count":1, "label":"1 Jahr", "step":"year", "stepmode":"backward"},
                    {"step":"all"}
                ]
            },
            "rangeslider" : {"visible":True},
            "type":"date"
        },
        yaxis = {'title': 'kWh', "range":[0,40]},
    )


    return {"data":data , "layout": layout}


if __name__=="__main__":
    app.run_server(port=1337, host="0.0.0.0")
