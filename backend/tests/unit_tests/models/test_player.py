import pytest
from src.models.character import Character
from src.models.match import Match, MatchParticipant
from src.models.player import Player


def test_create_player(db_session):
    # Create a player
    player = Player(name="Test Player", elo=1200)
    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)

    # Assertions
    assert player.id is not None
    assert player.name == "Test Player"
    assert player.elo == 1200
    assert player.created_at is not None


def test_player_unique_name(db_session):
    player1 = Player(name="Unique Player", elo=1000)
    db_session.add(player1)
    db_session.commit()

    # Try to create duplicate
    player2 = Player(name="Unique Player", elo=1100)
    db_session.add(player2)

    with pytest.raises(Exception):  # IntegrityError
        db_session.commit()


def test_player_relationship_match_participation(db_session):
    # Create players
    player1 = Player(name="Player 1", elo=1000)
    player2 = Player(name="Player 2", elo=1050)
    db_session.add_all([player1, player2])
    db_session.commit()

    # Create a match
    match = Match(team_size=1, k_factor=32, is_long=False, winner_team_side=1)
    db_session.add(match)
    db_session.commit()

    # Create match participations
    participation1 = MatchParticipant(
        match_id=match.id, player_id=player1.id, team_side=1, elo_before=1000, elo_after=1016
    )
    participation2 = MatchParticipant(
        match_id=match.id, player_id=player2.id, team_side=2, elo_before=1050, elo_after=1034
    )
    db_session.add_all([participation1, participation2])
    db_session.commit()

    # Refresh and test relationships
    db_session.refresh(player1)
    db_session.refresh(match)

    assert len(player1.match_participations) == 1
    assert player1.match_participations[0].match_id == match.id
    assert player1.match_participations[0].elo_after == 1016

    assert len(match.participants) == 2
    assert match.participants[0].player_id in [player1.id, player2.id]


def test_player_with_character(db_session):
    player = Player(name="Character User", elo=1200)
    character = Character(name="Ryu")
    db_session.add_all([player, character])
    db_session.commit()

    match = Match(team_size=1, k_factor=32, winner_team_side=1)
    db_session.add(match)
    db_session.commit()

    participation = MatchParticipant(
        match_id=match.id, player_id=player.id, character_id=character.id, team_side=1, elo_before=1200, elo_after=1216
    )
    db_session.add(participation)
    db_session.commit()

    db_session.refresh(player)
    assert player.match_participations[0].character_id == character.id
