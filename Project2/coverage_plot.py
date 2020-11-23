from preprocess_data import PreprocessData
from coverage_figure import CoverageFigure
import plotly.graph_objects as go
import numpy as np
import datetime

def create_trace_fxd(fxd_data):
    trace = []
    print("Creating Slice Fixation Trace")
    end_time = max(fxd_data['time'])

    
    trace.append(
                    go.Scattergl(
                        name = 'Total Fixation',
                        visible=False,
                        hoverinfo='none',
                        x=fxd_data['x'],
                        y=fxd_data['y'],
                        mode='markers',
                        marker=dict(
                            opacity=0.20,
                            color='white',
                            size=fxd_data['duration'] / 4,
                            line=dict(width=0)
                        )
                    )
                )

    for initial_time in np.arange(0, end_time, TIMESTEP):
        final_time = initial_time + TIMESTEP
        fxd_subset = fxd_data[fxd_data['time'].between(initial_time, final_time)]

        start_time = datetime.datetime.fromtimestamp(initial_time / 1000).strftime("%M:%S")
        end_time = datetime.datetime.fromtimestamp(final_time / 1000).strftime("%M:%S")
        trace.append(
            go.Scattergl(
                name = start_time + '-' + end_time,
                visible = False,
                #hoverinfo = 'none',
                x = fxd_subset['x'],
                y = fxd_subset['y'],
                #mode = 'lines+markers',
                mode = 'markers+lines',
                marker = dict(
                    #opacity = 1.0,
                    color = 'limegreen',
                    #color = 'black',
                    line = dict(
                        color = 'limegreen',
                        width = 1
                    ),
                    size = fxd_subset['duration']/4,
                    #size = 25
                ),
                
                line = dict(
                    #color = '#708090',
                    color = 'red',
                    width = 2
                ),
                text=fxd_subset['duration'],
                hoverinfo='text',
                hovertemplate="<b> Duration: %{text}ms</b><extra></extra>",
            )
        )

    return trace
                
def create_sliders(fxd_data):
    steps = []
    end_time = max(fxd_data['time'])
    data_len = end_time // TIMESTEP + (end_time % TIMESTEP > 0) + 1

    for i in range(data_len):
        step = dict(
            method='restyle',
            args=['visible', [False] * data_len],
            label=datetime.datetime.fromtimestamp(TIMESTEP * i / 1000).strftime("%M:%S"),
        )

        for j in range(i - 1, i):
            if j >= 0:
                step['args'][1][j + 1] = True

        step['args'][1][0] = True
        steps.append(step)

    sliders = [dict(
        active=0,
        steps=steps,
        currentvalue={'prefix': 'Time: '},
        pad={'t': 50},
        font=dict(size=15)
    )]

    return sliders

def create_heatmap(fxd_data):
    print("creating heatmap")
    img = Image.open(data.filepath + data.graph_or_tree + ".png")
    img = resize((1600,1200), img)
    img = img.convert('RGBA')
    pixels = np.array(img)


    zList = [[0 for x in range(1600)] for y in range(1200)]

    for index, row in fxd_data.iterrows():
        cx = row['x']
        cy = row['y']
        z = row['duration']
        r = 25
        for x in range(cx-r, cx+r):
            for y in range(cy-r, cy+r):
                d = math.sqrt((cx-x) ** 2 + (cy-y)**2)
                if d<=r and zList[y][x] < 1000:
                    xList[y][x] = zList[y][x] + float(z)


    blurred = gaussian_filter(zList, sigma=25)

    min = 0
    max = np.amax(blurred)
    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            pixels[i][j][3] = normalize(min, max, blurred[i][j])


    img = Image.fromarray(pixels)
    img.save(data.filepath + "New" + data.graph_or_tree + ".png")


if __name__ == '__main__':
    TIMESTEP = 10000

    WIDTH = 1600
    HEIGHT = 1200

    graph_data = PreprocessData("", "graph")
    tree_data = PreprocessData("", "tree")

    trace_fxd = []
    trace_fxd.append(create_trace_fxd(graph_data.fixation_data()))

    trace_sliders = []
    trace_sliders.append(create_sliders(graph_data.fixation_data()))

    # trace_updatemenus = []
    # trace.updatemenus.append(create_heatmap(graph_data.fixation_data()))
    
    
    trace_fxd2 = []
    trace_fxd2.append(create_trace_fxd(tree_data.fixation_data()))

    trace_sliders2 = []
    trace_sliders2.append(create_sliders(tree_data.fixation_data()))

    figure = CoverageFigure()
    figure.initialize_layout()
    #for trace in trace_fxd:
    figure.update_data(trace_fxd[0])
    #for trace_s in trace_sliders:
    figure.update_layout(trace_sliders[0])
    figure.show()
    
    figure2 = CoverageFigure()
    figure2.initialize_layout2()
    #for trace in trace_fxd:
    figure2.update_data(trace_fxd2[0])
    #for trace_s in trace_sliders:
    figure2.update_layout(trace_sliders2[0])
    figure2.show()
    
    # In order to reset traces, set fig.data = []
    
    # In order to reset traces, set fig.data = []