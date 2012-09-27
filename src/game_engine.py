import sys
import game

class GameEngine:

  QUIT = -1

  def __init__(self, board, io, ai, board_analyzer):
    self.board = board
    self.io = io
    self.ai = ai
    self.board_analyzer = board_analyzer

  def start(self, play_type):
    self.play_type = play_type
    self.player_one_turn = True
    while not(self.board_analyzer.game_over(self.board)):
      self.io.display_board(self.board)
      self.place_move()
    self.io.display_board(self.board)
    self.io.display_game_over_message(self.board_analyzer.winner)

  def place_move(self):
    if self.player_one_turn:
      move = self.get_player_one_move()
      if self.available(move):
        self.board[move] = 'X'
        self.player_one_turn = False
    else:
      move = self.get_player_two_move() 
      if self.available(move):
        self.board[move] = 'O'
        self.player_one_turn = True

  def get_player_one_move(self):
    if self.human_is_playing():
      move = self.io.get_move(self.board)
      if move == self.QUIT:
        sys.exit()
    else:
      move = self.ai.get_move(self.board, self.ai.PLAYER_X)
    return move

  def get_player_two_move(self):
    if self.ai_is_playing():
      move = self.ai.get_move(self.board, self.ai.PLAYER_O)
    else:
      move = self.io.get_move(self.board)
      if move == self.QUIT:
        sys.exit()
    return move

  def human_is_playing(self):
    return False if self.play_type == game.AI_VS_AI else True

  def ai_is_playing(self):
    return False if self.play_type == game.PLAYER_VS_PLAYER else True

  def available(self, move):
    if self.board[move] == 'X':
      return False
    if self.board[move] == 'O':
      return False
    return True
