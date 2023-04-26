import math
import matrix
import tile
import block

class Map:
# position is determined by bottom_left coordinate
# tiles: [(position, type)]
# piece: ((geometricPosition), (extension), {tilesUnderneath}) --> start location
    def __init__(self, tiles, piece):
        tileCoordinates = [tile[0] for tile in tiles]

        # WE GOT TO SCALE THE BOARD SO IT FITS ON THE SCREEN:
        # mX,mY,mZ are the number of tiles spanning each dimension
        xPlus = matrix.findExtremum(tileCoordinates,0,1)
        xMinus = matrix.findExtremum(tileCoordinates,0,-1)
        yPlus = matrix.findExtremum(tileCoordinates,1,1)
        yMinus = matrix.findExtremum(tileCoordinates,1,-1)
        zPlus = matrix.findExtremum(tileCoordinates,2,1)
        zMinus = matrix.findExtremum(tileCoordinates,2,-1)

        mX = xPlus - xMinus
        mY = yPlus - yMinus
        mZ = zPlus - zMinus
        maxCount = max(mX,mY,mZ)
        scalingFactor = 1/maxCount

        self.scalingFactor = scalingFactor
        self.tileCoordinates = set(tileCoordinates)
        self.goalTiles = set()
        self.fragileTiles = set()


        for i in range(len(tiles)):
            if tiles[i][1] == 2:
                point1 = tiles[i][0]
                point2 = matrix.vectorAddition(point1, (1,0,0))
                point3 = matrix.vectorAddition(point1, (1,0,1))
                point4 = matrix.vectorAddition(point1, (0,0,1))
                self.goalTiles = {point1, point2, point3, point4}
            elif tiles[i][1] == 1:
                point1 = tiles[i][0]
                point2 = matrix.vectorAddition(point1, (1,0,0))
                point3 = matrix.vectorAddition(point1, (1,0,1))
                point4 = matrix.vectorAddition(point1, (0,0,1))
                self.fragilelTiles = {point1, point2, point3, point4}

        # ADD ALL GRID POINTS to tileCoordinates
        newGridPoints = set()
        for point in self.tileCoordinates:
            point1 = matrix.vectorAddition(point, (0,0,1))
            point2 = matrix.vectorAddition(point, (1,0,1))
            point3 = matrix.vectorAddition(point, (1,0,0))

            newGridPoints.add(point1)
            newGridPoints.add(point2)
            newGridPoints.add(point3)

        self.tileCoordinates = set.union(self.tileCoordinates, newGridPoints)


        translate = (-(xPlus + xMinus)/2, -(yPlus + yMinus)/2, zMinus)
        self.translate = translate

        tileCoordinates = [matrix.vectorAddition(translate, tileCoordinates[i]) 
                           for i in range(len(tileCoordinates))]
        
        # make this a set, so we can easily locate the block

        self.Tiles = [tile.Tile(matrix.scaleVector(tileCoordinates[i],scalingFactor), 
                                matrix.scaleVector((1,0,1), scalingFactor), tiles[i][1]) 
                                for i in range(len(tiles))]

        self.startingLocation = piece[0]

        self.Piece = block.Block(matrix.scaleVector(matrix.vectorAddition(piece[0], translate),scalingFactor), 
                                 matrix.scaleVector(piece[1],scalingFactor))
        self.floor = piece[0][1] + piece[1][1]
        
        self.PieceArea = piece[1][0]* piece[1][1] * piece[1][2]


        xPlus = matrix.findExtremum(tileCoordinates,0,1)
        xMinus = matrix.findExtremum(tileCoordinates,0,-1)

    # note for 1 by 1 by 1 blocks, isStanding returns False
    def isStanding(self):
        coordinates = self.Piece.points
        xPlus = matrix.findExtremum(coordinates,0,1)
        xMinus = matrix.findExtremum(coordinates,0,-1)
        yPlus = matrix.findExtremum(coordinates,1,1)
        yMinus = matrix.findExtremum(coordinates,1,-1)
        zPlus = matrix.findExtremum(coordinates,2,1)
        zMinus = matrix.findExtremum(coordinates,2,-1)

        x = xPlus - xMinus    
        y = yPlus - yMinus
        z = zPlus - zMinus

        if y > x and y > z:
            return True
        return False
        

    # checks to make sure the block is still on the map
    # if inside: returns NONE
    # if outside returns (axis, value), where:
    # axis is the axis that the block cantilevers
    # and value is where the cantilevers occurs
    def checkInside(self):
        bottomPoints = self.getBottomPoints()

        # LOGIC
        # IF ONE x COMPONENT INSIDE AND OTHER OUTSIDE --> 
        # KNOW THIS IS THE BAD AXIS
        # REPEAT FOR OTHER COMPONENTS
        # IF BOTH COMPONENTS INSIDE OR OUTSIDE -->
        # GOOD AXIS

        minX = matrix.findExtremum(bottomPoints,0,0)
        maxX = matrix.findExtremum(bottomPoints,0,1)
        minZ = matrix.findExtremum(bottomPoints,2,0)
        maxZ = matrix.findExtremum(bottomPoints,2,1)
        y = bottomPoints[0][1]
        outsideCount = 0

        for x in range(minX, maxX+1):
            for z in range(minZ, maxZ+1):
                point = (x,y,z)
                if point not in self.tileCoordinates:
                    outsideCount += 1

        if outsideCount >= self.PieceArea/2:
            return False

        # block is inside
        return True


    def getBottomPoints(self):
        # first locate min and max x and z coordinates
        # locate min y coordinates
        points = self.Piece.points
        scaledY = matrix.findExtremum(points,1,1)
        unscaledY = round(scaledY/self.scalingFactor - self.translate[1])

        bottomPoints = []
        for point in points:
            x = point[0]
            x = round(x/self.scalingFactor - self.translate[0])
            y = point[1]
            y = round(y/self.scalingFactor - self.translate[1])
            z = point[2]
            z = round(z/self.scalingFactor - self.translate[2])
            if y == unscaledY:
                cor1 = (x,y,z)
                bottomPoints.append(cor1)

        return bottomPoints
        
    def verifyWin(self):
        bottomPoints = self.getBottomPoints()

        for point in bottomPoints:
            if point not in self.goalTiles:
                return False
        return True
    



