CREATE INDEX idx_team_tour_edit_stage_reached ON team_tournament_edition(stage_reached);

CREATE INDEX idx_tournament_edition_location_id ON tournament_edition(location_id);

CREATE INDEX idx_team_player_active_captain
ON team_player(team_id, player_id)
WHERE is_captain = true AND date_of_departure IS NULL;

CREATE INDEX idx_team_tte
ON team_tournament_edition(tournament_edition_id, team_id);


CREATE INDEX idx_tournament_match_match_type
ON tournament_match(match_type_id);

CREATE INDEX idx_match_team_team_id ON match_team(team_id);

CREATE INDEX idx_tournament_match_match_type_id
ON tournament_match(match_type_id);

CREATE INDEX idx_match_team_match_team_id ON match_team(match_id,team_id);

CREATE INDEX idx_match_event_match_id_event_type ON match_event(match_id,"event");


CREATE INDEX idx_match_type_tour_phase ON match_type(tournament_edition_id,phase);

CREATE INDEX idx_team_player_player_id ON team_player(player_id);

CREATE INDEX idx_team_tournament_covering
ON team_tournament_edition(team_id) INCLUDE (stage_reached, tournament_edition_id);

CREATE INDEX idx_tournament_match_referee_id ON tournament_match(referee_id);

