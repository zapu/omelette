import math
import random

class Layouter(object):

##########################################################################
# circular layout section
##########################################################################

    @staticmethod
    def __circular_layout(diagram, sx=0, sy=0, start=math.pi/2, spread=2):
        """
        Basic layout function placing all nodes on circle, adjusting
        circle range to size of nodes.
        """
        r = 0
        # Finding max size of drawable
        maxsize = Layouter.__max_size_of_drawable_node(diagram.nodes.values())
        n = len(diagram.nodes) # number of drawables
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
            sortednodes = Layouter.__sort_nodes_by_neighbourhood(diagram.nodes.values())
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
        
    @staticmethod
    def __sort_nodes_by_degree(nodes, rev=True):
        """
        Function sorting nodes in order of vertex grade
        """
        return sorted(nodes, key=Layouter.__node_degree, reverse=rev)
    
    @staticmethod
    def __sort_nodes_by_neighbourhood(nodes):
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
            
    @staticmethod
    def __node_degree(node):
        """
        Function calculating node's degree
        """
        return len(node.neighbours)

##########################################################################
# spring layout section (Eades)
##########################################################################

    @staticmethod
    def __spring_layout(diagram, c1=2, c2=2, c3=1, c4=0.1, m=1):
        """
        Layout function using mechanical model of spring embedder.
        """
        # Moving all nodes in random positions
        maxrand = 100
        for node in diagram.nodes.values():
            node.setPos(random.random() * maxrand,
                        random.random() * maxrand)
            node.update()

        for i in range(m):
            nodeslist = []
            shifts = []
            for node in diagram.nodes.values():
                nodeslist.append(node)
                shift = []
                for other in diagram.nodes.values():
                    d = Layouter.__dist(node, other)
                    if d != 0:
                        force = -c3 / math.sqrt(d)
                        if other in node.neighbours:
                            force = force + c1 * math.log(d/c2, 2)
                        force = c4 * force
                        shift = shift + Layouter.__shift(node, other, force)
                print shift
                shifts.append(shift)
            for node in diagram.nodes.values():
                node.moveBy(shifts[nodeslist.index(node)][0], shifts[nodeslist.index(node)][1])

    @staticmethod
    def __shift(node1, node2, force):
        versor = Layouter.__versor(node1, node2)
        shift = [0,0]
        shift[0] = versor[0] * force
        shift[1] = versor[1] * force
        return shift


    @staticmethod
    def __incidence_matrix(diagram):
        """
        Function generating incidence matrix from given diagram
        """
        #initializing incidence array
        incidence = [[ 0 for row in range(len(diagram.nodes))]
                    for col in range(len(diagram.nodes)) ]
        #filling incidence array
        for node in diagram.nodes.values():
            for neigh in node.neighbours:
                incidence[diagram.nodes.values().index(node)][diagram.nodes.values().index(neigh)] = 1
        return incidence

    @staticmethod
    def __dist(node1, node2):
        """
        Function calculating euclidean distance between two given nodes
        """
#        d = -math.sqrt(math.pow(node1.boundingRect().size().width(), 2) + math.pow(node1.boundingRect().size().height(),2))/2
#        d = d - math.sqrt(math.pow(node2.boundingRect().size().width(),2) + math.pow(node2.boundingRect().size().height(),2))/2
#        d = d + math.fabs(math.sqrt(math.pow(node1.pos().x() - node2.pos().x(), 2) + math.pow(node1.pos().y() - node2.pos().y(), 2)))
        return math.fabs(math.sqrt(math.pow(node1.pos().x() - node2.pos().x(), 2) + math.pow(node1.pos().y() - node2.pos().y(), 2)))
#        return math.fabs(d)
#        d =  math.sqrt(math.pow(node1.pos().x() - node2.pos().x(), 2) + math.pow(node1.pos().y() - node2.pos().y(), 2)) - math.sqrt(2) * Layouter.__max_size_of_drawable_node([node1, node2])
#        if d < 0:
#            return 0.5
#        else:
#            return d

    @staticmethod
    def __versor(node1, node2):
        """
        Function calculating versor shift beetween two given nodes
        from node1 to node2
        """
        d = Layouter.__dist(node1, node2)
        return ((node2.pos().x() - node1.pos().x())/d, (node2.pos().y() - node1.pos().y())/d)

    @staticmethod
    def __max_size_of_drawable_node(nodes):
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

##########################################################################

    @staticmethod
    def layout(diagram, mode=1):
        """
        General function calling different layout functions
        """
        if mode == 0:
            Layouter.__circular_layout(diagram)
        if mode == 1:
            Layouter.__spring_layout(diagram)
