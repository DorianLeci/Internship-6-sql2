DROP INDEX idx_team_tour_edit_stage_reached
CREATE INDEX idx_team_tour_edit_stage_reached ON team_tournament_edition(stage_reached);

DROP INDEX  idx_tournament_edition_location_id
CREATE INDEX idx_tournament_edition_location_id ON tournament_edition(location_id);

DROP INDEX idx_team_player_active_captain
CREATE INDEX idx_team_player_active_captain
ON team_player(team_id, player_id)
WHERE is_captain = true AND date_of_departure IS NULL;

DROP INDEX idx_team_tte
CREATE INDEX idx_team_tte
ON team_tournament_edition(tournament_edition_id, team_id);


CREATE INDEX idx_tournament_match_match_type
ON tournament_match(match_type_id);



