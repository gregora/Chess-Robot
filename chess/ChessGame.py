import chess
import chess.engine

import numpy as np


class ChessGame:

    def __init__(self) -> None:
            
        self.board = chess.Board()

        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-ubuntu-x86-64")

        self.mask = np.zeros((8, 8))
        self.mask[0:2, :] = 1
        self.mask[6:8, :] = 2

    def __del__(self):
        self.engine.close()
        self.board.clear()


    def get_move(self, board):

        move_mask = self.get_mask() - ChessGame.mask_from_board(board)

        from_square = 0
        to_square = 0

        for i in range(64):
            if move_mask[i // 8][i % 8] < 0:
                from_square = i
            if move_mask[i // 8][i % 8] > 0:
                to_square = i

        move = chess.Move(from_square, to_square)
        return move.uci()


    def get_mask(self):
        mask = np.zeros((8, 8))
        
        
        ### currently simulated, should get data from Alen
        mask = ChessGame.mask_from_board(self.board)

        move = self.engine.play(self.board, chess.engine.Limit(time=0.01)).move

        mask[move.from_square // 8][move.from_square % 8] = 0
        mask[move.to_square // 8][move.to_square % 8] = 2
        ### end of simulation

        return mask



    def mask_from_board(board):
        mask = np.zeros((8, 8))

        for i in range(8):
            for j in range(8):
                if board.color_at(i * 8 + j) == chess.WHITE:
                    mask[i][j] = 1
                elif board.color_at(i * 8 + j) == chess.BLACK:
                    mask[i][j] = 2

        return mask
    
    def game(self, engine_time = 0.1):

        print("MATCH BEGINS!")
        print(self.board)
        print()

        while not self.board.is_game_over():
            
            # WHITE - COMPUTER
            print("WHITE PLAYS - COMPUTER")
            result = self.engine.play(self.board, chess.engine.Limit(time=engine_time))
            self.board.push(result.move)
            print(self.board)
            print()

            if self.board.is_game_over():
                if self.board.outcome().result() == "1-0":
                    print("WHITE WINS!")
                    return 1
                elif self.board.outcome().result() == "0-1":
                    print("BLACK WINS!")
                    return 2
                else:
                    print("DRAW!")
                    return 0

            # BLACK - HUMAN
            print("BLACK PLAYS - HUMAN")
            move = ""
            while move not in self.board.legal_moves:
                move = self.get_move(self.board)
                try:
                    move = chess.Move.from_uci(move)
                except:
                    print("Illegal move!")
                    move = chess.Move.null()
            self.board.push(move)
            print(self.board)
            print()


            if self.board.is_game_over():
                if self.board.outcome().result() == "1-0":
                    print("WHITE WINS!")
                    return 1
                elif self.board.outcome().result() == "0-1":
                    print("BLACK WINS!")
                    return 2
                else:
                    print("DRAW!")
                    return 0
