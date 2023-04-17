from cmu_graphics import *
import matrix
import block
import math


def onAppStart(app):
    # set 800 by 800 canvas size (for now)
    app.width = 800
    app.height = 800

    # Set maximum x,y (we normalize these)
    app.xMax = 1
    app.yMax = 1

    #Locate our origin:
    app.x0 = app.width/2
    app.y0 = app.width/2

    # set minimum and maximum z depth (n, f)
    app.n = 1
    app.f = 2

    # (x,y,z)
    app.Piece = block.Block((-0.5,0,0),(0.1,0.2,0.1))

def redrawAll(app):
    drawBlock(app)

def drawBlock(app):
    # increment through each edge and make line:
    for edge in app.Piece.edges:
        p1 = edge[0]
        p2 = edge[1]

        # we want the camera to look down 
        # let's say 30 degrees, so rotate vectors up 
        # ROTATE ABOUT X-AXIS

        p1 = matrix.rotate(p1, math.pi/6, 1)
        p2 = matrix.rotate(p2, math.pi/6, 1)

        x1 = p1[0]
        y1 = p1[1]
        z1 = p1[2]
        x2 = p2[0]
        y2 = p2[1]
        z2 = p2[2]

        projX1 = matrix.getProjection(x1, z1, app.n)
        projY1 = matrix.getProjection(y1, z1, app.n)
        projX2 = matrix.getProjection(x2, z2, app.n)
        projY2 = matrix.getProjection(y2, z2, app.n)

        # must scale up by size of the screen
        x1Displacement = projX1*app.width/2
        x2Displacement = projX2*app.width/2
        y1Displacement = projY1*app.height/2
        y2Displacement = projY2*app.height/2


        drawLine(app.x0+x1Displacement, app.y0+y1Displacement, 
                 app.x0+x2Displacement, 
                 app.y0+y2Displacement, fill='black')
            
def onKeyPress(app, key):
    print(app.Piece.extension)
    # https://en.wikipedia.org/wiki/Rotation_matrix

    index = 0
    angle = math.pi/2
    if key == 'right':
        index = 3
    elif key == 'left':
        index = 3
        angle *= -1
    elif key == 'up':
        index = 1
    elif key == 'down':
        index = 1
        angle *= -1

    if index != 0:
        points = app.Piece.points
        for i in range(len(points)):
            points[i] = matrix.rotate(points[i], angle, index)

        # don't forget to updateEdges:
        app.Piece.updateEdges()

    print(app.Piece.extension)


def main():
    runApp()

if __name__ == '__main__':
    main()