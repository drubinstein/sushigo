from Cards import *
import random

class SushiGo:
    class Player:
        def __init__(self):
            self.score = 0
            self.hand = []
            self.pallete = []
            self.n_tempura = 0
            self.n_sashimi = 0
            self.n_pudding = 0
            self.n_maki = 0
            self.n_dumplings = 0
            self.wasabi_unused = 0

        def get_hand_size(self):
            return len(self.hand)

        #move card index h in hand (must be range 0:len(hand))
        #update score as well
        def mov_hand_pallete(self, h=0):
            if type(hand[h]) is Sashimi:
                self.n_sashimi += 1
            if type(hand[h]) is Tempura:
                self.n_tempura += 1
            if type(hand[h]) is Pudding:
                self.n_pudding += 1
            if type(hand[h]) is Maki:
                self.n_maki += hand[h].get_maki()
            if type(hand[h]) is Dumpling:
                self.n_dumplings += 1
            if type(hand[h]) is Wasabi:
                self.wasabi_unused += 1
            if issubclass(hand[h], Nigiri) and self.wasabi_unused > 0
                hand[h].wasabi = True
                self.wasabi_unused -= 1

            self.pallete.append(hand[h])
            del hand[h]

        def reset(self):
            self.hand = []
            self.pallete = []
            self.n_tempura = 0
            self.n_sashimi = 0
            self.n_pudding = 0
            self.n_maki = 0
            self.n_dumplings = 0
            self.wasabi_unused = 0

    def __init__(self,n_players):
        #Cycle direction
        self.cycle = True

        deck = [Tempura    for _ in range(1,15) \
               ,Sashimi    for _ in range(1,14) \
               ,Dumpling   for _ in range(1,14) \
               ,Maki(2)    for _ in range(1,12) \
               ,Maki(3)    for _ in range(1,8)  \
               ,Maki(1)    for _ in range(1,6)  \
               ,Salmon     for _ in range(1,10) \
               ,Squid      for _ in range(1,5)  \
               ,Egg        for _ in range(1,5)  \
               ,Pudding    for _ in range(1,10) \
               ,Wasabi     for _ in range(1,6)  \
               ,Chopsticks for _ in range(1,4)]
        self.n_players = n_players
        self.players = [Player for _ in range(1,n_players)]

        if self.n_players == 2: self.start_hand_size = 10
        if self.n_players == 3: self.start_hand_size = 9
        if self.n_players == 4: self.start_hand_size = 8
        if self.n_players == 5: self.start_hand_size = 7

        #shuffle the master deck for the game
        #initialize turn
        self.round = 0
        random.shuffle(master_deck)

    def begin_turn(self):
        #hand out cards to each players
        for p in self.players:
            p.hand.append(deck[0:self.start_hand_size])
            del deck[0:self.start_hand_size]

    def get_max_pudding(self):
        max_pudding = 0
        for p in self.players:
            max_pudding = max(max_pudding, p.n_pudding)
        return max_pudding

    def get_top_makis(self):
        max_makis = [0,0]
        for p in self.players:
            if p.n_maki > max_makis[0]:
                max_makis[1] = max_makis[0]
                max_makis[0] = p.n_maki
                continue
            if p.n_maki > max_makis[1]:
                max_makis[0] = p.n_maki
        return max_makis

    def score_players(self):
        scores = [0]*self.n_players
        max_pudding = self.get_max_pudding()
        max_makis = self.get_max_makis()
        for p in range(0,self.n_players-1):
            scores[p] = self.players[p].n_tempura/2*5 \
                      + self.players[p].n_sashimi/3*10 \
            if max_pudding > 0:
                if self.players[p].n_pudding == max_pudding:
                    scores[p] += 6
                else
                    scores[p] -= 6

            if max_makis[0] > 0:
                if self.players[p].n_maki == max_maki[0]:
                    scores[p] += 6
                elif self.players[p].n_maki == max_maki[1]:

            if self.players[p].n_dumplings == 1: scores[p] += 1
            if self.players[p].n_dumplings == 2: scores[p] += 3
            if self.players[p].n_dumplings == 3: scores[p] += 6
            if self.players[p].n_dumplings == 4: scores[p] += 10
            if self.players[p].n_dumplings == 5: scores[p] += 15

            #now just loop through the pallete to deal with the nigiri
            for card in self.players[p].hand:
                if issubclass(card,Nigiri):
                    scores[p] += card.get_value()

    def play_round(self,cycle ):
        for c in range(0,self.start_hand_size-1):
            for p in self.players:
                print("Hand: {0}\nPlate: {1}".format(p.hand, p.pallete)
                h = input("Please enter the index of the card you want to play."
                          " Must be between 0 and {0}. If you have and want to use"
                          " chopsticks from your pallete enter c[0-9][0-9] where"
                          "the numbers represent the cards from the hand you want to use".format(len(p.hand)-1))
                while(True):
                    if len(h) == 0:
                        print("You have not entered anything...")
                        continue
                    if h == "c" and p.hand.count(Chopsticks) > 0
                        if h[1].isdigit() and h[2].isdigit():
                            h1 = int(h[1])
                            h2 = int(h[2])
                            if h1 < len(p.hand) or h1 < len(p.hand):
                                print("You have entered an invalid hand index")
                                continue

                            p.pallete.remove(Chopsticks)
                            p.mov_hand_pallete(h1)
                            p.mov_hand_pallete(h2)
                    if h.isdigit():
                        h = int(h)
                        if h < len(p.hand):
                            print("You have entered an invalid hand index")
                            continue
                        p.mov_hand_pallete(h)
                    break
            #Now cycle the hands

            if cycle == RIGHT:
                for p in range(0,self.n_players):
                    self.players[p].hand, self.players[(p+1)%self.n_players] =  \
                    self.players[(p+1)%self.n_players].hand, self.players[p]
            elif cycle == LEFT:
                for p in range(self.n_players-1,-1,-1):
                    self.players[p].hand, self.players[p-1] =  \
                    self.players[p-1].hand, self.players[p]

    def game(self):
        #3 rounds per game
        for r in range(0,3):
            self.play_round(cycle)
            cycle = not cycle
            scores = self.score_players()
            #record scores and reset for next turn
            for p in range(0,self.n_players-1):
                self.begin_turn()
                self.players[p].score += scores[p]
                p.reset()


        print("Game over\nScores:\n")
        for n in range(0,self.n_players-1):
            print("\tPlayer {0}: {1}".format(n,self.players[n].score))


game = SushiGo(3)
game.game()
