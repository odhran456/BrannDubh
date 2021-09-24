from operator import sub
from operator import add
from BrannDubh import Constants


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

        self.moveFunctions = {"P": self.get_regular_moves, "K": self.get_king_moves}
        self.whiteToMove = True
        self.moveLog = []
        self.black_win_condition = False
        self.white_win_condition = False

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

        # here im finding out what is the enemy piece given the turn. i.e. white to move, black is enemy
        if self.whiteToMove is True:
            enemy_pieces = ["bP", "bK"]
            ally_pieces = ["wP"]
        elif self.whiteToMove is False:
            enemy_pieces = ["wP"]
            ally_pieces = ["bP", "bK"]

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
            enemy_row_val, enemy_col_val = square  # check every square thats left in the squares to check

            if self.board[enemy_row_val][enemy_col_val] in enemy_pieces:
                enemy_piece_info.append([self.board[enemy_row_val][enemy_col_val], square])  # [piece, location]

        piece_location = (move.end_row, move.end_col)

        # here we're going to check for every enemy we are orthogonal to, is there an ally on the opposite side of
        # that enemy

        for enemy in enemy_piece_info:  # for every enemy we are orthogonal to:
            enemy_piece, enemy_piece_location = enemy
            direction = tuple(map(sub, enemy_piece_location, piece_location))  # get what direction we are to them
            ally_location = tuple(map(add, enemy_piece_location, direction))  # add this tuple to their posn to know
            # which square we are checking to see if we have an ally on

            # this checks if you're capturing a piece against the corner
            if (piece_location in Constants.FAR_CORNER_SQUARES) and (
                    enemy_piece_location in Constants.ADJACENT_CORNER_SQUARES):
                captured_piece_info.append((enemy_piece, enemy_piece_location))
                if enemy_piece == "bK":
                    self.white_win_condition = True  # it's faster to check here where we have enemy piece if it's the King
                # so here we checked if you're two squares adjacently away from the corner, and the enemy is one
                # square adjacently away from the corner (which basically means the enemy is between you and the
                # corner). The second check of checking if the enemy is in the list of squares adjacent to the corner
                # may not seem strict enough but recall an enemy_piece can only exist if it satisfies the rules in
                # squares_to_check, so actually everything works

            # this checks if you're capturing a piece by having an ally on the opposite side of the enemy
            elif 0 <= ally_location[0] <= 6 and 0 <= ally_location[1] <= 6:  # don't check for allies outside the board
                if self.board[ally_location[0]][ally_location[1]] in ally_pieces:  # if we have an ally on the opposite
                    # square
                    captured_piece_info.append((enemy_piece, enemy_piece_location))  # note a piece as captured
                    if enemy_piece == "bK":
                        self.white_win_condition = True

            # In some cases the throne is hostile, which means that it can replace one of the two pieces involved in
            # a capture. The throne is never hostile to the king, always hostile to the attackers, and only hostile
            # to the defenders when the king is not occupying it.

            # Here is logic for throne hostile to defenders (but not king)
            if (self.whiteToMove is True) and (
                    self.board[Constants.CENTRE_SQUARE[0][0]][Constants.CENTRE_SQUARE[0][1]] != "bK") and (
                    enemy_piece != "bK") and (piece_location in Constants.FAR_CENTRE_SQUARE) and (
                    enemy_piece_location in Constants.ADJACENT_CENTRE_SQUARE):
                captured_piece_info.append((enemy_piece, enemy_piece_location))
            # here is logic throne hostile to attackers
            elif (self.whiteToMove is False) and (piece_location in Constants.FAR_CENTRE_SQUARE) and (
                    enemy_piece_location in Constants.ADJACENT_CENTRE_SQUARE):
                captured_piece_info.append((enemy_piece, enemy_piece_location))

        return captured_piece_info

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"  # update pieces old square to be blank

        pieces_to_remove = self.check_for_captures(move)
        for piece in pieces_to_remove:  # delete any captured pieces
            p, loc = piece
            self.board[loc[0]][loc[1]] = "--"

        self.board[move.end_row][move.end_col] = move.piece_moved  # update your new square to have your moved piece

        if move.piece_moved == "bK":  # check if black won the game by getting king to corner
            king_move = (move.end_row, move.end_col)
            if king_move in Constants.CORNER_SQUARES:
                self.black_win_condition = True

        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        print(move.get_algebraic_notation())

    def get_all_possible_moves(self):  # scan the whole board and get every legal move combination
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):  # num cols in given row
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (
                        turn == 'b' and not self.whiteToMove):  # here the code has bumped into a piece in its search of the board, and if the colour of the piece aligns with whoevers turn it currently is, the possible moves for that piece will be considered
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)  # calls appropriate move function based on piece type
        print(len(moves), moves)
        return moves

    def get_regular_moves(self, row, col,
                          moves):  # gets all legal moves for piece located at (r,c) and adds to legal moves list
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up left down right
        for d in directions:
            for i in range(1, Constants.DIMENSION):
                potential_end_row = row + (d[0] * i)
                potential_end_col = col + (d[1] * i)

                if 0 <= potential_end_row < Constants.DIMENSION and 0 <= potential_end_col < Constants.DIMENSION:
                    end_square = self.board[potential_end_row][potential_end_col]
                    if end_square == '--' and (potential_end_row,
                                               potential_end_col) not in Constants.SPECIAL_SQUARES:  # these pieces cant access special squares
                        moves.append(Move((row, col), (potential_end_row, potential_end_col), self.board))
                    elif (potential_end_row, potential_end_col) == Constants.CENTRE_SQUARE[0] and end_square == '--':
                        continue  # we dont want to jump out of the loop when it hits special sqaure in previous if statement if it just went to a break statement then, but also if the king is in the centre we dont want to just jump over this tile and keep checking on the other side
                    else:
                        break
                else:
                    break

    def get_king_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up left down right
        for d in directions:
            for i in range(1, Constants.DIMENSION):
                potential_end_row = row + (d[0] * i)
                potential_end_col = col + (d[1] * i)

                if 0 <= potential_end_row < Constants.DIMENSION and 0 <= potential_end_col < Constants.DIMENSION:
                    end_square = self.board[potential_end_row][potential_end_col]
                    if end_square == '--':
                        moves.append(Move((row, col), (potential_end_row, potential_end_col), self.board))
                    else:
                        break
                else:
                    break


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
        self.moveID = (self.start_row * 1000) + (self.start_col * 100) + (self.end_row * 10) + (
            self.end_col)  # unique 4 digit numb for move

    # Overridding the equals method, to compare a Move against a move (comparing two objects, instances of the Move class)
    def __eq__(self, other):
        if isinstance(other,
                      Move):  # only check when the other item is an instance of Move class, dont compare numbers to Move object
            return self.moveID == other.moveID  # i could compare both objects' return vlues of their algebraic notation instead
        return False

    def __repr__(self):
        return '[(' + str(self.start_row) + ', ' + str(self.start_col) + ') -> (' + str(self.end_row) + ', ' + str(
            self.end_col) + ')]'

    def get_algebraic_notation(self):
        # TODO: add notation with capturese etc, like in: http://aagenielsen.dk/visspil.php , maybe move this funct to GameState to take advantage of captures func for like nxf3
        return self.get_rank_file(self.start_row, self.start_col) + ' - ' + self.get_rank_file(self.end_row,
                                                                                               self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
