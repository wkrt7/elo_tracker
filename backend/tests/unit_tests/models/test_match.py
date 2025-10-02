from src.models.match import Match
from src.models.team import Team


def test_create_match(db_session):
    team_a = Team(name="Team A")
    team_b = Team(name="Team B")
    db_session.add_all([team_a, team_b])
    db_session.commit()

    match = Match(team_a_id=team_a.id, team_b_id=team_b.id, team_size=2, k_factor=32, is_long=False)
    db_session.add(match)
    db_session.commit()
    db_session.refresh(match)

    assert match.id is not None
    assert match.team_a.id == team_a.id
    assert match.team_b.id == team_b.id
    assert match.k_factor == 32
