import sys
from dataclasses import dataclass
import random


class Deck:
    '''
    プレイヤーの持っているカードのデッキおよび手札。
    
    デッキには任意の枚数のカードを含む。手札は最初は5枚で、デッキをシャッフルして上から5枚取って作る。
    手札は使うと捨て札になる。手札を1枚捨てたら、デッキから1枚補充する。
    デッキがすべてなくなったら、捨て札をシャッフルしてデッキとする。
    
    デッキはプレイヤーそれぞれが持つ。捨て札もプレイヤーそれぞれにまとめておく。
    異なるプレイヤーのデッキが混ざることはない。
    '''
    DEFAULT = [-3, -2, -1, -1, -1, 0, 0, 1, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 7]

    def __init__(self):
        self.deck: list[int] = list(Deck.DEFAULT)
        self.hand: list[int] = []
        self.stash: list[int] = []

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def empty_stash(self):
        if self.deck:
            raise RuntimeError("Invalid state: Deck is not empty, cannot proceed with emptying the stash.")
        self.deck = self.stash
        self.stash = []
        self.shuffle_deck()

    def draw_from_deck(self):
        if not self.deck:
            self.empty_stash()
        self.hand.append(self.deck.pop())

    def replenish_hand(self):
        while len(self.hand) < 5:
            self.draw_from_deck()

    def play_from_hand(self, card_index):
        if card_index < 0 or card_index >= len(self.hand):
            raise ValueError("Invalid card index.")
        played = self.hand.pop(card_index)
        self.stash.append(played)
        self.replenish_hand()


@dataclass
class GameSetting:
    names: tuple[str, str] = ("Player1", "Player2")
    life_points: tuple[int, int] = (20, 20)


class Game:
    def __init__(self, setting: GameSetting):
        self.current_turn_no = 1
        self.is_finished: bool = False
        self.players: list[str] = list(setting.names)
        self.life_points: dict[str, int] = {
            self.players[0]: setting.life_points[0],
            self.players[1]: setting.life_points[1],
        }
        self.decks: dict[str, Deck] = {
            self.players[0]: Deck(),
            self.players[1]: Deck(),
        }
        self.guarding: dict[str, bool] = {
            self.players[0]: False,
            self.players[1]: False,
        }

        for deck in self.decks.values():
            deck.shuffle_deck()
            deck.replenish_hand()

    def cards(self, player):
        return self.decks[player].hand

    def get_life_point(self, player) -> int:
        return self.life_points[player]

    def play(self, player, card_index):
        if self.get_turn()['player'] != player:
            raise ValueError('wrong player')
        opponent = self.get_turn()['opponent']
        if self.cards(player)[card_index] > 0:
            # 正の値はダメージ点
            damage = self.cards(player)[card_index]
            # 相手がガード中ならダメージを半減
            if self.guarding[opponent]:
                damage = damage // 2
            self.life_points[opponent] -= damage
            self.decks[player].play_from_hand(card_index)
        elif self.cards(player)[card_index] < 0:
            # 負の値は回復点 (符号を除いてライフポイントに加算)
            healing = -self.cards(player)[card_index]
            self.life_points[player] += healing
            self.decks[player].play_from_hand(card_index)
        elif self.cards(player)[card_index] == 0:
            # 0はガード (次のターンで自分の受けるダメージを半減)
            self.guarding[player] = True
            self.decks[player].play_from_hand(card_index)
        # ガードは1ターンだけ有効
        self.guarding[opponent] = False
        if self.life_points[opponent] <= 0:
            self.is_finished = True
        else:
            self.current_turn_no += 1

    def set_life_point(self, player, life_point):
        self.life_points[player] = life_point

    def get_turn(self):
        if self.current_turn_no % 2 == 1:
            return {'player': self.players[0], 'opponent': self.players[1], 'turn_no': self.current_turn_no}
        else:
            return {'player': self.players[1], 'opponent': self.players[0], 'turn_no': self.current_turn_no}


def main():
    game = Game(GameSetting())
    while not game.is_finished:
        print(f'===== ターン {game.get_turn()['turn_no']} =====')
        print(f'{game.get_turn()['player']}のターン')
        print(
            f'{game.players[0]}のライフ: {game.get_life_point(game.players[0])}, {game.players[1]}のライフ: {game.get_life_point(game.players[1])}')
        print(f'カードを選んでください(0-index): {game.cards(game.get_turn()["player"])}')
        while True:
            line = sys.stdin.readline()
            try:
                card_index = int(line)
                if 0 <= card_index < len(game.cards(game.get_turn()["player"])):
                    break
            except ValueError:
                pass
            print(f'0から{len(game.cards(game.get_turn()["player"])) - 1}の数字を入力してください')

        game.play(game.get_turn()["player"], card_index)
        if game.is_finished:
            print(
                f'{game.players[0]}のライフ: {game.get_life_point(game.players[0])}, {game.players[1]}のライフ: {game.get_life_point(game.players[1])}')
            print(f'{game.get_turn()['player']}の勝利')


if __name__ == '__main__':
    main()
