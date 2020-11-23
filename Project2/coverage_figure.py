from PIL import Image
import plotly.graph_objects as go
import plotly.offline as py

class CoverageFigure:
    def __init__(self):
        self.figure = go.Figure()

    def initialize_layout(self):
        self.figure.update_layout(
            title = go.layout.Title(
                text = 'Data Viz - Eye Tracking',
                xref = 'paper',
                x = 0
            ),
            width = 1600,
            height = 1200,

            images = [dict(
                source = Image.open('Graph.png'),
                opacity = 0.25,
                xref = 'x',
                yref = 'y',
                x = 0,
                y = 0,
                sizex = 1600,
                sizey = 1200,
                sizing = 'stretch',
            )],

            shapes=[
                go.layout.Shape(
                    type="rect",
                    x0=0,
                    y0=0,
                    x1=1600,
                    y1=1200,
                    fillcolor='black',
                    layer='below'
                )
            ],

            xaxis=dict(
                showline=True,
                showgrid = False,
                mirror=True,
                #tickfont = dict(size = 30),
                linewidth=2,
                linecolor='black',
                #gridcolor='#000000',
                range=[0, 1600],
                tickvals = []
                #tickvals=[k*200+100 for k in range(0, 8)],
                #ticktext=['1', '2', '3', '4', '5', '6', '7', '8', '9']

            ),
            yaxis=dict(
                showline=True,
                showgrid = False,
                mirror=True,
                #tickfont = dict(size = 30),
                linewidth=2,
                linecolor='black',
                #gridcolor='#000000',
                range=[1200, 0],
                tickvals = []
                #tickvals=[k*200+100 for k in range(0, 6)],
                #ticktext=['A', 'B', 'C', 'D', 'E', 'F', 'G']
            )
        )
    def initialize_layout2(self):
        self.figure.update_layout(
            title = go.layout.Title(
                text = 'Data Viz - Eye Tracking',
                xref = 'paper',
                x = 0
            ),
            width = 1600,
            height = 1200,

            images = [dict(
                source = Image.open('Tree.png'),
                opacity = 0.25,
                xref = 'x',
                yref = 'y',
                x = 0,
                y = 0,
                sizex = 1600,
                sizey = 1200,
                sizing = 'stretch',
            )],

            shapes=[
                go.layout.Shape(
                    type="rect",
                    x0=0,
                    y0=0,
                    x1=1600,
                    y1=1200,
                    fillcolor='black',
                    layer='below'
                )
            ],

            xaxis=dict(
                showline=True,
                showgrid = False,
                mirror=True,
                #tickfont = dict(size = 30),
                linewidth=2,
                linecolor='black',
                #gridcolor='#000000',
                range=[0, 1600],
                tickvals = []
                #tickvals=[k*200+100 for k in range(0, 8)],
                #ticktext=['1', '2', '3', '4', '5', '6', '7', '8', '9']

            ),
            yaxis=dict(
                showline=True,
                showgrid = False,
                mirror=True,
                #tickfont = dict(size = 30),
                linewidth=2,
                linecolor='black',
                #gridcolor='#000000',
                range=[1200, 0],
                tickvals = []
                #tickvals=[k*200+100 for k in range(0, 6)],
                #ticktext=['A', 'B', 'C', 'D', 'E', 'F', 'G']
            )
        )

    def update_data(self, data):
        self.figure.data = None

        #iter_data = iter(data)
        #next(iter_data)
        for trace in data:
            self.figure.add_trace(trace)

    def update_layout(self, sliders):
        self.figure.data[0].visible = True

        self.figure.update_layout(
            sliders=sliders,
            showlegend = True
        )

    def show(self):
        py.plot(self.figure, filename='plotlysample.html')