import dash
from flask import Flask
import dash_core_components as doc
import dash_html_components as html
import numpy as np 
import plotly.graph_objs as go

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

consumption_x = np.arange(24)
consumption_y = np.array([2,1,1,0,0,0,1,4,4,3,3,7,8,5,3,2,1,2,6,6,3,3,2,2])*2
production_x = np.arange(24)
production_y = np.array([0,0,0,0,0,0,0,0.9,3.5,7.4,12.3,16.4,18.6,19.2,18.4,15.8,11.7,6.7,2.3,0.2,0,0,0,0])
assert(len(consumption_x)==len(consumption_y))
assert(len(production_x)==len(production_y))

app.layout=html.Div(children=[
  
    doc.Graph(
        id='scatter',
        figure={
            'data': [
                go.Scatter(
                    x=consumption_x,
                    y=consumption_y,
                    fill='tozeroy',
                    name='Verbrauch'
                ),
                go.Scatter(
                    x=production_x,
                    y=production_y,
                    fill='tonexty',
                    name='PV Erzeugung'
                ),
            ],
            'layout': go.Layout(
                title = 'Dummy Verbrauch-Erzeugungs-Plot',
                xaxis = {'title': 'Uhrzeit'},
                yaxis = {'title': 'kW'}
            )
        }
    )
    ])



if __name__=="__main__":
    app.run_server(port=1337)