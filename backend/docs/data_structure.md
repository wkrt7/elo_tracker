# Elo Tracker Database Structure (Team-Based)

## 1. Player Table

| Column       | Type     | Notes              |
| ------------ | -------- | ------------------ |
| `id`         | INT PK   | Unique player ID   |
| `name`       | VARCHAR  | Player name        |
| `elo`        | FLOAT    | Current Elo        |
| `created_at` | DATETIME | Optional timestamp |

---

## 2. Character Table

| Column | Type    | Notes                   |
| ------ | ------- | ----------------------- |
| `id`   | INT PK  | Unique character ID     |
| `name` | VARCHAR | Character name (unique) |

---

## 3. Finish Type Table

| Column | Type    | Notes                                            |
| ------ | ------- | ------------------------------------------------ |
| `id`   | INT PK  | Unique finish type ID                            |
| `name` | VARCHAR | Finish type name (unique)                        |
|        |         | Examples: 'push_to_base', 'regular_push', 'kill' |

---

## 4. Team Table

| Column | Type    | Notes              |
| ------ | ------- | ------------------ |
| `id`   | INT PK  | Unique team ID     |
| `name` | VARCHAR | Optional team name |

---

## 5. Team Participants Table

| Column      | Type   | Notes                       |
| ----------- | ------ | --------------------------- |
| `id`        | INT PK | Unique record ID            |
| `team_id`   | INT FK | Foreign key to `team(id)`   |
| `player_id` | INT FK | Foreign key to `player(id)` |

- Supports 1–5 players per team.

---

## 6. Match Table

| Column           | Type     | Notes                                         |
| ---------------- | -------- | --------------------------------------------- |
| `id`             | INT PK   | Unique match ID                               |
| `date`           | DATETIME | When the match occurred                       |
| `description`    | VARCHAR  | Optional match description                    |
| `finish_type_id` | INT FK   | Foreign key to `finish_type(id)`, nullable    |
| `is_long`        | BOOLEAN  | 1 = long match, 0 = short match               |
| `team_a_id`      | INT FK   | Foreign key to `team(id)`                     |
| `team_b_id`      | INT FK   | Foreign key to `team(id)`                     |
| `winner_team_id` | INT FK   | Nullable, FK to `team(id)` — the winning team |
| `k_factor`       | FLOAT    | K-factor used for Elo calculation             |
| `team_size`      | int      | 1,2,3,4,5                                     |

---

## 7. Match Participant Table

| Column         | Type   | Notes                                    |
| -------------- | ------ | ---------------------------------------- |
| `id`           | INT PK | Unique record ID                         |
| `match_id`     | INT FK | Foreign key to `match(id)`               |
| `player_id`    | INT FK | Foreign key to `player(id)`              |
| `character_id` | INT FK | Foreign key to `character(id)`, nullable |
| `elo_before`   | FLOAT  | Elo before match                         |
| `elo_after`    | FLOAT  | Elo after match                          |
| `team_id`      | INT FK | Foreign key to `team(id)` for this match |

---

## 8. Elo History Table

| Column      | Type     | Notes                                |
| ----------- | -------- | ------------------------------------ |
| `id`        | INT PK   | Unique record ID                     |
| `player_id` | INT FK   | Foreign key to `player(id)`          |
| `match_id`  | INT FK   | Foreign key to `match(id)`, nullable |
| `elo`       | FLOAT    | Player Elo after this event          |
| `timestamp` | DATETIME | When this Elo was recorded           |

---

## Relationships

- `match_participant.match_id → match.id`
- `match_participant.player_id → player.id`
- `match_participant.character_id → character.id` (nullable)
- `match_participant.team_id → team.id`
- `match.team_a_id → team.id`
- `match.team_b_id → team.id`
- `match.winner_team_id → team.id` (nullable)
- `match.finish_type_id → finish_type.id` (nullable)
- `elo_history.player_id → player.id`
- `elo_history.match_id → match.id` (nullable)

---

## Key Features

1. Team-based matches with 1–5 players per team.
2. Winner is tracked at team level (`winner_team_id`).
3. Participant info tracks which player played which character, and which team they were on.
4. Elo tracking per player, both before/after match and historical (`elo_history`).
5. Normalized: no redundant or inconsistent character/finish type/team names.
6. Supports short/long matches and finish type stats.
