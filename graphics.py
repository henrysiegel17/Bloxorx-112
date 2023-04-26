from cmu_graphics import *
import random
import matrix
import block
import math
import boards
import map


def onAppStart(app):
    # set 800 by 800 canvas size (for now)
    app.width = 800
    app.height = 800
    app.levelNumber = -1
    app.extremum = 0

    # Set maximum x,y (we normalize these)
    app.xMax = 1
    app.yMax = 1

    #Locate our origin:
    app.x0 = app.width/2
    app.y0 = app.height/2

    # set minimum and maximum z depth n, f)
    app.n = 1
    app.f = 2

    # loading screen
    app.menuRotateCounter = 50
    app.initialCount = 1
    initiateLoadingScreen(app, app.initialCount)
    app.menuSign = [1 for i in range(app.initialCount)]
    app.extremums = [0 for i in range(app.initialCount)]
    app.menuScreen = False

    app.levelTransition = False
    app.moveInSpeed = 0
    app.transitionTime = 0
    app.fadeDistance = 20

    # for now, we will call onStep 30 times per second
    app.stepPerSecond = 30

def restart(app):

    # map:
    map1 = boards.levels[app.levelNumber]
    app.level = map.Map(map1[0], map1[1])

    map2 = None
    app.nextLevel = None
    if app.levelNumber + 1 < len(boards.levels):
        map2 = boards.levels[app.levelNumber+1]
        app.nextLevel = map.Map(map2[0], map1[1])

    # (x,y,z)
    app.Piece = app.level.Piece

    # only relevant when the block is rotating
    app.rotateCounter = 0
    app.rotateType = 0
    app.totalAngle = 0
    app.maxCounter = 15
    app.extremum = 0

    # only relevant when the block is falling off the edge 
    # or when the map loads

    app.fallCounter = 1
    app.die = True
    app.levelTransition = False
    app.loadMap = True

    # go back to menu screen
    app.menuScreen = False

