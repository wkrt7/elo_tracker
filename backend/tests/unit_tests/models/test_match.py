from src.models.match import Match


def test_create_match(db_session):
    match = Match(team_size=2, k_factor=32, is_long=False, winner_team_side=1)
    db_session.add(match)
    db_session.commit()
    db_session.refresh(match)

    assert match.id is not None
    assert match.k_factor == 32
    assert match.team_size == 2
    assert match.is_long is False
    assert match.winner_team_side == 1
    assert match.date is not None  # Auto-generated timestamp


def test_create_match_with_optional_fields(db_session):
    match = Match(
        team_size=3,
        k_factor=40,
        is_long=True,
        winner_team_side=2,
        description="Epic battle",
        finish_type_id=1,  # Assuming finish_type exists
    )
    db_session.add(match)
    db_session.commit()
    db_session.refresh(match)

    assert match.description == "Epic battle"
    assert match.finish_type_id == 1
    assert match.is_long is True
