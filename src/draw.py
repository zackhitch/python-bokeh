import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, ColumnDataSource, Range1d, LabelSet, Label
from bokeh.palettes import Spectral8

from graph import *

WIDTH = 500
HEIGHT = 500  # TODO: currently graph renders to scale, scaled to numbers here. https://stackoverflow.com/questions/21980662/how-to-change-size-of-bokeh-figure
CIRCLE_SIZE = 30

graph_data = Graph()
# graph_data.debug_create_test_data()
graph_data.randomize(5, 4, 150, 0.6)
# print(graph_data.vertexes)
graph_data.bfs(graph_data.vertexes[0])

N = len(graph_data.vertexes)
node_indices = list(range(N))

color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)

plot = figure(title='Graph Layout Demonstration', x_range=(0, WIDTH), y_range=(0, HEIGHT),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Circle(size=CIRCLE_SIZE, fill_color='color')

start_points, end_points = [], []

for start_point, vert in enumerate(graph_data.vertexes):
    for edge in vert.edges:
        start_points.append(start_point)
        end_points.append(graph_data.vertexes.index(edge.destination))

# this is drawing the edges from start to end
#
graph.edge_renderer.data_source.data = dict(
    # this is a list of some kind that has to do with starting points
    start=start_points,
    end=end_points)  # this is a lst of some kind that has to do with ending points
print(graph.edge_renderer.data_source.data)


# start of layout cde
# Looks like this is setting the positions of the vertexes
x = [v.pos['x'] for v in graph_data.vertexes]
y = [v.pos['y'] for v in graph_data.vertexes]

print(y)

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)


# Create a new dictionary to use as a data source, with three lists in it, ordered in the same
# way as vertexes
# List of x values
# List of y values
# List of labels

value = [v.value for v in graph_data.vertexes]  # TODO: possible optimization

label_source = ColumnDataSource(data=dict(x=x, y=y, v=value))


labels = LabelSet(x='x', y='y', text='v', level='overlay',
                  source=label_source, render_mode='canvas', text_align='center', text_baseline='middle')


# TODO: Investigate plot.add_layout vs. plot.renderers.append
plot.add_layout(labels)


output_file('graph.html')
show(plot)
