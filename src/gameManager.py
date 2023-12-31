from consoleIO import ConsoleIO
from game import Game

class GameManager:
    def __init__(self):
        self._io = ConsoleIO()
        self._game = None

    def start(self):
        self.print_initial()

        while True:
            if self._game:
                # runs game for determined amount of rounds
                for i in range (0, self._game.get_max_cards()):
                    self.new_round()
                    self.bid()
                    self.play_tick()
                    self._game.next_round()
                # can add code to sum up points at the end
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

    def new_game(self):
        game_setup_tuple = self.get_player_game_setup_input()

        self._game = Game(game_setup_tuple[0],game_setup_tuple[1])
        self._game.start()

    def new_round(self):
        self._game.new_round()

        self.print_round_information()
        self.print_hands()
        self.print_trump()

    def bid(self):
        for i in range(0, self._game.get_player_count()):
            bid = self.get_player_bid_input(i)

            self._game.player_bid(bid)
            self._game.next_turn()

        self.print_round_bids()

    def play_tick(self):
        # loop that plays through all ticks in a round
        for i in range(0, self._game.get_round()):

            self._io.cout(f"Tick {i+1} (Trump: {self._game.get_trump()}): ")
            self._io.newline()

            self._game.set_turn_pointer_at_tick_begin()

            # each players move
            for j in range(0, self._game.get_player_count()):
                self.play_turn()

            self.print_tick_cards()

            # important to realise this calculate function does a lot in the game-class
            self._game.calculate_tick_winner()

            self._io.cout(f"Tick winner is Player {self._game.get_tick_winner}")

            self.print_tick_situation()

        self._game.calculate_points()

        self.print_points_situation()

    def play_turn(self):
        card_input = self.get_player_turn_input()

        self._game.play_tick_card(card_input)
        self._game.next_turn()

        self._io.newline()

    def get_player_bid_input(self, index):
        bid = None

        # if we are last, runs this
        if index == self._game.get_player_count()-1:
            # enforces a rule, making sure the player does not cheat
            # I think the Game class does not need to be the enforcer
            # I think that is left to UI and manager
            # also because it might be useful at points to allow the AI to cheat
            cannot_bid = self._game.get_round() - self._game.get_current_bidsum()
            while True:
                self._io.cout(
                    f"Player {self._game.get_player_turn()}'s bid (cannot bid {cannot_bid}): "
                    )

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

        return bid

    def get_player_turn_input(self):
        player = self._game.get_player_turn()
        player_hand = self._game._players[player-1]
        self._io.cout(f"Player {player}'s turn")

        while True:
            self._io.cout(f"Pick a card to play:")
            self.print_player_hand(player)

            #this is the main input
            card = self._io.cin("Command: ")

            #all of this just checks the player is making a legal move
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

        if player == self._game.get_last_tick_winner():
            self.print_this_rounds_suit(card)

        return card

    def get_player_game_setup_input(self):
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

        return (player_count,max_cards)


    ### UI print functions that simply utilize get-functions from the Game-class

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

    def print_hands(self):
        self._io.cout("Hands:")
        for i in range(0, self._game.get_player_count()):
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

    def print_round_information(self):
        self._io.newline()
        self._io.cout(
            f"Round {self._game.get_max_cards() - self._game.get_round() + 1} (dealing {self._game.get_round()} cards)"
            )
        self._io.newline()


    def print_round_bids(self):
        self._io.newline()
        self._io.cout("Bids:")
        for i in range(0, self._game.get_player_count()):
            self._io.cout(
                f"Player {i+1}: " + str(self._game.get_bids()[i][self._game.get_round()-1])
                )
        self._io.newline()
        self._io.cout("Lets start the round!")
        self._io.newline()

    def print_player_hand(self, player):
        self._io.cout(self._game._players[player-1])

    def print_tick_situation(self):
        self._io.newline()
        self._io.cout("Tick situation: [bids] [ticks won]")
        bid_table = self._game.get_bids()
        round = self._game.get_round()
        tick_winners = self._game.get_tick_winners()
        for i in range(0, self._game.get_player_count()):
            self._io.cout(
                f"Player {i+1}: " + str(bid_table[i][round-1]) + " " + str(tick_winners[i])
                )
        self._io.newline()

    def print_points_situation(self):
        points_table = self._game.get_points_table()
        self._io.cout("Point situation: ")
        for i in range(0, self._game.get_player_count()):
            self._io.cout(f"Player {i+1}: " + str(points_table[i]))
        self._io.newline()

    def print_this_rounds_suit(self, card):
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
