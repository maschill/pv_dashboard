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
assert(len(consumption_x)==len(consumption_y))
days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
food = ["Spargel-Eiersalat", "Pizza", "Nudelsalat", 'Ofengemüse', 'Uhl Bestellen', 'Reissalat', 'Bananenbrot']

#read db config from db_config.txt
connection = None
with open('src/db_config.txt', 'r') as fo:
    connection = fo.read().strip()

engine = create_engine(connection)
data = [[x,y] for x,y in engine.execute("""SELECT uhrzeit AT TIME ZONE 'Europe/Berlin', wechselstrom_leistung FROM messdaten WHERE wechselrichter_id=4;""")]
t = [d[0] for d in data]
p = [max(d[1]/100.0,0) for d in data]
consumption_y = [0]*(len(t))

app.title = 'Photovoltaik Dashboard'
app.layout=html.Div(children=[
        doc.Graph(
            id='scatter',
            figure={
                'data': [
                    go.Scatter(
                        x=t,
                        y=consumption_y,
                        fill='tozeroy',
                        name='Verbrauch Beispiel'
                    ),
                    go.Scatter(
                        x=t,
                        y=p,
                        fill='tonexty',
                        name='PV Erzeugung'
                    ),
                ],
                'layout': go.Layout(
                    title = 'Dummy Verbrauch-Erzeugungs-Plot',
                    xaxis = {'title': 'Uhrzeit'},
                    yaxis = {'title': 'kWh', 'range':[0,40]}
                )
            }
        ),
        html.Div(children=[
            dash_table.DataTable(
                id = "essen",
                columns = [{"name":i, "id":i} for i in days],
                data = [{k:v for k,v in zip(days,food)}]
            )
        ]),
        doc.Graph(
            id = "updated_graph"),
        doc.Interval(
            id = 'graph_update',
            interval = 1*150000,
            n_intervals = 0
        )
    ])

@app.callback(Output('updated_graph', 'figure'), 
            [Input('graph_update', 'n_intervals')])
def update_graph(n):
    #read db config from db_config.txt
    connection = None
    with open('src/db_config.txt', 'r') as fo:
        connection = fo.read().strip()

    engine = create_engine(connection)
    query = """
        SELECT
            uhrzeit AT TIME ZONE 'Europe/Berlin', SUM(wechselstrom_leistung)
        FROM
            messdaten
        WHERE
            uhrzeit >= (now() - interval '2 days')
        GROUP BY
            uhrzeit
        ORDER BY
            uhrzeit;
    """
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
        xaxis = {'title': 'Uhrzeit'},
        yaxis = {'title': 'kWh', "range":[0,40]}
    )

    return {"data":data , "layout": layout}

if __name__=="__main__":
    app.run_server(port=1337, host="0.0.0.0")
