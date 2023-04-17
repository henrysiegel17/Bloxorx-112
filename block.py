import matrix

class Block:
    
    def __init__(self, location, extension):
        self.location = location
        self.extension = extension

        p1 = self.location
        p8 = matrix.vectorAddition(self.location, self.extension)

        # from here it's just a bash
        p2 = (p8[0], p1[1], p1[2])
        p3 = (p8[0], p8[1], p1[2])
        p4 = (p1[0], p8[1], p1[2])

        p5 = (p1[0], p1[1], p8[2])
        p6 = (p1[0], p8[1], p8[2])
        p7 = (p8[0], p1[1], p8[2])

        self.points = [p1,p2,p3,p4,p5,p6,p7,p8]

        # Now update edges:
        # ...
        # we are calling a separate function, so we can call this later
        # whenever the block changes orientation
        self.updateEdges()

    def updateEdges(self):
        # I'm expanding for clarity:
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]
        p4 = self.points[3]
        p5 = self.points[4]
        p6 = self.points[5]
        p7 = self.points[6]
        p8 = self.points[7]

        self.edges =   {(p1,p2), (p2,p3), (p1,p4), (p3,p4), 
                         (p5,p6), (p6,p8), (p5,p7), (p7,p8),
                         (p4,p6), (p1,p5), (p3,p8), (p2,p7)
        }

