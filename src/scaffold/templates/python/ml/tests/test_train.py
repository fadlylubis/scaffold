from __PACKAGE__.train import train


def test_train_beats_chance():
    _, acc = train()
    assert acc > 0.8
