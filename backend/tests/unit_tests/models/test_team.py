from src.models import Player, Team, TeamParticipant


def test_create_team_with_players(db_session):
    player1 = Player(name="Bob")
    player2 = Player(name="Charlie")
    team = Team(name="TeamX")
    db_session.add_all([player1, player2, team])
    db_session.commit()

    tp1 = TeamParticipant(team_id=team.id, player_id=player1.id)
    tp2 = TeamParticipant(team_id=team.id, player_id=player2.id)
    db_session.add_all([tp1, tp2])
    db_session.commit()

    fetched_team = db_session.query(Team).filter_by(name="TeamX").first()
    assert len(fetched_team.participants) == 2
