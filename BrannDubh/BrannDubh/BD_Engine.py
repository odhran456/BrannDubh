from operator import sub
from operator import add


class GameState:
    def __init__(self):
        self.board = [
            ["--", "--", "--", "wP", "--", "--", "--"],
            ["--", "--", "--", "wP", "--", "--", "--"],
            ["--", "--", "--", "bP", "--", "--", "--"],
            ["wP", "wP", "bP", "bK", "bP", "wP", "wP"],
            ["--", "--", "--", "bP", "--", "--", "--"],
            ["--", "--", "--", "wP", "--", "--", "--"],
            ["--", "--", "--", "wP", "--", "--", "--"]
        ]
        self.whiteToMove = True
        self.moveLog = []

    # TODO: here i need to add in clause about special squares being capture pieces
    def check_for_captures(self, move):
        # first after a piece moves, check the orthogonal squares to it to see if it's even in contact with enemy
        # pieces. these are the orthogonal squares we will have to check vv
        squares_to_check = [(move.end_row - 1, move.end_col), (move.end_row + 1, move.end_col),
                            (move.end_row, move.end_col + 1), (move.end_row, move.end_col - 1)]
        enemy_pieces = []
        ally_pieces = []
        enemy_piece_info = []
        direction = ()
        ally_location = ()
        captured_piece_info = []

        # remove orthogonal squares that can't exist because maybe you're at the side of the board
        if move.end_row == 0:
            squares_to_check.remove((move.end_row - 1, move.end_col))
        elif move.end_row == 6:
            squares_to_check.remove((move.end_row + 1, move.end_col))
        if move.end_col == 0:
            squares_to_check.remove((move.end_row, move.end_col - 1))
        elif move.end_col == 6:
            squares_to_check.remove((move.end_row, move.end_col + 1))

        for square in squares_to_check:
            row_val, col_val = square

            # here im finding out what is the enemy piece given the turn. i.e. white to move, black is enemy
            if self.whiteToMove is True:
                enemy_pieces = ["bP", "bK"]
                ally_pieces = ["wP"]
            elif self.whiteToMove is False:
                enemy_pieces = ["wP"]
                ally_pieces = ["bP", "bK"]

            if self.board[row_val][col_val] in enemy_pieces:
                enemy_piece_info.append([self.board[row_val][col_val], square])  # [piece, location]

        piece_location = (move.end_row, move.end_col)

        # here we're going to check for every enemy we are orthogonal to, is there an ally on the opposite side of
        # that enemy

        for enemy in enemy_piece_info:  # for every enemy we are orthogonal to:
            enemy_piece, enemy_piece_location = enemy
            direction = tuple(map(sub, enemy_piece_location, piece_location))  # get what direction we are to them
            ally_location = tuple(map(add, enemy_piece_location, direction))  # add this to their posn to know which
            # square we are checking to see if we have an ally on

            if 0 <= ally_location[0] <= 6 and 0 <= ally_location[1] <= 6:  # don't check for allies outside the board
                if self.board[ally_location[0]][ally_location[1]] in ally_pieces:  # if we have an ally on the opposite
                    # square
                    captured_piece_info.append((enemy_piece, enemy_piece_location))  # note a piece as captured

        return captured_piece_info

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"  # update pieces old square to be blank

        pieces_to_remove = self.check_for_captures(move)
        for piece in pieces_to_remove:  # delete any captured pieces
            p, loc = piece
            self.board[loc[0]][loc[1]] = "--"

        self.board[move.end_row][move.end_col] = move.piece_moved  # update your new square to have your moved piece
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove


class Move:
    ranks_to_rows = {"1": 6, "2": 5, "3": 4, "4": 3, "5": 2, "6": 1, "7": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]  # TODO: note in brann dubh: captured piece is not in
        # square you are moving to. however he does en passant i will need to look into. i'm doing this in
        # chek_for_captures()

        # TODO: win conditions: OR(piece_moved == bK && end_square in corner_squares, piece_captured == bK)

    def get_algebraic_notation(self):
        # TODO: add notation with capturese etc, like in: http://aagenielsen.dk/visspil.php , maybe move this funct to GameState to take advantage of captures func for like nxf3
        return self.get_rank_file(self.start_row, self.start_col) + ' - ' + self.get_rank_file(self.end_row,
                                                                                               self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
