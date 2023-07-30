import unittest
from game import Game

class TestGame(unittest.TestCase):
	def setUp(self):
		print("Set up goes here")

	def test_shuffle_cards(self):
		game = Game(4, 1)
		game.start()
		game.new_round()
		deck1 = game._players
		game.next_round()
		game.new_round()
		deck2 = game._players

		self.assertNotEqual(deck1, deck2)

	def test_tick_winner_right(self):
		game = Game(4, 1)
		game.start()
		game.new_round()
		game._players = [["s2"],["s7"],["s8"],["sA"]]
		game.play_tick_card("s2")
		game.next_turn()
		game.play_tick_card("s7")
		game.next_turn()
		game.play_tick_card("s8")
		game.next_turn()
		game.play_tick_card("sA")
		game.next_turn()
		game.calculate_tick_winner()
		winner = game.get_tick_winner()

		self.assertEqual(winner, 4)

	def test_tick_winner_right_with_trump(self):
		game = Game(4, 1)
		game.start()
		game.new_round()
		game._players = [["d2"],["s7"],["s8"],["sA"]]
		game._trump = "d (diamonds)"
		game.play_tick_card("d2")
		game.next_turn()
		game.play_tick_card("s7")
		game.next_turn()
		game.play_tick_card("s8")
		game.next_turn()
		game.play_tick_card("sA")
		game.next_turn()
		game.calculate_tick_winner()
		winner = game.get_tick_winner()

		self.assertEqual(winner, 1)

	def test_points_calculation_right(self):
		game = Game(4, 2)
		game.start()
		game.new_round()
		game._players = [["d2","d3"],["s7","s4"],["s8","sJ"],["sA","sK"]]
		game._trump = "d (diamonds)"

		game.player_bid(2)
		game.next_turn()
		game.player_bid(0)
		game.next_turn()
		game.player_bid(0)
		game.next_turn()
		game.player_bid(1)
		game.next_turn()

		game.set_turn_pointer_at_tick_begin()

		game.play_tick_card("d2")
		game.next_turn()
		game.play_tick_card("s7")
		game.next_turn()
		game.play_tick_card("s8")
		game.next_turn()
		game.play_tick_card("sA")
		game.next_turn()

		game.calculate_tick_winner()

		game.set_turn_pointer_at_tick_begin()

		game.play_tick_card("d3")
		game.next_turn()
		game.play_tick_card("s4")
		game.next_turn()
		game.play_tick_card("sJ")
		game.next_turn()
		game.play_tick_card("sK")
		game.next_turn()

		game.calculate_tick_winner()

		game.calculate_points()

		self.assertEqual(game._points_table, [4,2,2,-3])

	def test_compare_function(self):
		game = Game(4, 2)

		card1 = "s2"
		card2 = "sA"

		higher = game.compare_higher(card1,card2,"s","s")
		self.assertEqual(higher, "sA")

	def test_compare_function2(self):
		game = Game(4, 2)

		card1 = "s2"
		card2 = "dA"

		higher = game.compare_higher(card1,card2,"d","s")
		self.assertEqual(higher, "s2")

	def test_compare_function3(self):
		game = Game(4, 2)

		card1 = "c2"
		card2 = "cA"

		higher = game.compare_higher(card1,card2,"s","s")
		self.assertEqual(higher, None)

	def test_player_amount_setting(self):
		game = Game(4, 2)

		players = game.get_player_count()
		self.assertEqual(players, 4)

	def test_round_amount_setting(self):
		game = Game(4, 2)

		rounds = game.get_max_cards()
		self.assertEqual(rounds, 2)

