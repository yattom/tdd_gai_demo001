class Game:
    def __init__(self):
        self.is_finished: bool = False
        self.players: list[str] = ["Player1", "Player2"]
        self.life_points: dict[str, int] = {
            self.players[0]: 20,
            self.players[1]: 20,
        }
        self._cards: dict[str, list[int]] = {
            self.players[0]: [3],
            self.players[1]: [3],
        }

    def cards(self, player):
        return self._cards[player]

    def get_life_point(self, player) -> int:
        return self.life_points[player]

    def play(self, player, card_index):
        opponent = self.players[0] if self.players[1] == player else self.players[1]
        damage = self.cards(player)[card_index]
        self.life_points[opponent] -= damage
        if self.life_points[opponent] <= 0:
            self.is_finished = True

    def set_life_point(self, player, life_point):
         self.life_points[player] = life_point
