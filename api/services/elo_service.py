from typing import List

from crud.player import player_crud
from schemas.match import MatchInternal
from schemas.player import PlayerUpdate
from sqlalchemy.orm import Session


class EloService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def calculate_and_update(self, match: MatchInternal) -> List[dict]:
        """
        Calculate new ELO for match participants and update players in the DB.
        Returns a list of participant dicts with elo_before and elo_after.
        """
        player_ids = [p.player_id for p in match.participants]
        players = {p.id: p for p in player_crud.batch_get(self.db, player_ids, with_transaction=True)}

        # Split into teams
        team_a = [players[p.player_id] for p in match.participants if p.team_side == 1]
        team_b = [players[p.player_id] for p in match.participants if p.team_side == 2]

        avg_elo_a = sum(p.elo for p in team_a) / len(team_a)
        avg_elo_b = sum(p.elo for p in team_b) / len(team_b)

        participants = []
        for p in match.participants:
            player = players[p.player_id]
            part_dict = p.model_dump()
            part_dict["elo_before"] = player.elo

            if p.team_side == 1:
                expected = 1 / (1 + 10 ** ((avg_elo_b - player.elo) / 400))
                score = 1 if match.winner_team_side == 1 else 0
            else:
                expected = 1 / (1 + 10 ** ((avg_elo_a - player.elo) / 400))
                score = 1 if match.winner_team_side == 2 else 0

            new_elo = player.elo + match.k_factor * (score - expected)
            part_dict["elo_after"] = new_elo

            # Update player in DB
            player_crud.update(self.db, id=p.player_id, obj_in=PlayerUpdate(elo=new_elo))
            participants.append(part_dict)

        return participants
