## Formatting

Suits are a single letter: "s" , "d" , "h" , or "c"

Cards are thus: "s2" , "d8" , "h10" , "hA" , or "cJ"

## Game function fundamentals

```
## To initialize a new game

self._game = Game(player_count, max_cards)
self._game.start()

## To run through gameplay

for i in range (0, self._game._max_cards):
	self.new_round()

	-->		self._game.new_round()


	self.bid()

	-->		for i in range(0, self._game._player_count):
				bid = get_bid_input() # input some positive integer

				self._game.player_bid(bid)
				self._game.next_turn()


	self.play_tick()

	-->		# loop that plays through all ticks in a round
			for i in range(0, self._game.get_round()):
				self._game.set_turn_pointer_at_tick_begin()
				
				# each players move
				for j in range(0, self._game._player_count):
					self.play_turn()

					-->		card = self.get_card_input() # input some card in the required format
		
							self._game.play_tick_card(card)
							self._game.next_turn()
				
				winner = self._game.calculate_and_return_tick_winner()

			self._game.calculate_points()

	self._game.next_round()

## After which the game finishes
```