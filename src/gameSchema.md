## Formatting

Suits are a single letter: "s" , "d" , "h" , or "c"

Cards are thus: "s2" , "d8" , "h10" , "hA" , or "cJ"

## Game function fundamentals

```
## To initialize a new game

game = Game(player_count, max_cards)
game.start()

## To run through gameplay

for i in range (0, game.get_max_cards()):
	self.new_round()

	-->		game.new_round()


	self.bid()

	-->		for i in range(0, game.get_player_count()):
				bid = get_bid_input() # input some positive integer

				game.player_bid(bid)
				game.next_turn()


	self.play_tick()

	-->		# loop that plays through all ticks in a round
			for i in range(0, game.get_round()):
				game.set_turn_pointer_at_tick_begin()
				
				# each players move
				for j in range(0, game.get_player_count()):
					self.play_turn()

					-->		card = self.get_card_input() # input some card
		
							game.play_tick_card(card)
							game.next_turn()
				
				game.calculate_tick_winner()

			game.calculate_points()

	game.next_round()

## After which the game finishes
```