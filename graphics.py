from cmu_graphics import *
import matrix
import block
import math
import boards
import map


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

    # map:
    map1 = boards.level1 
    app.level = map.Map(map1[0], map1[1])

    # (x,y,z)
    app.Piece = app.level.Piece

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

            points = app.Piece.points

            # translation <-- rotation <--- translation
            # INSPIRED BY https://www.youtube.com/watch?v=cN97hkDrzcc&list=PLqCJpWy5Fohe8ucwhksiv9hTF5sfid8lA&index=5&ab_channel=ChiliTomatoNoodle

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
                    #FIRST THE TRANSLATION PART:
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
    drawTiles(app)
    drawBlock(app)
    print(matrix.findExtremum(app.Piece.points, 1, 1))

def drawTiles(app):
    Tiles = app.level.Tiles
    for tile in Tiles:
        points = tile.points
        color = tile.color
        p1 = points[0]
        p2 = points[1]
        p3 = points[2]
        p4 = points[3]

        # we want the camera to look down 
        # let's say 45 degrees, so rotate vectors up 
        # ROTATE ABOUT X-AXIS

        p1 = matrix.rotate(p1, math.pi/4, 1)
        p2 = matrix.rotate(p2, math.pi/4, 1)
        p3 = matrix.rotate(p3, math.pi/4, 1)
        p4 = matrix.rotate(p4, math.pi/4, 1)


        x1 = p1[0]
        y1 = p1[1]
        z1 = p1[2]
        x2 = p2[0]
        y2 = p2[1]
        z2 = p2[2]
        x3 = p3[0]
        y3 = p3[1]
        z3 = p3[2]
        x4 = p4[0]
        y4 = p4[1]
        z4 = p4[2]

        projX1 = matrix.getProjection(x1, z1, app.n)
        projY1 = matrix.getProjection(y1, z1, app.n)
        projX2 = matrix.getProjection(x2, z2, app.n)
        projY2 = matrix.getProjection(y2, z2, app.n)
        projX3 = matrix.getProjection(x3, z3, app.n)
        projY3 = matrix.getProjection(y3, z3, app.n)
        projX4 = matrix.getProjection(x4, z4, app.n)
        projY4 = matrix.getProjection(y4, z4, app.n)
        
        x1Displacement = projX1*app.width/2
        x2Displacement = projX2*app.width/2
        x3Displacement = projX3*app.width/2
        x4Displacement = projX4*app.width/2
        y1Displacement = projY1*app.height/2
        y2Displacement = projY2*app.height/2
        y3Displacement = projY3*app.height/2
        y4Displacement = projY4*app.height/2

        drawPolygon(app.x0+x1Displacement, app.y0+y1Displacement, 
                 app.x0+x2Displacement, app.y0+y2Displacement,  
                 app.x0+x4Displacement, app.y0+y4Displacement,
                 app.x0+x3Displacement, app.y0+y3Displacement,  
                 fill=color, border='black')

 
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
           app.extremum = matrix.findExtremum(points,0,1)
        elif key == 'left':
            app.rotateType = 2
            app.extremum = matrix.findExtremum(points,0,0)
        elif key == 'down':
            app.rotateType = 3
            app.extremum = matrix.findExtremum(points,2,0)
        elif key == 'up':
            app.rotateType = 4
            app.extremum = matrix.findExtremum(points,2,1)

def main():
    runApp()

if __name__ == '__main__':
    main()