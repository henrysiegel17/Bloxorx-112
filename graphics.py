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
    app.Piece = block.Block((-0.5,-0.2,0),(0.1,0.2,0.4))

    # only true when the block is rotating
    app.rotateCounter = 0
    app.rotateType = 0
    app.totalAngle = 0
    app.maxCounter = 15
    app.extremum = 0

    # for now, we will call onStep 30 times per second
    app.stepPerSecond = 30

def onStep(app):
    # let's say it takes 1/2 second to rotate 90 degrees
    angle = (math.pi/2)/app.maxCounter

    if app.rotateType != 0:
        app.rotateCounter += 1
        app.totalAngle += angle

        # end cycle:
        if app.rotateCounter <= app.maxCounter:

            # https://en.wikipedia.org/wiki/Rotation_matrix

            points = app.Piece.points

            # translation <-- rotation <--- translation

            # average x-cor of p1 and p2
            xAvg = (points[0][0] + points[1][0])/2
            # average z-cor of p1 and p5
            zAvg = (points[0][2] + points[4][2])/2

            xOffSet = app.Piece.extension[0]/2
            zOffSet = app.Piece.extension[2]/2
            translate = None

            # need to check if x,z is positive or negative
            if xAvg < 0:
                xOffSet *= -1
            if zAvg < 0:
                zOffSet *= -1

            index = 0

            if app.rotateType == 1:
                index = 3
            elif app.rotateType == 2:
                index = 3
                angle *= -1
            elif app.rotateType == 3:
                index = 1
            elif app.rotateType == 4:
                index = 1
                angle *= -1

            if index != 0:
                for i in range(len(points)):
                    # FIRST THE TRANSLATION PART:
                    displacement = None
                    if index == 1:
                        displacement = [0,0,-app.extremum]
                    elif index == 3:
                        displacement = [-app.extremum,0,0]
                    points[i] = matrix.vectorAddition(points[i], displacement)
                    # THEN THE ROTATION
                    points[i] = matrix.rotate(points[i], angle, index)
                    # AND FINALLY THE INVERSE TRANSLATION
                    displacement = matrix.reverseVector(displacement)
                    points[i] = matrix.vectorAddition(points[i], displacement)

                # don't forget to updateEdges:
                app.Piece.updateEdges()
            
        # we are done with the cycle
        else:
            app.rotateCounter = 0
            app.rotateType = 0
            app.totalAngle = 0

def redrawAll(app):
    drawBlock(app)
    print(findExtremum(app.Piece.points, 1, 1))

def drawBlock(app):
    # increment through each edge and make line:
    for edge in app.Piece.edges:
        p1 = edge[0]
        p2 = edge[1]

        # we want the camera to look down 
        # let's say 45 degrees, so rotate vectors up 
        # ROTATE ABOUT X-AXIS

        p1 = matrix.rotate(p1, math.pi/4, 1)
        p2 = matrix.rotate(p2, math.pi/4, 1)

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
    points = app.Piece.points
    if app.rotateType == 0:
        if key == 'right':
           app.rotateType = 1
           app.extremum = findExtremum(points,0,1)
        elif key == 'left':
            app.rotateType = 2
            app.extremum = findExtremum(points,0,0)
        elif key == 'down':
            app.rotateType = 3
            app.extremum = findExtremum(points,2,0)
        elif key == 'up':
            app.rotateType = 4
            app.extremum = findExtremum(points,2,1)

# type = 0: minimum
# type = 1: maximum
def findExtremum(points, index, type):
    extreme = points[0][index]
    for p in points:
        if type == 0:
            if p[index] < extreme:
                extreme = p[index]
        elif type == 1:
            if p[index] > extreme:
                extreme = p[index]
    return extreme

def main():
    runApp()

if __name__ == '__main__':
    main()