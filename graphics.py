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
    app.Piece = block.Block((-0.5,0,0),(0.3,0.2,0.1))

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

    points = app.Piece.points

    # translation <-- rotation <--- translation

    # average x-cor of p1 and p2
    xAvg = (points[0][0] + points[1][0])/2
    # average z-cor of p1 and p5
    zAvg = (points[0][2] + points[4][2])/2

    xOffSet = app.Piece.extension[0]/2
    zOffSet = app.Piece.extension[2]/2
    offSet = None
    avgMove = None

    # need to check if x,z is positive or negative
    if xAvg < 0:
        xOffSet *= -1
    if zAvg < 0:
        zOffSet *= -1

    index = 0
    angle = math.pi/2
    if key == 'right':
        index = 3
        offSet = xOffSet
        avgMove = xAvg
    elif key == 'left':
        index = 3
        angle *= -1
        avgMove = xAvg
        offSet = -xOffSet
    elif key == 'up':
        index = 1
        avgMove = zAvg
        offSet = zOffSet
    elif key == 'down':
        index = 1
        angle *= -1
        avgMove = zAvg
        offSet = -zOffSet

    if index != 0:
        for i in range(len(points)):
            # FIRST THE TRANSLATION PART:
            displacement = None
            if index == 1:
                displacement = [-offSet - avgMove, 0,0]
            elif index == 3:
                displacement = [0,0,-offSet - avgMove]
            points[i] = matrix.vectorAddition(points[i], displacement)
            # THEN THE ROTATION
            points[i] = matrix.rotate(points[i], angle, index)
            # AND FINALLY THE INVERSE TRANSLATION
            displacement = matrix.reverseVector(displacement)
            points[i] = matrix.vectorAddition(points[i], displacement)

        # don't forget to updateEdges:
        app.Piece.updateEdges()

    print(app.Piece.extension)


def main():
    runApp()

if __name__ == '__main__':
    main()