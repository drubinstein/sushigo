from Cards import *
import random
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class SushiGo:
    class Player:
        hand = []
        plate = []
        score = 0
        def __init__(self):
            self.score = 0
            self.hand = []
            self.plate = []
            self.n_tempura = 0
            self.n_sashimi = 0
            self.n_pudding = 0
            self.n_maki = 0
            self.n_dumplings = 0
            self.wasabi_unused = 0

        def get_hand_str(self):
            s = ""
            for c in self.hand:
                s += c.get_name() + " "
            return s

        def get_plate_str(self):
            s = ""
            for c in self.plate:
                s += c.get_name() + " "
            return s

        def mov_hand_plate(self, h=0):
            if type(self.hand[h]) is Sashimi:
                self.n_sashimi += 1
            if type(self.hand[h]) is Tempura:
                self.n_tempura += 1
            if type(self.hand[h]) is Pudding:
                self.n_pudding += 1
            if type(self.hand[h]) is Maki:
                self.n_maki += self.hand[h].get_maki()
            if type(self.hand[h]) is Dumpling:
                self.n_dumplings += 1
            if type(self.hand[h]) is Wasabi:
                self.wasabi_unused += 1
            if issubclass(self.hand[h], Nigiri) and self.wasabi_unused > 0:
                self.hand[h].wasabi = True
                self.wasabi_unused -= 1

            self.plate.append(self.hand[h])
            del self.hand[h]

        def reset(self):
            self.hand = []
            self.plate = []
            self.n_tempura = 0
            self.n_sashimi = 0
            self.n_pudding = 0
            self.n_maki = 0
            self.n_dumplings = 0
            self.wasabi_unused = 0

    def __init__(self,n_players):
        self.deck = [Tempura() for _ in range(0,15)] \
                  + [Sashimi() for _ in range(0,14)] \
                  + [Dumpling() for _ in range(0,14)] \
                  + [Maki(2) for _ in range(0,12)] \
                  + [Maki(1) for _ in range(0,6)] \
                  + [Maki(3) for _ in range(0,8)] \
                  + [Salmon() for _ in range(0,10)] \
                  + [Squid() for _ in range(0,5)] \
                  + [Egg() for _ in range(0,5)] \
                  + [Pudding() for _ in range(0,10)] \
                  + [Wasabi() for _ in range(0,6)] \
                  + [Chopsticks() for _ in range(0,4)]
        self.n_players = n_players
        self.players = [SushiGo.Player() for _ in range(0,n_players)]

        if self.n_players == 2: self.start_hand_size = 10
        if self.n_players == 3: self.start_hand_size = 9
        if self.n_players == 4: self.start_hand_size = 8
        if self.n_players == 5: self.start_hand_size = 7

        #shuffle the master deck for the game
        #initialize turn
        self.round = 0
        random.shuffle(self.deck)

    def begin_turn(self):
        #hand out cards to each players
        for p in self.players:
            p.hand = self.deck[0:self.start_hand_size]
            del self.deck[0:self.start_hand_size]

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
        max_makis = self.get_top_makis()

        for p in range(0,self.n_players):
            scores[p] = int(self.players[p].n_tempura/2)*5 \
                      + int(self.players[p].n_sashimi/3)*10
            if max_pudding > 0:
                if self.players[p].n_pudding == max_pudding:
                    scores[p] += 6
                else:
                    scores[p] -= 6

            if max_makis[0] > 0 and self.players[p].n_maki == max_makis[0]:
                    scores[p] += 6
            elif max_makis[1] > 0 and self.players[p].n_maki == max_makis[1]:
                    scores[p] += 3

            scores[p] += int(self.players[p].n_dumplings*(self.players[p].n_dumplings+1)/2)
            """ Equivalent to the following
            if self.players[p].n_dumplings == 1:
                scores[p] += 1
            if self.players[p].n_dumplings == 2:
                scores[p] += 3
            if self.players[p].n_dumplings == 3:
                scores[p] += 6
            if self.players[p].n_dumplings == 4:
                scores[p] += 10
            if self.players[p].n_dumplings == 5:
                scores[p] += 15
            """

            #now just loop through the plate to deal with the nigiri
            for card in self.players[p].hand:
                if issubclass(card,Nigiri):
                    scores[p] += card.get_value()

        return scores

    def play_round(self, cycle):
        for c in range(0,self.start_hand_size):
            print("PASS {0}".format(c))
            for p in self.players:
                if len(p.hand) == 1:
                    p.mov_hand_plate(0)
                    continue

                #For "Security"
                cls()
                input("Press enter when you are ready to take your turn")
                print("Hand: {0}\nPlate: {1}".format(p.get_hand_str(), p.get_plate_str()))
                while(True):
                    h = input("Please enter the index of the card you want to play."
                          " Must be between 0 and {0}. If you have and want to use"
                          " chopsticks from your plate enter c[0-9][0-9] where"
                          "the numbers represent the cards from the hand you want to use\n".format(len(p.hand)-1))

                    if len(h) == 0:
                        print("You have not entered anything...")
                        continue
                    if h == "c" and p.hand.count(Chopsticks) > 0:
                        if h[1].isdigit() and h[2].isdigit():
                            h1 = int(h[1])
                            h2 = int(h[2])
                            if h1 >= len(p.hand) or h1 >= len(p.hand):
                                print("You have entered an invalid hand index")
                                continue

                            p.plate.remove(Chopsticks)
                            p.mov_hand_plate(h1)
                            p.mov_hand_plate(h2)
                            print("SUSHI GO!")
                            break
                    if h[0].isdigit():
                        idx = int(h[0])
                        if idx >= len(p.hand):
                            print("You have entered an invalid hand index: {0}".format(idx))
                            continue
                        p.mov_hand_plate(idx)
                        break
            #Now cycle the hands

            if cycle:
                for p in range(0,self.n_players):
                    self.players[p].hand, self.players[(p+1)%self.n_players].hand =  \
                    self.players[(p+1)%self.n_players].hand, self.players[p].hand
            else:
                for p in range(self.n_players-1,-1,-1):
                    self.players[p].hand, self.players[p-1].hand =  \
                    self.players[p-1].hand, self.players[p].hand

    def game(self):
        print("WELCOME TO SUSHI GO!")
        #3 rounds per game
        cycle = True
        for r in range(0,3):
            self.begin_turn()
            input("Press enter when you are ready to begin the round")
            self.play_round(cycle)
            cycle = not cycle
            scores = self.score_players()
            print("Scores for the round: ")
            print(scores)
            #record scores and reset for next turn
            for p in range(0,self.n_players):
                self.players[p].score += scores[p]
                self.players[p].reset()

            print("Score Totals:\n")
            for n in range(0,self.n_players):
                print("\tPlayer {0}: {1}".format(n,self.players[n].score))

        print("Game over\n")

game = SushiGo(3)
game.game()
