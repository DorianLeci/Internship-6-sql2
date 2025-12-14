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
mte1.score AS team1_score,mte2.score AS team2_score,
team1.team_id AS team1_id,team2.team_id AS team2_id,team1.team_name AS team1_name,team2.team_name AS team2_name
FROM tournament_edition te
JOIN match_type mty ON mty.tournament_edition_id=te.tournament_edition_id
JOIN tournament_match mt ON mt.match_type_id=mty.match_type_id
JOIN match_team mte1 ON mte1.match_id=mt.match_id
JOIN match_team mte2 ON mte2.match_id=mt.match_id AND mte1.team_id<mte2.team_id 
JOIN team team1 ON team1.team_id=mte1.team_id
JOIN team team2 ON team2.team_id=mte2.team_id

WHERE te.tournament_edition_id=3
ORDER BY mty.phase;


EXPLAIN(ANALYZE,COSTS)
SELECT te.tournament_edition_id,mty.phase,mt.date_time AS match_time,
mte1.score AS selected_team_score,mte2.score AS opponent_score,
team1.team_id AS selected_team_id,team2.team_id AS opponent_id,team1.team_name AS selected_team_name,team2.team_name AS opponent_name
FROM tournament_edition te
JOIN match_type mty ON mty.tournament_edition_id=te.tournament_edition_id
JOIN tournament_match mt ON mt.match_type_id=mty.match_type_id
JOIN match_team mte1 ON mte1.match_id=mt.match_id
JOIN match_team mte2 ON mte2.match_id=mt.match_id AND mte1.team_id!=mte2.team_id 
JOIN team team1 ON team1.team_id=mte1.team_id
JOIN team team2 ON team2.team_id=mte2.team_id
WHERE mte1.team_id=4;


EXPLAIN(ANALYZE,COSTS)
SELECT mte.event,mte.match_minute,p.player_id,p.player_fname,p.player_lname
FROM tournament_match tm
JOIN match_event mte ON mte.match_id=tm.match_id
JOIN player p ON p.player_id=mte.player_id
WHERE tm.match_id=100
ORDER BY mte.event;

EXPLAIN(ANALYZE,COSTS)
SELECT p.player_fname,p.player_lname,t.team_id,t.team_name AS team_name,
me.event,me.match_minute,tm.match_id,tm.date_time AS match_time,mty.phase
FROM tournament_edition te
JOIN match_type mty ON mty.tournament_edition_id = te.tournament_edition_id
JOIN tournament_match tm ON tm.match_type_id = mty.match_type_id
JOIN match_event me ON me.match_id = tm.match_id
JOIN player p ON p.player_id=me.player_id
JOIN team_player tp ON tp.player_id=p.player_id
JOIN team t ON t.team_id=tp.team_id
WHERE te.tournament_edition_id=1 AND me.event IN ('yellow_card','red_card')

ORDER BY tm.date_time,me.match_minute;


EXPLAIN(ANALYZE,COSTS)
SELECT p.player_fname || ' ' || p.player_lname AS player_name,
t.team_name,
COUNT(*) as goals_scored

FROM tournament_edition te
JOIN match_type mty ON mty.tournament_edition_id = te.tournament_edition_id
JOIN tournament_match tm ON tm.match_type_id = mty.match_type_id
JOIN match_event me ON me.match_id = tm.match_id
JOIN player p ON p.player_id=me.player_id
JOIN team_player tp ON tp.player_id=p.player_id
JOIN team t ON t.team_id=tp.team_id
WHERE te.tournament_edition_id=2 AND me.event='goal'
GROUP BY player_name,t.team_name

ORDER BY goals_scored DESC;



EXPLAIN(ANALYZE,COSTS)
SELECT 
	t.team_id,
	t.team_name,
	SUM(
		CASE
			WHEN mty.phase='group_stage' AND mte.score>opp.score THEN 3
			WHEN mty.phase='group_stage' AND mte.score=opp.score THEN 1
			ELSE 0
		END
			
	)AS team_points,
	
	SUM(mte.score - opp.score) AS goal_difference,
	SUM(mte.score) AS goals_scored,
	SUM(opp.score) AS goals_conceded,
	tte.stage_reached
	
FROM tournament_edition te
JOIN match_type mty ON mty.tournament_edition_id = te.tournament_edition_id
JOIN tournament_match tm ON tm.match_type_id = mty.match_type_id
JOIN match_team mte ON mte.match_id=tm.match_id
JOIN match_team opp ON opp.match_id=tm.match_id AND mte.team_id!=opp.team_id
JOIN team t ON t.team_id=mte.team_id
JOIN team_tournament_edition tte ON tte.team_id=mte.team_id AND tte.tournament_edition_id=te.tournament_edition_id
WHERE te.tournament_edition_id = 5

GROUP BY t.team_id,t.team_name,tte.stage_reached

ORDER BY tte.stage_reached





