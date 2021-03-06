import unittest
import sys
import src.game

from src.game_engine import GameEngine
from src.board import Board
from mock import *

class TestGameEngine(unittest.TestCase):

  def setUp(self):
    self.board = Board(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    self.mock_io = Mock()
    self.mock_ai = Mock()
    self.mock_board_analyzer = Mock()
    self.moves = [2, 3]
    self.mock_io.get_move.side_effect = self.moves
    self.game_over_values = [False, True]
    self.mock_board_analyzer.game_over.side_effect = self.game_over_values
    self.engine = GameEngine(self.mock_io, self.mock_ai, self.mock_board_analyzer)

  def test_start_displays_board(self):
    self.engine.start(src.game.PLAYER_VS_PLAYER, self.board)
    self.mock_io.assert_has_calls([call.display_board(self.board)])

  def test_start_gets_player_move(self):
    self.engine.start(src.game.PLAYER_VS_PLAYER, self.board)
    self.mock_io.assert_has_calls([call.get_move(self.board)])

  def test_start_puts_move_on_the_board(self):
    self.engine.start(src.game.PLAYER_VS_PLAYER, self.board)
    self.assertEqual(self.board.get_square(self.moves[0]), 'X')

  def test_start_checks_if_game_is_over(self):
    self.engine.start(src.game.PLAYER_VS_PLAYER, self.board)
    self.mock_board_analyzer.assert_has_calls([call.game_over(self.board)])

  def test_start_displays_game_over_message_when_game_is_over(self):
    self.engine.start(src.game.PLAYER_VS_PLAYER, self.board)
    self.mock_io.assert_has_calls(
        [call.display_game_over_message(self.mock_board_analyzer.winner)])

  def test_place_move_allows_two_players_to_play(self):
    game_over_values = [False, False, True]
    self.mock_board_analyzer.game_over.side_effect = game_over_values
    self.engine.start(src.game.PLAYER_VS_PLAYER, self.board)
    self.assertEqual(self.board.get_square(self.moves[0]), 'X')
    self.assertEqual(self.board.get_square(self.moves[1]), 'O')

  def test_place_move_does_not_allow_move_to_be_placed_in_same_square(self):
    self.moves = [2, 2]
    self.mock_io.get_move.side_effect = self.moves
    game_over_values = [False, False, True]
    self.mock_board_analyzer.game_over.side_effect = game_over_values
    self.mock_board_analyzer.square_is_available.side_effect = [True, False]
    self.engine.start(src.game.PLAYER_VS_PLAYER, self.board)
    self.assertEqual(self.board.get_square(self.moves[0]), 'X')
    self.assertEqual(self.board.get_square(self.moves[1]), 'X')

  def test_place_move_allows_ai_to_move_second(self):
    ai_moves = [5]
    self.mock_ai.get_move.side_effect = ai_moves
    game_over_values = [False, False, True]
    self.mock_board_analyzer.game_over.side_effect = game_over_values
    self.engine.start(src.game.PLAYER_VS_AI, self.board)
    self.mock_ai.assert_has_calls([call.get_move(self.board, self.mock_ai.PLAYER_O)])

  def test_start_allows_ai_to_play_against_itself(self):
    ai_moves = [5, 6]
    self.mock_ai.get_move.side_effect = ai_moves
    game_over_values = [False, False, True]
    self.mock_board_analyzer.game_over.side_effect = game_over_values
    self.engine.start(src.game.AI_VS_AI, self.board)
    self.mock_ai.assert_has_calls([call.get_move(self.board, self.mock_ai.PLAYER_X),
                                   call.get_move(self.board, self.mock_ai.PLAYER_O)])

