import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8

from graph import *

graph_data = Graph()
graph_data.debug_create_test_data()
print(graph_data.vertexes)

N = len(graph_data.vertexes)
node_indices = list(range(N))

color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)

plot = figure(title='Graph Layout Demonstration', x_range=(0, 500), y_range=(0, 500),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Oval(height=30, width=30, fill_color='color')

start_points, end_points = [], []
for vert in graph_data.vertexes:
    for edge in vert.edges:
        start_points.append(graph_data.vertexes.index(vert))
        end_points.append(graph_data.vertexes.index(edge.destination))

# this is drawing the edges from start to end
#
graph.edge_renderer.data_source.data = dict(
    # start=[0]*N,  # this is a list of some kind that has to do with starting points
    start=start_points,
    end=end_points)  # this is a lst of some kind that has to do with ending points
print(graph.edge_renderer.data_source.data)


# start of layout cde
# circ = [i*2*math.pi/N for i in node_indices]
# Looks liek this is setting the positions of the vertexes
# x = [math.cos(i) for i in circ]
x = [v.pos['x'] for v in graph_data.vertexes]
# y = [math.sin(i) for i in circ]
y = [v.pos['y'] for v in graph_data.vertexes]

print(y)

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)

output_file('graph.html')
show(plot)
