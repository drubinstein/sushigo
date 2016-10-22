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

        def get_hand(self): return self.hand

        def get_hand_size(self): return len(self.hand)

        def mov_hand_pallete(self, h=0):
        """move card index h in hand (must be range 0:len(hand))
            update score as well
        """

            if type(hand[h]) is Sashimi: self.n_sashimi += 1
            if type(hand[h]) is Tempura: self.n_tempura += 1
            if type(hand[h]) is Pudding: self.n_pudding += 1
            if type(hand[h]) is Maki: self.n_maki += hand[h].get_maki()
            if type(hand[h]) is Dumpling: self.n_dumplings += 1
            if type(hand[h]) is Wasabi: self.wasabi_unused += 1
            if issubclass(hand[h], Nigiri) and self.wasabi_unused > 0
                hand[h].wasabi = True
                self.wasabi_unused -= 1

            self.pallete.append(hand[h])
            del hand[h]

    def __init__(self,n_players):
        deck = [Tempura    for _ in xrange(1,15) \
               ,Sashimi    for _ in xrange(1,14) \
               ,Dumpling   for _ in xrange(1,14) \
               ,Maki(2)    for _ in xrange(1,12) \
               ,Maki(3)    for _ in xrange(1,8)  \
               ,Maki(1)    for _ in xrange(1,6)  \
               ,Salmon     for _ in xrange(1,10) \
               ,Squid      for _ in xrange(1,5)  \
               ,Egg        for _ in xrange(1,5)  \
               ,Pudding    for _ in xrange(1,10) \
               ,Wasabi     for _ in xrange(1,6)  \
               ,Chopsticks for _ in xrange(1,4)]
        self.n_players = n_players
        self.players = [Player for _ in xrange(1,n_players)]

        if self.n_players == 2: self.start_hand_size = 10
        if self.n_players == 3: self.start_hand_size = 9
        if self.n_players == 4: self.start_hand_size = 8
        if self.n_players == 5: self.start_hand_size = 7

        #shuffle the master deck for the game
        #initialize turn
        self.round = 0
        random.shuffle(master_deck)
        begin_turn()

    def begin_turn(self):
        #hand out cards to each players
        for p in self.players:
            p.hand.append(deck[0:self.start_hand_size])
            del deck[0:self.start_hand_size]
