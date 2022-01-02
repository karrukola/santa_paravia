"""Tests for _eventually_invade() Use Case

They cover wheter land has been seized or not.
Amount of land
    """

from santa_paravia.paravia import _eventually_invade


class MinPlayer:
    """A minimal player, just the attributes needed for this use case"""

    def __init__(self, soldiers, land, which_player, title, name, city):
        self.soldiers = soldiers
        self.land = land
        self.which_player = which_player
        self.title = title
        self.name = name
        self.city = city


def test_player_is_safe():
    """If you have at least one soldier per 500 hectares, you are safe."""
    under_attack = MinPlayer(1, 500, 1, "sir", "player1", "city1")
    others = [MinPlayer(10, 500, 2, "duke", "player2", "city2")]
    peppone = MinPlayer(25, 10000, 7, "baron", "peppone", "brescello")

    land_before = under_attack.land
    # pylint: disable-next=protected-access
    _eventually_invade(under_attack, others, peppone)
    assert land_before == under_attack.land


def test_player_is_invaded_by_baron_peppone():
    """If you have less than one soldier per 1000 hectares, you will be invaded."""
    under_attack = MinPlayer(10, 10001, 1, "sir", "player1", "city1")
    others = [MinPlayer(10, 500, 2, "duke", "player2", "city2")]
    peppone = MinPlayer(25, 10000, 7, "baron", "peppone", "brescello")  # attacker

    attacked_land_before = under_attack.land
    attacker_land_before = peppone.land
    # pylint: disable-next=protected-access
    _eventually_invade(under_attack, others, peppone)
    assert attacked_land_before > under_attack.land
    delta_land = attacked_land_before - under_attack.land
    assert peppone.land == attacker_land_before + delta_land


def test_player_is_invaded_by_other_player():
    """If you have between one soldier per 500 hectares and one soldier per 1000
    hectares, you are safe unless one of the other players has about 2 and a
    half times as many soldiers as you have."""

    under_attack = MinPlayer(10, 7500, 1, "sir", "player1", "city1")
    others = [
        MinPlayer(51, 7500, 2, "duke", "player2", "city2"),  # is the attacker
        MinPlayer(51, 7500, 3, "duke", "player3", "city3"),
    ]
    peppone = MinPlayer(25, 10000, 7, "baron", "peppone", "brescello")

    attacked_land_before = under_attack.land
    attacker_land_before = others[0].land
    # pylint: disable-next=protected-access
    _eventually_invade(under_attack, others, peppone)
    assert attacked_land_before > under_attack.land
    delta_land = attacked_land_before - under_attack.land
    assert others[0].land == attacker_land_before + delta_land


def test_player_is_not_invaded_by_npc():
    """between 500 and 1000, no other players

    NPC - Baron Peppone has enough soldiers to eventually invade, if it was a
    player.

    If you have between one soldier per 500 hectares and one soldier per 1000
    hectares, you are safe unless one of the other players has about 2 and a
    half times as many soldiers as you have."""
    under_attack = MinPlayer(10, 7500, 1, "sir", "player1", "city1")
    others = [under_attack]  # needed because code always loops through all players
    peppone = MinPlayer(25, 10000, 7, "baron", "peppone", "brescello")

    attacked_land_before = under_attack.land
    # pylint: disable-next=protected-access
    _eventually_invade(under_attack, others, peppone)
    assert attacked_land_before == under_attack.land


def test_player_is_not_invaded_by_baron_1000():
    """Exactly 1/1000"""
    under_attack = MinPlayer(10, 10000, 1, "sir", "player1", "city1")
    others = [under_attack]  # needed because code always loops through all players
    peppone = MinPlayer(25, 10000, 7, "baron", "peppone", "brescello")

    attacked_land_before = under_attack.land
    # pylint: disable-next=protected-access
    _eventually_invade(under_attack, others, peppone)
    assert attacked_land_before == under_attack.land
