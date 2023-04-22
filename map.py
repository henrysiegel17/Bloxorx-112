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

        # WE GOT TO SCALE THE BOARD SO IT FITS IN THE SCREEN:
        # mX,mY,mZ are the number of tiles spanning each dimension
        xPlus = matrix.findExtremum(tileCoordinates,0,1)
        xMinus = matrix.findExtremum(tileCoordinates,0,-1)
        yPlus = matrix.findExtremum(tileCoordinates,1,1)
        yMinus = matrix.findExtremum(tileCoordinates,1,-1)
        zPlus = matrix.findExtremum(tileCoordinates,2,1)
        zMinus = matrix.findExtremum(tileCoordinates,2,-1)

        # make this a set, so we can easily locate the block
        self.tileCoordinates = set(tileCoordinates)

        mX = xPlus - xMinus
        mY = yPlus - yMinus
        mZ = zPlus - zMinus
        maxCount = max(mX,mY,mZ)
        scalingFactor = 1/maxCount

        translate = (-(xPlus + xMinus)/2, -(yPlus + yMinus)/2, zMinus)
        tileCoordinates = [matrix.vectorAddition(translate, tileCoordinates[i]) 
                           for i in range(len(tileCoordinates))]

        self.Tiles = [tile.Tile(matrix.scaleVector(tileCoordinates[i],scalingFactor), 
                                matrix.scaleVector((1,0,1), scalingFactor), tiles[i][1]) 
                                for i in range(len(tiles))]

        self.Piece = block.Block(matrix.scaleVector(matrix.vectorAddition(piece[0], translate),scalingFactor), 
                                 matrix.scaleVector(piece[1],scalingFactor))
        self.blockLocations = piece[2]

        

