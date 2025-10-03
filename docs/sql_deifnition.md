-- 1. Player Table
CREATE TABLE player (
id SERIAL PRIMARY KEY,
name VARCHAR(255) NOT NULL UNIQUE,
elo FLOAT NOT NULL DEFAULT 1000.0,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Character Table
CREATE TABLE character (
id SERIAL PRIMARY KEY,
name VARCHAR(255) NOT NULL UNIQUE
);

-- 3. Finish Type Table
CREATE TABLE finish_type (
id SERIAL PRIMARY KEY,
name VARCHAR(255) NOT NULL UNIQUE
);

-- 4. Match Table
CREATE TABLE match (
id SERIAL PRIMARY KEY,
date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
description VARCHAR(500),
finish_type_id INTEGER,
is_long BOOLEAN NOT NULL DEFAULT FALSE,
team_size INTEGER NOT NULL,
k_factor FLOAT NOT NULL,
winner_team_side INTEGER,
FOREIGN KEY (finish_type_id) REFERENCES finish_type(id)
);

-- 5. Match Participant Table
CREATE TABLE match_participant (
id SERIAL PRIMARY KEY,
match_id INTEGER NOT NULL,
player_id INTEGER NOT NULL,
character_id INTEGER,
elo_before FLOAT NOT NULL,
elo_after FLOAT NOT NULL,
team_side INTEGER NOT NULL,
FOREIGN KEY (match_id) REFERENCES match(id) ON DELETE CASCADE,
FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE,
FOREIGN KEY (character_id) REFERENCES character(id) ON DELETE SET NULL,
CONSTRAINT uq_match_player UNIQUE (match_id, player_id)
);

-- Indexes for better query performance
CREATE INDEX idx_match_participant_match ON match_participant(match_id);
CREATE INDEX idx_match_participant_player ON match_participant(player_id);
CREATE INDEX idx_match_date ON match(date);
CREATE INDEX idx_player_elo ON player(elo DESC);
