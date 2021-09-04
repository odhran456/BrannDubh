WIDTH = HEIGHT = 700
DIMENSION = 7
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 5
IMAGES = {}
FILE_PATH_IMAGES = "images/"
FILE_EXTENSION = ".png"
CORNER_SQUARES_DICT = {(0, 0): [(0, 1), (0, 2)],
                       (0, DIMENSION - 1): [(0, DIMENSION - 2), (0, DIMENSION - 3)],
                       (DIMENSION - 1, 0): [(DIMENSION - 2, 0), (DIMENSION - 3, 0)],
                       (DIMENSION - 1, DIMENSION - 1): [(DIMENSION - 2, DIMENSION - 1), (DIMENSION - 3, DIMENSION - 1)]
                       }
CENTRE_SQUARE = [(DIMENSION // 2, DIMENSION // 2)]
SPECIAL_SQUARES = [*CORNER_SQUARES_DICT.keys()] + CENTRE_SQUARE
