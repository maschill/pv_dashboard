import dash
from flask import Flask
import dash_core_components as doc
import dash_html_components as html
import numpy as np 
import plotly.graph_objs as go


server = Flask(__name__)
app = dash.Dash(__name__, server=server)

np.random.seed(101)
random_x = np.random.randint(1,21,20)
random_y = np.random.randint(1,21,20)

app.layout=html.Div(children=[
    html.H1('Hello World'),
    
    doc.Graph(
        id='scatter',
        figure={
            'data': [
                go.Scatter(
                    x=random_x,
                    y=random_y,
                    mode='markers'
                )
            ],
            'layout': go.Layout(
                title = 'Here is My Scatter Plot',
                xaxis = {'title': 'Here is My X-Axis'},
                yaxis = {'title': 'Here is My Y-Axis'}
            )
        }
    )
    ])



if __name__=="__main__":
    app.run_server()