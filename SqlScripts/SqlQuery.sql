EXPLAIN(ANALYZE,COSTS)
SELECT EXTRACT(YEAR FROM te.start_date) AS tournament_year,
(SELECT team_name FROM team WHERE team_id=tte.team_id) AS winner_name,
tl.city_name,c.country_name AS winner_name

FROM tournament t
JOIN tournament_edition te ON te.tournament_id=t.tournament_id
JOIN tournament_location tl ON tl.location_id=te.location_id
JOIN country c ON c.country_id=tl.country_id
JOIN team_tournament_edition tte ON tte.tournament_edition_id=te.tournament_edition_id
WHERE tte.stage_reached = 'Winner';


EXPLAIN(ANALYZE,COSTS)
SELECT t.team_id, t.team_name, t.team_email, tte.tournament_edition_id,
       tour.name, tp.player_id,p.player_fname, p.player_lname
FROM team_tournament_edition tte
JOIN team t ON t.team_id = tte.team_id
JOIN team_player tp ON tp.team_id = t.team_id
JOIN player p ON p.player_id = tp.player_id
JOIN tournament_edition te ON te.tournament_edition_id = tte.tournament_edition_id
JOIN tournament tour ON tour.tournament_id = te.tournament_id
WHERE tp.is_captain = true
  AND tp.date_of_departure IS NULL
ORDER BY tte.tournament_edition_id;


EXPLAIN(ANALYZE,COSTS)
SELECT t.team_name,p.player_fname,p.player_lname,p.birth_date,p.weight,p.height,
tp.date_of_joining,tp.date_of_departure
FROM team_player tp
JOIN player p ON p.player_id=tp.player_id
JOIN team t ON t.team_id=tp.team_id;

EXPLAIN(ANALYZE,COSTS)
SELECT te.tournament_edition_id,mty.phase,mt.date_time AS match_time,
mte1.score AS team1_score,mte2.score AS team2_score
FROM tournament_edition te
JOIN match_type mty ON mty.tournament_edition_id=te.tournament_edition_id
JOIN tournament_match mt ON mt.match_type_id=mty.match_type_id
JOIN match_team mte1 ON mte1.match_id=mt.match_id
JOIN match_team mte2 ON mte2.match_id=mt.match_id

WHERE mte1.team_id<mte2.team_id;