def onStep(app):

    # transitioning to next level
    if app.levelTransition and not app.menuScreen:
        app.moveInSpeed = 0.1
        if app.moveInSpeed * app.transitionTime < app.fadeDistance:

            app.transitionTime += 1
            points = app.Piece.points
            yCM = (matrix.findExtremum(points,1,1) + matrix.findExtremum(points,1,0))/2

            if app.rotateCounter <= app.maxCounter:
                rotate(app, app.Piece, 1, -(math.pi/2)/app.maxCounter, yCM)
                app.rotateCounter += 1
            else:
                app.rotateCounter = 0
                app.extrema = matrix.findExtremum(points,2,1)
                app.Piece.updateEdges()


        else:
            app.moveInSpeed = 0
            app.transitionTime = 0
            app.levelNumber += 1
            app.levelTransition = False
            restart(app)

        
    elif app.levelNumber != -1 and not app.menuScreen:
        if app.rotateType != 0:
            # let's say it takes 1/2 second to rotate 90 degrees
            angle = (math.pi/2)/app.maxCounter
            app.rotateCounter += 1
            app.totalAngle += angle

            # end cycle:
            if app.rotateCounter <= app.maxCounter:            

                points = app.Piece.points

                # translation <-- rotation <--- translation
                # INSPIRED BY https://www.youtube.com/watch?v=cN97hkDrzcc&list=PLqCJpWy5Fohe8ucwhksiv9hTF5sfid8lA&index=5&ab_channel=ChiliTomatoNoodle

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

                rotate(app, app.Piece, index, angle, 0)

                # don't forget to updateEdges:
                app.Piece.updateEdges()
                
            # we are done with the cycle
            else:

                if app.fallCounter > 75:
                    restart(app)

                # CHECK IF THE PLAYER WINS
                if app.level.verifyWin():
                    app.rotateCounter = app.maxCounter

                    print('You Win!')
                    if app.levelNumber < len(boards.levels) - 1:
                        app.levelTransition = True

                # CHECK TO MAKE SURE BLOCK IS ON THE MAP:
                if app.fallCounter > 1 or not app.level.checkInside():
                    print('block is not on the map')

                    speed = app.fallCounter*0.0001 + 0.005
                    points = app.Piece.points


                    angle = (math.pi/2)/app.maxCounter
                    index = 0

                    # right
                    if app.rotateType == 1:
                        index = 3
                        app.extremum = matrix.findExtremum(points,0,1)

                    # left
                    elif app.rotateType == 2:
                        index = 3
                        angle *= -1
                        app.extremum = matrix.findExtremum(points,0,0)

                    # down
                    elif app.rotateType == 3:
                        index = 1 
                        app.extremum = matrix.findExtremum(points,2,0)

                    # up
                    elif app.rotateType == 4:
                        index = 1
                        angle *= -1
                        app.extremum = matrix.findExtremum(points,2,1)

                    yMin = matrix.findExtremum(points, 1, 0)
                    yMax = matrix.findExtremum(points, 1, 1)

                    yDisplacement = (yMin + yMax)/2
                    
                    rotate(app, app.Piece, index, angle, -yDisplacement)

                    for i in range(len(points)):
                        points[i] = matrix.vectorAddition(points[i], 
                                                          (0,speed*app.fallCounter,0))
                    app.Piece.updateEdges()
                    app.fallCounter += 1

                else:
                    print('block is on the map')

                    app.rotateCounter = 0
                    app.rotateType = 0
                    app.totalAngle = 0

    # else we are on the main screen
    else:
        if app.menuRotateCounter < 50:
        # randomly walk in either direction:
            angle = (math.pi/2)/50
            for b in range(len(app.preliminaryBlocks)):
                points = app.preliminaryBlocks[b].points
                yMax = matrix.findExtremum(points, 1, 1)
                app.extremum = app.extremums[b]

                index = 3
                angle *= app.menuSign[b]
                rotate(app, app.preliminaryBlocks[b], 3, angle, -yMax)
            app.menuRotateCounter+=1

        else:
            app.menuRotateCounter = 0
            for i in range(len(app.menuSign)):
                app.menuSign[i] = random.randint(1,2)
                if app.menuSign[i] == 2:
                    app.menuSign[i] = -1
                
                points = app.preliminaryBlocks[i].points
                if app.menuSign[i] == 1:
                    app.extremums[i] = matrix.findExtremum(points,0,1)
                else:
                    app.extremums[i] = matrix.findExtremum(points,0,0)


def rotate(app, piece, index, angle, yDisplacement):
    points = piece.points
    if index != 0:
        for i in range(len(points)):
            #FIRST THE TRANSLATION PART:
            displacement = None
            if index == 1:
                displacement = [0,yDisplacement,-app.extremum]
            elif index == 3:
                displacement = [-app.extremum,yDisplacement,0]
            points[i] = matrix.vectorAddition(points[i], displacement)
            # THEN THE ROTATION
            points[i] = matrix.rotate(points[i], angle, index)
            # AND FINALLY THE INVERSE TRANSLATION
            displacement = matrix.reverseVector(displacement)
            points[i] = matrix.vectorAddition(points[i], displacement)

def playMenuScreen(app):
    drawLabel('BLOXORX 112', app.width/2, app.height/2-50, bold=True, size=88, 
              fill='white', border = 'black')
    drawLine(100, app.height/2-100, app.width-100, app.height/2-100)
    drawLine(100, app.height/2, app.width-100, app.height/2)
    drawLabel('Laws of the Blox:', 
              100, 50 + app.height/2, size=18, 
              font='Monospace',align='left')
    drawLabel('1. Use arrow keys to step and roll. ', 
              100, 100 + app.height/2, size=18, 
              font='Monospace',align='left')
    drawLabel('2. Have Fun', 
              100, 150 + app.height/2, size=18, 
              font='Monospace', align='left')
    drawLabel('3. Enter Enter', 
              100, 200 + app.height/2, size=18, 
              font='Monospace', align = 'left')
    randomWalk(app)

def initiateLoadingScreen(app, size):
    delta = 0.8/(size+1)
    app.preliminaryBlocks = []
    for i in range(size):
        x = (random.randint(1,8))/10
        z = (random.randint(1,8))/10
        y = 0.2
        app.preliminaryBlocks.append(block.Block((0, -0.2, 1 + 10*i*delta),(x,y,z)))

