from random import random, randint


class Edge:
    def __init__(self, destination):
        self.destination = destination


class Vertex:
    def __init__(self, value, **pos):  # TODO: Test default args
        self.value = value
        self.color = 'white'
        self.pos = pos
        self.edges = []


class Graph:
    def __init__(self):
        self.vertexes = []

    def debug_create_test_data(self):
        debug_vertex_1 = Vertex('t1', x=40, y=40)
        debug_vertex_2 = Vertex('t2', x=140, y=140)
        debug_vertex_3 = Vertex('t3', x=300, y=400)
        debug_vertex_4 = Vertex('t4', x=400, y=450)
        debug_vertex_5 = Vertex('t5', x=340, y=350)

        debug_edge_1 = Edge(debug_vertex_2)
        debug_vertex_1.edges.append(debug_edge_1)

        debug_edge_2 = Edge(debug_vertex_3)
        debug_vertex_2.edges.append(debug_edge_2)

        debug_edge_3 = Edge(debug_vertex_4)
        debug_vertex_3.edges.append(debug_edge_3)

        debug_edge_4 = Edge(debug_vertex_5)
        debug_vertex_4.edges.append(debug_edge_4)

        self.vertexes.extend(
            [debug_vertex_1, debug_vertex_2, debug_vertex_3, debug_vertex_4, debug_vertex_5])

    def bfs(self, start):
        print('called bfs')
        random_color = "rgb({0},{1},{2})".format(randint(
            0, 255), randint(0, 255), randint(0, 255))

        queue = []
        found = []

        queue.append(start)
        found.append(start)

        start.color = random_color

        print('about to start while')
        while len(queue) > 0:
            v = queue[0]
            for edge in v.edges:
                if edge.destination not in found:
                    found.append(edge.destination)
                    queue.append(edge.destination)
                    edge.destination.color = random_color
            queue.pop(0)  # TODO: Look at collections.dequeue

        # print('about to return')
        # return found

    # create a random graph
    def randomize(self, width, height, pxBox, probability=0.6):
        # helper function to set up two way edges
        def connectVerts(v0, v1):
            v0.edges.append(Edge(v1))
            v1.edges.append(Edge(v0))

        count = 0

        # build a grid of verts
        grid = []
        for i in range(height):
            row = []
            for j in range(width):
                count += 1
                valString = "v%s" % (count)
                v = Vertex(valString, x=0, y=0)
                row.append(v)
            grid.append(row)

        # go through the grid randomly hooking up edges
        for y in range(height):
            for x in range(width):
                # connect down
                if y < height - 1:
                    if random() < probability:
                        connectVerts(grid[y][x], grid[y + 1][x])

                # connect right
                if x < width - 1:
                    if random() < probability:
                        connectVerts(grid[y][x], grid[y][x + 1])

        # last pass, set the x and y coordinates for drawing
        boxBuffer = 0.8
        boxInner = pxBox * boxBuffer
        boxInnerOffset = (pxBox - boxInner) / 2

        for y in range(height):
            for x in range(width):
                grid[y][x].pos['x'] = x * pxBox + \
                    boxInnerOffset + random() * boxInner
                grid[y][x].pos['y'] = y * pxBox + \
                    boxInnerOffset + random() * boxInner

        # finally, add everything in our grid to the vertexes in this Graph
        for y in range(height):
            for x in range(width):
                self.vertexes.append(grid[y][x])
