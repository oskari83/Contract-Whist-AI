from consoleIO import ConsoleIO
from game import Game

deck_of_cards = ["d2","d3","d4","d5","d6","d7","d8","d9","d10","dJ","dQ","dK","dA",
		 "s2","s3","s4","s5","s6","s7","s8","s9","s10","sJ","sQ","sK","sA",
		 "c2","c3","c4","c5","c6","c7","c8","c9","c10","cJ","cQ","cK","cA",
		 "h2","h3","h4","h5","h6","h7","h8","h9","h10","hJ","hQ","hK","hA"]

## big todo is to give the start of the next round to the winner of the tick
## also to check that player is legally allowed to play that card
## and type checking everywhere is missing

class GameManager:
	def __init__(self):
		self._io = ConsoleIO()
		self._game = None

	def start(self):
		self.print_initial()

		while True:
			if self._game:
				for i in range (0, self._game._max_cards):
					self.new_round()
					self._game.set_turn_pointer_at_round_begin()
					self.bid()
					self.play_tick()
					self._game.next_round()
				self._io.cout("Game finished!")
				self._game = None
			else:
				self.print_instructions()
				command = self._io.cin("Command: ")

				if(command=="1"):
					self.new_game()
				elif(command=="2"):
					self._io.newline()
					self._io.cout("Bye, see you soon!")
					break

	def print_initial(self):
		for i in range(0,20):
			self._io.newline()
		self._io.cout("-------------------------------------------------")
		self._io.cout("|		Contract Whist v1		|")
		self._io.cout("-------------------------------------------------")

	def print_instructions(self):
		self._io.newline()
		self._io.cout("Welcome, Press:")
		self._io.newline()
		self._io.cout("[1]	To Play a Game")
		self._io.cout("[2]	To Exit")
		self._io.newline()

	def new_game(self):
		for i in range(0,20):
			self._io.newline()

		while True:
			self._io.cout("Give the number of players (3-5):")

			try:
				player_count = int(self._io.cin("Command: "))
			except:
				self._io.newline()
				self._io.cout("Error, please give an integer")
				self._io.newline()
				continue

			if player_count>=3 and player_count<=5:
				break
			else:
				self._io.newline()
				self._io.cout("Error, please give a number between 3 and 5")
				self._io.newline()
		
		while True:
			self._io.cout("Give the starting number of cards (1-10):")

			try:
				max_cards = int(self._io.cin("Command: "))
			except:
				self._io.newline()
				self._io.cout("Error, please give an integer")
				self._io.newline()
				continue

			if max_cards>=1 and max_cards<=10:
				break
			else:
				self._io.newline()
				self._io.cout("Error, please give a number between 1 and 10")
				self._io.newline()

		self._io.cout("Starting game...")

		self._game = Game(player_count,max_cards)
		self._game.start()

	def new_round(self):
		self._io.newline()

		self._game.new_round()

		self._io.cout(f"Round {self._game.get_round()} (dealing {self._game.get_round()} cards)")
		self._io.newline()
		self.print_hands()
		self.print_trump()

	def bid(self):
		bidtable = self._game.get_bids()

		current_bid_sum = 0
		max_bid_sum = self._game.get_round()

		for i in range(0, self._game._player_count):
			bid = None

			if i == self._game._player_count-1:
				cannot_bid = max_bid_sum - current_bid_sum
				while True:
					self._io.cout(f"Player {self._game.get_player_turn()}'s bid (cannot bid {cannot_bid}): ")

					try:
						bid = int(self._io.cin("Command: "))
					except:
						self._io.newline()
						self._io.cout("Error, please give an integer")
						self._io.newline()
						continue

					if bid!=cannot_bid:
						break
					elif bid<0:
						self._io.newline()
						self._io.cout(f"Error, please bid a positive amount")
						self._io.newline()
					else:
						self._io.newline()
						self._io.cout(f"Error! You cannot bid {cannot_bid}.")
						self._io.newline()
			else:
				while True:
					self._io.cout(f"Player {self._game.get_player_turn()}'s bid: ")

					try:
						bid = int(self._io.cin("Command: "))
					except:
						self._io.newline()
						self._io.cout("Error, please give an integer")
						self._io.newline()
						continue
					
					if bid<0:
						self._io.newline()
						self._io.cout(f"Error, please bid a positive amount")
						self._io.newline()
					else:
						break

			bidtable[i][self._game.get_round()-1] = bid
			current_bid_sum += bid
			self._game.next_turn()

		self._game.set_bids(bidtable)

		self._io.newline()
		self.print_round_bids()

		self._io.cout("Lets start the round!")
		self._io.newline()

	def play_tick(self):
		for i in range(0, self._game.get_round()):

			self._io.cout(f"Tick {i+1} (Trump: {self._game.get_trump()}): ")
			self._io.newline()

			self._game.set_turn_pointer_at_tick_begin()

			for j in range(0, self._game._player_count):
				self.play_turn()
			self.print_tick_cards()

			## pray that this works
			winner = self._game.get_tick_highest_player() ## gives like player 3 (ind)  (4) 2
			delta_in_starters_index = 0 ## gives like player 3 (actual) (1) 2
			steps = self._game.get_last_tick_winner()-1
			for i in range(0,steps):
				if(delta_in_starters_index-1)<0:
					delta_in_starters_index=self._game._player_count-1
				else:
					delta_in_starters_index-=1
			player_one_index = delta_in_starters_index
			if winner-1 >= player_one_index:
				winner = winner - player_one_index
			else:
				winner = self._game._player_count - (player_one_index-winner)

			## hopefully winner is now correct

			self._io.cout(f"Tick winner is Player {winner}")
			self._game.set_tick_winner(winner)
			self._game.clear_tick_cards()
			self._game.clear_tick_highest_player()
			#self._game.clear_last_tick_winner()
			self._io.newline()
			self.print_tick_situation()

		## set points
		bid_table = self._game.get_bids()
		round = self._game.get_round()
		tick_winners = self._game.get_tick_winners()
		points_table = self._game.get_points_table()
		for i in range(0,self._game._player_count):
			if bid_table[i][round-1] == tick_winners[i]:
				points_table[i] += 2
				points_table[i] += bid_table[i][round-1]
			else:
				points_table[i] -= 2
				points_table[i] -= abs(bid_table[i][round-1]-tick_winners[i])
		self._game.set_points_table(points_table)
		self.print_points_situation()
		self._game.clear_tick_cards_won()
		self._game.clear_last_tick_winner()

	def print_hands(self):
		self._io.cout("Hands:")
		for i in range(0, self._game._player_count):
			self._game._players[i].sort()
			hand = ""
			for j in range(0, self._game.get_round()):
				hand += str(self._game._players[i][j])
				hand += " "
			self._io.cout(f"Player {i+1}: " + hand[0:len(hand)-1])
		self._io.newline()

	def print_tick_cards(self):
		tick_cards = self._game.get_tick_cards()
		s = ""
		for i in range(0,len(tick_cards)):
			s += tick_cards[i]
			s += " "
		self._io.cout("Cards played: ")
		self._io.cout(s)
		self._io.newline()

	def print_trump(self):
		self._io.cout(f"Trump: {self._game.get_trump()}")
		self._io.newline()

	def print_round_bids(self):
		self._io.cout("Bids:")
		for i in range(0, self._game._player_count):
			self._io.cout(f"Player {i+1}: " + str(self._game.get_bids()[i][self._game.get_round()-1]))
		self._io.newline()

	def play_turn(self):
		player = self._game.get_player_turn()
		player_hand = self._game._players[player-1]
		self._io.cout(f"Player {player}'s turn")

		while True:
			self._io.cout(f"Pick a card to play:")
			self.print_player_hand(player)
			card = self._io.cin("Command: ")
			if card in player_hand:
				if player==self._game.get_last_tick_winner() or card[0]==self._game.get_tick_suit():
					break
				else:
					suits_in_hand = []
					for c in player_hand:
						suits_in_hand.append(c[0])
					
					tick_suit = self._game.get_tick_suit()
					if tick_suit in suits_in_hand:
						self._io.newline()
						self._io.cout(f"Error, you have a card of the suit that has to be played")
						self._io.newline()
					else:
						break
			else:
				self._io.newline()
				self._io.cout("Error, select a card that is in the hand")
				self._io.newline()
		
		self._game._players[player-1].remove(card)
		if player == self._game.get_last_tick_winner():
			self._game.set_tick_suit(card[0])
			text = None
			if card[0] == "s":
				text = "s (spades)"
			elif card[0] == "d":
				text = "d (diamonds)"
			elif card[0] == "c":
				text = "c (clubs)"
			elif card[0] == "h":
				text = "h (hearts)"
			self._io.newline()
			self._io.cout(f"This round's suit is {text}")
		self._game.play_tick_card(card)
		self._game.next_turn()
		self._io.newline()

	def print_player_hand(self, player):
		self._io.cout(self._game._players[player-1])

	def print_tick_situation(self):
		self._io.cout("Tick situation: [bids] [ticks won]")
		bid_table = self._game.get_bids()
		round = self._game.get_round()
		tick_winners = self._game.get_tick_winners()
		for i in range(0, self._game._player_count):
			self._io.cout(f"Player {i+1}: " + str(bid_table[i][round-1]) + " " + str(tick_winners[i]))
		self._io.newline()

	def print_points_situation(self):
		points_table = self._game.get_points_table()
		self._io.cout("Point situation: ")
		for i in range(0, self._game._player_count):
			self._io.cout(f"Player {i+1}: " + str(points_table[i]))
		self._io.newline()
