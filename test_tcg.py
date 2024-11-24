import tcg
from tcg import Card, Game

def test_カードが攻撃力を持つことを確認する_攻撃力が5():
    card = Card(attack_power=5)
    assert 5 == card.get_attack_power()


def test_カードが攻撃力を持つことを確認する_攻撃力が1():
    card = Card(attack_power=1)
    assert 1 == card.get_attack_power()

def test_プレイヤー1が攻撃力5のカードでプレイヤー2に攻撃しプレイヤー2のライフが15になることを確認する():
    # arrange
    game = Game()

    # create a card with attack power 5
    card = Card(attack_power=5)
    # act
    game.play_card(
        player=1,
        card=card,
        opponent=2)
    life = game.get_life(player=2)
    # assert
    assert 15 == life
    

def test_第1ターンはプレイヤー1がプレイヤー2に攻撃する():
    game = Game()
    # act
    # ターンに応じたプレイヤーを取得する
    turn = 1  # Assuming first turn
    player, opponent = game.get_players_by_turn(turn)
    # 各ターンのプレイヤーが正しい
    assert player == 1
    assert opponent == 2