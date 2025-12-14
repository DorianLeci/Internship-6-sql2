EXPLAIN(ANALYZE,COSTS)
SELECT t.name,EXTRACT(YEAR FROM te.start_date),
(SELECT team_name FROM team WHERE team_id=tte.team_id) AS winner_name,
tl.city_name,c.country_name AS winner_name

FROM tournament t
JOIN tournament_edition te ON te.tournament_id=t.tournament_id
JOIN tournament_location tl ON tl.location_id=te.location_id
JOIN country c ON c.country_id=tl.country_id
JOIN team_tournament_edition tte ON tte.tournament_edition_id=te.tournament_edition_id
WHERE tte.stage_reached = 'Winner';

DROP INDEX idx_team_tour_edit_stage_reached
CREATE INDEX idx_team_tour_edit_stage_reached ON team_tournament_edition(stage_reached);
