import pytest
from src.models.player import Player
from src.models.team import Team, TeamParticipant


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


def test_player_relationship_team_participation(db_session):

    player = Player(name="Relation Test", elo=1000)
    team = Team(name="Alpha Team")
    db_session.add_all([player, team])
    db_session.commit()

    # Create team participation
    participation = TeamParticipant(player_id=player.id, team_id=team.id)
    db_session.add(participation)
    db_session.commit()

    db_session.refresh(player)
    db_session.refresh(team)

    assert len(player.team_participations) == 1
    assert player.team_participations[0].team.id == team.id
    assert len(team.participants) == 1
    assert team.participants[0].player.id == player.id
