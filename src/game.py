import random

deck_of_cards = ["d2","d3","d4","d5","d6","d7","d8","d9","d10","dJ","dQ","dK","dA",
		 "s2","s3","s4","s5","s6","s7","s8","s9","s10","sJ","sQ","sK","sA",
		 "c2","c3","c4","c5","c6","c7","c8","c9","c10","cJ","cQ","cK","cA",
		 "h2","h3","h4","h5","h6","h7","h8","h9","h10","hJ","hQ","hK","hA"]

card_ranking = ["2","3","4","5","6","7","8","9","1","J","Q","K","A"]

class Game:
	def __init__(self, players, max_cards):
		self._player_count = int(players)
		self._max_cards = int(max_cards)
		self._round = None
		self._trump = None
		self._players = []
		self._bids = [ [ [] for j in range(0,self._max_cards)] for i in range(0,self._player_count)]
		self._deck = deck_of_cards
		self._turn_pointer = 0
		self._tick_cards = []
		self._tick_cards_won = [ 0 for i in range(0,self._player_count)]
		self._tick_suit = None
		self._tick_highest_player = 1
		self._points_table = [ 0 for i in range(0,self._player_count)]
		self._last_tick_winner = 1
		self._last_round_starter = 1
			  
	def start(self):
		self._round = self._max_cards
		
	def get_round(self):
		return self._round
	
	def get_trump(self):
		return self._trump
	
	def get_player_turn(self):
		return self._turn_pointer + 1
	
	def get_bids(self):
		return self._bids
	
	def set_bids(self, table):
		self._bids = table

	def get_tick_cards(self):
		return self._tick_cards
	
	def play_tick_card(self, card):
		self._tick_cards.append(card)
		if len(self._tick_cards)!=1:
			answer = self.compare_higher(card,self._tick_cards[self._tick_highest_player-1],self._tick_suit,self._trump[0])
			if answer!=None:
				if answer==card:
					self._tick_highest_player = len(self._tick_cards)

	def clear_tick_cards(self):
		self._tick_cards = []

	def clear_tick_cards_won(self):
		self._tick_cards_won = [ 0 for i in range(0,self._player_count)]

	def set_tick_suit(self, suit):
		self._tick_suit = suit

	def get_tick_suit(self):
		return self._tick_suit

	def get_tick_highest_player(self):
		return self._tick_highest_player
	
	def set_tick_winner(self, player):
		self._tick_cards_won[player-1]+=1
		self._last_tick_winner = player

	def get_last_tick_winner(self):
		return self._last_tick_winner
	
	def clear_last_tick_winner(self):
		self._last_round_starter += 1
		self._last_tick_winner = self._last_round_starter

	def get_last_round_starter(self):
		return self._last_round_starter

	def clear_tick_highest_player(self):
		self._tick_highest_player = 1

	def get_tick_winners(self):
		return self._tick_cards_won
	
	def get_points_table(self):
		return self._points_table
	
	def set_points_table(self,table):
		self._points_table = table
	
	def next_turn(self):
		if self._turn_pointer == self._player_count-1:
			self._turn_pointer = 0
		else:
			self._turn_pointer += 1

	## in this variation rounds go downwards
	def next_round(self):
		self._round -= 1
	
	def new_round(self):
		self.shuffle_deck()
		self.deal_cards()
		self.pick_trump()

	def shuffle_deck(self):
		self._deck = deck_of_cards
		random.shuffle(self._deck)

	def deal_cards(self):
		hands = []
		for i in range(0,self._player_count):
			hands.append([])
		for i in range(0,self.get_round()):
			for j in range(0,self._player_count):
				card = random.choice(self._deck)
				self._deck.remove(card)
				hands[j].append(card)
		self._players = hands

	def set_turn_pointer_at_round_begin(self):
		self._turn_pointer = self._last_round_starter - 1

	def set_turn_pointer_at_tick_begin(self):
		self._turn_pointer = self._last_tick_winner - 1

	def pick_trump(self):
		trump = random.choice(["d (diamonds)","s (spades)","c (clubs)","h (hearts)"])
		self._trump = trump

	def compare_higher(self, card1, card2, play_suit, trump_suit):
		if card1[0] == card2[0]:
			if card1[0] != play_suit and card1[0] != trump_suit:
				return None
			else:
				card1_index = card_ranking.index(card1[1])
				card2_index = card_ranking.index(card2[1])
				if card1_index>card2_index:
					return card1
				else:
					return card2
		else:
			if card1[0]==trump_suit:
				return card1
			elif card2[0]==trump_suit:
				return card2
			elif card1[0]==play_suit:
				return card1
			elif card2[0]==play_suit:
				return card2
			else:
				return None
