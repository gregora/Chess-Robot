from ChessGame import ChessGame


game = ChessGame()
game.game(engine_time=0.01)
game.__del__()
