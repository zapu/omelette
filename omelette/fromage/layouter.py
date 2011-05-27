import math
import random

class Layout(object):

    def __init__(self, diagram):
        self.diagram = diagram

    def apply(self):
        raise NotImplemented

    def _max_size_of_drawable_node(self, nodes):
        """
        Function calculating maximal size of nodes in given list of nodes
        """
        maxwidth = maxheight = 0
        for node in nodes:
            if maxwidth < node.boundingRect().size().width():
                maxwidth = node.boundingRect().size().width()
            if maxheight < node.boundingRect().size().height():
                maxheight = node.boundingRect().size().height()
        return max(maxwidth, maxheight)

class LayoutFactory(object):

    __layouts = { "circular layout" : (lambda diagram : CircularLayout(diagram)),
            "springs layout" : (lambda diagram : SpringLayout(diagram)),
            "neato layout" : (lambda diagram : GraphvizLayout(diagram, 'neato',
                2.5)),
            "dot layout" : (lambda diagram : GraphvizLayout(diagram, 'dot', 1.0/30)),
            "fdp layout" : (lambda diagram : GraphvizLayout(diagram, 'fdp')),
            "sfdp layout" : (lambda diagram : GraphvizLayout(diagram, 'sfdp', 4)),
            "twopi layout" : (lambda diagram : GraphvizLayout(diagram, 'twopi')),
            "circo layout" : (lambda diagram : GraphvizLayout(diagram, 'circo',
                1.0/30))}

    def __init__(self, diagram):
        self.diagram = diagram

    def layouts(self):
        return LayoutFactory.layouts.keys()

    def get(self, layout):
        return LayoutFactory.__layouts[layout](self.diagram)
            

class CircularLayout(Layout):

    def apply(self, sx=0, sy=0, start=math.pi/2, spread=2):
        """
        Basic layout function placing all nodes on circle, adjusting
        circle range to size of nodes.
        sx, sy are the coordinates of centre of circle
        start is a start angle for counting angles
        spread is a spread factor
        """
        r = 0
        # Finding max size of drawable
        maxsize = self._max_size_of_drawable_node(self.diagram.nodes.values())
        n = len(self.diagram.nodes) # number of drawables
        if n > 1:
            angle = 2 * math.pi / n # calculating angle step
            if angle % math.pi == 0:
                r = spread * maxsize
            else:
                r = (spread * maxsize
                    / math.sin( angle ))
            # shifting coordinates to be positive
            sx = r + maxsize - sx
            sy = r + maxsize - sy
            sortednodes = self.__sort_nodes_by_neighbourhood(self.diagram.nodes.values())
            i = 0
            for node in sortednodes:
                # calculating xpos
                x = sx + r * math.sin(start + angle * i)
                # calculating ypos
                y = sy + r * math.cos(start + angle * i)
                i += 1
                node.moveBy(x, y)
        else:
            node.moveBy(sx, sy)
        return True

    def __sort_nodes_by_degree(self, nodes, rev=True):
        """
        Function sorting nodes in order of vertex grade
        """
        return sorted(nodes, key=self.__node_degree, reverse=rev)

    def __sort_nodes_by_neighbourhood(self, nodes):
        """
        Function sorting nodes to have their neighbours on their both sides
        """
        sortednodes = []
        d = 0 # number of sorted nodes
        while d < len(nodes):
            for node in nodes:
                if not node in sortednodes:
                    sortednodes.append(node)
                    d += 1
                    for node in sortednodes:
                        i = 0 # sorted neighbours counter
                        for neigh in node.neighbours:
                            if not neigh in sortednodes:
                                # neighbour is placed on the right or on the left of node
                                sortednodes.insert(sortednodes.index(node) + pow(-1,i), neigh)
                                d += 1
                                i += 1
        return sortednodes

    def __node_degree(self, node):
        """
        Function calculating node's degree
        """
        return len(node.neighbours)

class SpringLayout(Layout):

    def apply(self, c1=1, c2=1, c3=1, c4=0.1, m=100):
        """
        Layout function using mechanical model of spring embedder.
        c1 is the attraction direct factor
        c2 is the attraction inverted factor
        c3 is the repel factor
        c4 is the force factor
        m is the number of iterations
        """
        # Moving all nodes in random positions
        maxrand = 100 # range of random numbers
        for node in self.diagram.nodes.values():
            node.setPos(random.random() * maxrand,
                        random.random() * maxrand)
            node.update()

        for i in range(m):
            nodeslist = [] # sequence of nodes in this iteration
            shifts = [] # sequence of nodes' shifts in this iteration
            for node in self.diagram.nodes.values():
                nodeslist.append(node)
                shift = []
                for other in self.diagram.nodes.values():
                    # Calculating cumulative shift
                    shift = shift + self.__shift(node, other, self.__force(node, other, c1, c2, c3, c4))
                shifts.append(shift)
            # Moving all nodes according to calculated shifts
            for node in self.diagram.nodes.values():
                node.moveBy(shifts[nodeslist.index(node)][0], shifts[nodeslist.index(node)][1])
        return True

    def __force(self, node1, node2, c1, c2, c3, c4):
        """
        Function calculating force between two nodes
        """
        d = self.__dist(node1, node2)
        # Calculating repel force between node and other
        force = -c3 / math.sqrt(d)
        # Calculating attract force between node and other
        if node2 in node1.neighbours:
            force = force + c1 * math.log(d/c2, 2)
        return c4 * force

    def __shift(self, node1, node2, force):
        """
        Function calculating shift from one node to another due to
        given force
        """
        versor = self.__versor(node1, node2)
        shift = [0,0]
        shift[0] = versor[0] * force
        shift[1] = versor[1] * force
        return shift

    def __dist(self, node1, node2):
        """
        Function calculating euclidean distance between two given nodes
        """
        d =  math.sqrt(math.pow(node1.pos().x() - node2.pos().x(), 2) +
                math.pow(node1.pos().y() - node2.pos().y(), 2)) - math.sqrt(2) * self._max_size_of_drawable_node([node1, node2])
        if d < 0:
            return 1
        else:
            return d

    def __versor(self, node1, node2):
        """
        Function calculating versor shift beetween two given nodes
        from node1 to node2
        """
        d = self.__dist(node1, node2)
        return ((node2.pos().x() - node1.pos().x())/d, (node2.pos().y() - node1.pos().y())/d)

class GraphvizLayout(Layout):

    def __init__(self, diagram, algorithm, scale=2.5):
        self.alg = algorithm
        self.scale = scale
        super(GraphvizLayout, self).__init__(diagram)

    def apply(self):
        try:
            import pygraphviz as pgv
        except ImportError:
            return False
        A=pgv.AGraph()
        A.node_attr['shape']='square'
        for node in self.diagram.nodes.values():
            w = node.boundingRect().width() 
            h = node.boundingRect().height() 
            A.add_node(node.uml_object.name, height=h, width=w)

        for edge in self.diagram.edges.values():
            u = edge.source_anchor.slot.uml_object.name
            v = edge.target_anchor.slot.uml_object.name
            A.add_edge(u, v)

        A.layout(prog=self.alg)
        lowest_x = float("inf")
        lowest_y = float("inf")

        for n in A.nodes():
            node = self.diagram.nodes[n.name.encode('ascii','ignore')]
            x,y = n.attr['pos'].split(',')
            x=float(x)*self.scale
            y=float(y)*self.scale
            if x < lowest_x: 
                lowest_x = x
            if y < lowest_y: 
                lowest_y = y
            node.moveBy(x,y)
        for n in self.diagram.nodes.values():
            n.moveBy(-lowest_x, -lowest_y)
        return True
