from abc import ABCMeta

class Card(metaclass=ABCMeta):
    @abstractmethod
    def get_name():
        pass

class Tempura(Card):
    def get_name():
        return "Tempura"

class Sashimi(Card):
    def get_name():
        return "Sashimi"

class Pudding(Card):
    def get_name():
        return "Pudding"

class Wasabi(Card):
    def get_name():
        return "Wasabi"

class Chopsticks(Card):
    def get_name():
        return "Chopsticks"

class Dumpling(Card):
    def get_name():
        return "Dumpling"

class Maki(Card):
    def __init__(self, n_maki):
        self.n_maki = n_maki

    def get_maki(self):
        return self.n_maki

    def get_name():
        return "Maki {0}".format(self.n_maki)

class Nigiri(Card):
    @abstractmethod
    def __init__():
        self.wasabi = False

class Squid(Nigiri):
    def get_value(self):
        return 9 if wasabi else 3

    def get_name():
        return "Squid Nigiri"

class Salmon(Nigiri):
    def get_value(self):
        return 6 if wasabi else 2

    def get_name():
        return "Salmon Nigiri"

class Egg(Nigiri):
    def get_value(self):
        return 3 if wasabi else 1

    def get_name():
        return "Egg Nigiri"
