import matrix
class Tile:

    def __init__(self, location, dimension, type):
        if type == 0:
            self.color = 'lightgrey'
            self.maxWeight = False
            self.end = False
        elif type == 1:
            self.color = 'orange'
            self.maxWeight = True
            self.end = False
        elif type == 2:
            self.color = 'maroon'
            self.maxWeight = False
            self.end = True

        p1 = location
        p2 = matrix.vectorAddition(p1, (dimension[0], 0, 0))
        p3 = matrix.vectorAddition(p1, (0, 0, dimension[2]))
        p4 = matrix.vectorAddition(p1, dimension)
        
        self.points = [p1,p2,p3,p4]
        self.addEdges()

    def addEdges(self):
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]
        p4 = self.points[3]

        e1 = (p1,p2)
        e2 = (p1,p3)
        e3 = (p2,p4)
        e4 = (p3,p4)

        self.edges = {e1,e2,e3,e4}