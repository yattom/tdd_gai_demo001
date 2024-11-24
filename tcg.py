class Card:
    def __init__(self, attack_power):
        self.attack_power = attack_power

    def get_attack_power(self):
        return self.attack_power

    def set_attack_power(self, param):
        self.attack_power = param


class Game:
    def play_card(self, player, card, opponent):
        pass

    def get_life(self, player):
        return 15

    def get_players_by_turn(self, turn):
        return 1, 2