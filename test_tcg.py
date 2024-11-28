from tcg import Game


def test_Player1とPlayer2がいる():
    # arrange 準備
    game = Game()
    # act 実行
    # assert 検証
    # Gameに参加しているのはPlayer1とPlayer2である
    assert game.players == ["Player1", "Player2"]


def test_Player1が攻撃力3のカードを1枚持っている():
    # arrange 準備
    game = Game()
    # act 実行
    # assert 検証
    assert game.cards("Player1") == [3]


def test_Player2が攻撃力3のカードを1枚持っている():
    game = Game()
    assert game.cards("Player2") == [3]
    
    
def test_Player1がカードを使用するとPlayer2が3のダメージを受ける():
    # arrange 準備
    game = Game()
    # act 実行
    game.play("Player1", card_index=0)
    life_point_of_player2 = game.get_life_point("Player2")
    # assert 検証
    assert life_point_of_player2 == 20 - 3


def test_Player2がカードを使用するとPlayer1が3のダメージを受ける():
    # arrange 準備
    game = Game()
    # act 実行
    game.play("Player2", card_index=0)
    life_point_of_player1 = game.get_life_point("Player1")
    # assert 検証
    assert life_point_of_player1 == 20 - 3


def test_Player1がカードを使用するとPlayer2がダメージを受けライフポイントが0になり終了():
    # arrange 準備
    game = Game()
    game.set_life_point("Player2", 3)
    # act 実行
    game.play("Player1", card_index=0)
    # assert 検証
    assert game.is_finished


def test_Player1がカードを使用するとPlayer2がダメージを受けライフポイントが11になり継続():
    # arrange 準備
    game = Game()
    game.set_life_point("Player2", 14)
    # act 実行
    game.play("Player1", card_index=0)
    # assert 検証
    assert not game.is_finished
