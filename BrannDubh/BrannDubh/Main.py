import pygame as p
from BrannDubh import BD_Engine
from BrannDubh import Constants
from BrannDubh import Bot
import pandas as pd
from timeit import default_timer as timer


p.init()


def load_images(file_path, file_extension):
    pieces = ["wP", "bP", "bK"]
    for piece in pieces:
        Constants.IMAGES[piece] = p.image.load(file_path + piece + file_extension)


def main_pygame():
    screen = p.display.set_mode(size=(Constants.WIDTH, Constants.HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = BD_Engine.GameState()
    valid_moves = gs.get_all_possible_moves()

    move_made = False  # flag variable, to ensure we dont call move checker every frame and only when we need it
    load_images(file_path=Constants.FILE_PATH_IMAGES, file_extension=Constants.FILE_EXTENSION)
    running = True
    sq_selected = ()
    player_clicks = []
    end_game = False
    white_human = True  # white side is human player
    black_human = False  # black side is human player

    while running:
        is_humans_turn = (gs.whiteToMove and white_human) or (not gs.whiteToMove and black_human)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if e.type == p.MOUSEBUTTONDOWN:
                if not end_game and is_humans_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // Constants.SQ_SIZE
                    row = location[1] // Constants.SQ_SIZE
                    if sq_selected == (row, col):  # check if user previously just selected this sqaure
                        sq_selected = ()  # unselect
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)

                    # check if a user has made two clicks
                    if len(player_clicks) == 2:
                        move = BD_Engine.Move(start_square=player_clicks[0], end_square=player_clicks[1],
                                              board=gs.board)
                        if move in valid_moves:  # note: for Move class i overrode __eq__() to allow comparison of two objects
                            gs.make_move(move=move)
                            move_made = True
                            sq_selected = ()
                            player_clicks = []

                        else:  # if it's not a valid move, the latest piece the person clicked on is probably what they want
                            # their first click to be
                            player_clicks = [sq_selected]

        if not end_game and not is_humans_turn:  # bot makes move if it's a bot's turn to play
            move = Bot.bot_make_random_move(
                valid_moves=valid_moves)  # could rename this to 'bot_move', but i kept human and bot move as move and end of loop i print move.get_algebraic_notation()
            gs.make_move(move=move)
            move_made = True

        if move_made:  # if the flag gets triggered this frame, generate upcoming all possible moves
            valid_moves = gs.get_all_possible_moves()
            move_made = False

            # TODO: Replace everything using self.board (the list of lists) with a self.board_df (a pd df). It'll make operations quicker.
            board_df = pd.DataFrame(gs.board, columns=[*Constants.COLS_TO_FILES.values()], index=[*Constants.ROWS_TO_RANKS.values()][::-1])

            print(board_df)
            print(move.get_algebraic_notation())

            #  win conditions: OR(piece_moved == bK && end_square in corner_squares, piece_captured == bK)
            if gs.black_win_condition:  # this is checking if black wins
                end_game = True
                print(len(gs.moveLog), gs.moveLog)
                print("Black is the Winner!")
            if gs.white_win_condition:
                end_game = True
                print(len(gs.moveLog), gs.moveLog)
                print("White is the Winner!")
            if gs.draw_condition:
                end_game = True
                print(len(gs.moveLog), gs.moveLog)
                print('Draw by threefold repetition!')
            # Check here if win conditions are satisfied. itll only check after move and not every frame

        draw_game_state(screen=screen, gs=gs, valid_moves=valid_moves,
                        sq_selected=sq_selected)  # state updates every frame
        clock.tick(Constants.MAX_FPS)
        p.display.flip()


def main_command_line():  # no visuals
    start_time = timer()

    gs = BD_Engine.GameState()
    valid_moves = gs.get_all_possible_moves()

    move_made = False  # flag variable, to ensure we dont call move checker every frame and only when we need it

    running = True
    sq_selected = ()
    player_clicks = []
    end_game = False
    white_human = False  # white side is human player
    black_human = False  # black side is human player

    while running:
        is_humans_turn = (gs.whiteToMove and white_human) or (not gs.whiteToMove and black_human)

        if not end_game and not is_humans_turn:  # bot makes move if it's a bot's turn to play
            move = Bot.bot_make_random_move(
                valid_moves=valid_moves)  # could rename this to 'bot_move', but i kept human and bot move as move and end of loop i print move.get_algebraic_notation()
            gs.make_move(move=move)
            move_made = True

        if move_made:  # if the flag gets triggered this frame, generate upcoming all possible moves
            valid_moves = gs.get_all_possible_moves()
            move_made = False

            # TODO: Replace everything using self.board (the list of lists) with a self.board_df (a pd df). It'll make operations quicker.
            board_df = pd.DataFrame(gs.board, columns=[*Constants.COLS_TO_FILES.values()], index=[*Constants.ROWS_TO_RANKS.values()][::-1])
            # TODO: Making the df has the biggest impact on time per game ATM

            #  win conditions: OR(piece_moved == bK && end_square in corner_squares, piece_captured == bK)
            if gs.black_win_condition:  # this is checking if black wins
                end_game = True
                print(len(gs.moveLog), gs.moveLog)
                print("Black is the Winner!")
                running = False
            if gs.white_win_condition:
                end_game = True
                print(len(gs.moveLog), gs.moveLog)
                print("White is the Winner!")
                running = False
            if gs.draw_condition:
                end_game = True
                print(len(gs.moveLog), gs.moveLog)
                print('Draw by threefold repetition!')
                running = False
            # Check here if win conditions are satisfied. itll only check after move and not every frame
    end_time = timer()
    print(end_time - start_time, ' seconds elapsed')  # Time in seconds, e.g. 5.38091952400282


def draw_board(screen):
    colours = [p.Color("white"), p.Color("gray")]

    for row in range(Constants.DIMENSION):
        for col in range(Constants.DIMENSION):
            row_col_tuple = (row, col)
            if row_col_tuple in Constants.SPECIAL_SQUARES:
                colour = p.Color("gold")
            else:
                colour = colours[
                    ((row + col) % 2)]  # every white space on board is even when r+c, hence remainder
                # will be 0. Same idea for all dark squares being odd, having remainder 1.
            p.draw.rect(screen, colour, p.Rect((col * Constants.SQ_SIZE, row * Constants.SQ_SIZE),
                                               (Constants.SQ_SIZE, Constants.SQ_SIZE)))


def draw_highlighted_squares(screen, gs, valid_moves, sq_selected):
    #  TODO: Could add in highglight of last move made, making use of moveLog[:-1] or something?
    if sq_selected != ():
        row, col = sq_selected
        if gs.board[row][col][0] == (
        "w" if gs.whiteToMove else "b"):  # ensureing square selected is same colour piece as whoevers turn it is
            s = p.Surface((Constants.SQ_SIZE, Constants.SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('green'))
            screen.blit(s, (col * Constants.SQ_SIZE, row * Constants.SQ_SIZE))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    # screen.blit(s, (move.end_col * Constants.SQ_SIZE, move.end_row * Constants.SQ_SIZE))
                    screen.blit(p.image.load(Constants.FILE_PATH_IMAGES + 'highlighted' + Constants.FILE_EXTENSION),
                                p.Rect(((move.end_col * Constants.SQ_SIZE) + (Constants.SQ_SIZE // 4),
                                        move.end_row * Constants.SQ_SIZE),
                                       (Constants.SQ_SIZE, Constants.SQ_SIZE)))


def draw_pieces(screen, board):
    for row in range(Constants.DIMENSION):
        for col in range(Constants.DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(Constants.IMAGES[piece],
                            p.Rect(((col * Constants.SQ_SIZE) + (Constants.SQ_SIZE // 4), row * Constants.SQ_SIZE),
                                   (Constants.SQ_SIZE, Constants.SQ_SIZE)))


def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_board(screen)
    # here this function can be used to add legal move highlighting, piece highlighting (later)
    draw_highlighted_squares(screen=screen, gs=gs, valid_moves=valid_moves,
                             sq_selected=sq_selected)  # toggle this off for performace increase!!
    draw_pieces(screen, gs.board)


def draw_text(screen, text):
    font = p.font.SysFont("Helvitca", 62, True, False)
    text_object = font.render(text, 0, p.Color('Black'))
    text_location = p.Rect(0, 0, Constants.WIDTH, Constants.HEIGHT).move(
        Constants.WIDTH // 2 - text_object.get_width() // 2, Constants.HEIGHT // 2 - text_object.get_height() // 2)
    screen.blit(text_object, text_location)


def main():
    mode = input('Select PyGame GUI or command line [p/c]: ')
    if mode == 'p':
        main_pygame()
    elif mode == 'c':
        main_command_line()


if __name__ == "__main__":
    main()
