import pygame as p
from BrannDubh import BD_Engine

p.init()
WIDTH = HEIGHT = 700
DIMENSION = 7
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 5
IMAGES = {}
FILE_PATH_IMAGES = "images/"
FILE_EXTENSION = ".png"
CORNER_SQUARES = [(0, 0), (0, DIMENSION - 1), (DIMENSION - 1, 0), (DIMENSION - 1, DIMENSION - 1)]
CENTRE_SQUARE = [(DIMENSION // 2, DIMENSION // 2)]
SPECIAL_SQUARES = CORNER_SQUARES + CENTRE_SQUARE


def load_images(file_path, file_extension):
    pieces = ["wP", "bP", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.image.load(file_path + piece + file_extension)


def main():
    screen = p.display.set_mode(size=(WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = BD_Engine.GameState()
    load_images(file_path=FILE_PATH_IMAGES, file_extension=FILE_EXTENSION)
    running = True
    sq_selected = ()
    player_clicks = []
    print("Currently debugging. White to move first, although this strict logic has not been coded in yet so black "
          "could move and collisions would not be realised.")
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):  # check if user previously just selected this sqaure
                    sq_selected = ()  # unselect
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)

            # check if a user has made two clicks
            if len(player_clicks) == 2:
                move = BD_Engine.Move(start_square=player_clicks[0], end_square=player_clicks[1], board=gs.board)
                print(gs.check_for_captures(move=move))
                gs.make_move(move=move)
                sq_selected = ()
                player_clicks = []

        draw_game_state(screen=screen, gs=gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_board(screen):
    colours = [p.Color("white"), p.Color("gray")]

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            row_col_tuple = (row, col)
            if row_col_tuple in SPECIAL_SQUARES:
                colour = p.Color("gold")
            else:
                colour = colours[
                    ((row + col) % 2)]  # every white space on chess board is even when r+c, hence remainder
                # will be 0. Same idea for all dark squares being odd, having remainder 1.
            p.draw.rect(screen, colour, p.Rect((col * SQ_SIZE, row * SQ_SIZE), (SQ_SIZE, SQ_SIZE)))


def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece],
                            p.Rect(((col * SQ_SIZE) + (SQ_SIZE // 4), row * SQ_SIZE), (SQ_SIZE, SQ_SIZE)))


def draw_game_state(screen, gs):
    draw_board(screen)
    # here this function can be used to add legal move highlighting, piece highlighting (later)
    draw_pieces(screen, gs.board)


if __name__ == "__main__":
    main()