def randomWalk(app):
    for block in app.preliminaryBlocks:
        drawBlock(app, block, math.pi/6)


def redrawAll(app):
    if app.levelTransition == True and not app.menuScreen:
        if app.transitionTime < 180:
            # only next Level comes in
            print('calling extremum')
            drawBlock(app, app.Piece, math.pi/4)

        # scroll next level
        drawTiles(app, math.pi/4, 1,2)


    elif app.levelNumber != -1 and not app.menuScreen:
        drawLabel(f'Level {app.levelNumber + 1}', app.width/2, app.height-150, bold=True, size=88, 
              fill='white', border = 'black')
        drawLine(100, app.height-100, app.width-100, app.height-100)
        drawLine(100, app.height-200, app.width-100, app.height-200)
        drawLabel('Press M or ESC to return to menu. Press R to restart', app.width/2, app.height-50, bold=True, size=18, 
              font='Monospace')
        if app.levelNumber < len(boards.levels) - 1:
            drawTiles(app, math.pi/4, 0,2)
        else:
            drawTiles(app, math.pi/4, 0,1)
        drawBlock(app, app.Piece, math.pi/4)
    # Else we are on the menuScreen
    else:
        playMenuScreen(app)

def drawTiles(app, cameraAngle, minTile, maxTile):
    for mapNum in range(minTile, maxTile):
        Tiles = None
        reduct = 0
        if mapNum >= 2:
            continue
        if maxTile > 2:
            reduct = 1
            Tiles = app.level.Tiles
        elif mapNum == maxTile-1 and app.nextLevel != None:
            Tiles = app.nextLevel.Tiles
        elif mapNum == minTile:
            Tiles = app.level.Tiles
        for tile in Tiles:
            points = tile.points
            color = tile.color

            for i in range(len(points)):
                points[i] = matrix.vectorAddition(points[i], (0,0,app.fadeDistance*(mapNum)))
            
            p1 = points[0]
            p2 = points[1]
            p3 = points[2]
            p4 = points[3]

            # we want the camera to look down 
            # let's say 45 degrees, so rotate vectors up 
            # ROTATE ABOUT X-AXIS

            p1 = matrix.rotate(p1, cameraAngle, 1)
            p2 = matrix.rotate(p2, cameraAngle, 1)
            p3 = matrix.rotate(p3, cameraAngle, 1)
            p4 = matrix.rotate(p4, cameraAngle, 1)

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
            
            for i in range(len(points)):
                points[i] = matrix.vectorAddition(points[i], (0,0,-(app.fadeDistance+app.moveInSpeed)*(mapNum)))

    
def drawBlock(app, piece, cameraAngle):
    # increment through each edge and make line:
    piece.updateEdges()
    for edge in piece.edges:
        p1 = edge[0]
        p2 = edge[1]

        # we want the camera to look down 
        # let's say 45 degrees, so rotate vectors up 
        # ROTATE ABOUT X-AXIS

        p1 = matrix.rotate(p1, cameraAngle, 1)
        p2 = matrix.rotate(p2, cameraAngle, 1)

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
    #We first presume the player is on the menu Screen
    if app.levelNumber==-1:
        if key == 'enter' or key =='return':
            # game has just loaded
            if app.menuScreen == False:
                app.levelNumber = 0
            restart(app)

    elif app.menuScreen == True:
        if key == 'enter' or key =='return':
            restart(app)
    else:
        points = app.Piece.points
        if app.rotateType == 0 and app.levelTransition == False:
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

            # player wants to go back to menu screen
            elif key == 'm' or key == 'escape':
                app.menuScreen = True
                initiateLoadingScreen(app, app.initialCount)
                # loading screen
                app.menuRotateCounter = 50
                app.initialCount = 1
                app.menuSign = [1 for i in range(app.initialCount)]
                app.extremums = [0 for i in range(app.initialCount)]

            # player want to restart level:
            elif key == 'r':
                app.levelNumber = 0
                restart(app)
        
def main():
    runApp()

if __name__ == '__main__':
    main()