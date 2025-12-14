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

ORDER BY tte.stage_reached;


EXPLAIN(ANALYZE,COSTS)
SELECT mty.phase,tm.date_time AS match_time,mw.team_id AS winner_id,ml.team_id AS runner_up_id,
tw.team_name AS winner_name,tw.team_email AS winner_contact FROM match_type mty
JOIN tournament_match tm ON tm.match_type_id=mty.match_type_id 
JOIN match_team mw ON mw.match_id=tm.match_id AND mw.team_id=tm.winner_id 
JOIN match_team ml ON ml.match_id=tm.match_id AND ml.team_id<>tm.winner_id
JOIN team tw ON tw.team_id=tm.winner_id
WHERE mty.phase='final';


EXPLAIN(ANALYZE,COSTS)
SELECT mty.phase,COUNT(*) AS match_type_count FROM match_type mty
GROUP BY mty.phase
ORDER BY mty.phase;


EXPLAIN(ANALYZE,COSTS)
SELECT tm.match_id,tm.date_time AS match_time,
mty.phase,
tw.team_id AS winner_id,
tw.team_name AS winner_name,
t2.team_id AS team2_id,
t2.team_name AS team2_name,
mte1.score AS winner_score,
mte2.score AS team2_score
FROM tournament_match tm
JOIN match_type mty ON mty.match_type_id=tm.match_type_id
JOIN match_team mte1 ON mte1.match_id=tm.match_id AND mte1.team_id=tm.winner_id
JOIN match_team mte2 ON mte2.match_id=tm.match_id AND mte2.team_id<>tm.winner_id
JOIN team tw ON tw.team_id=mte1.team_id
JOIN team t2 ON t2.team_id=mte2.team_id

WHERE tm.date_time::date= DATE '2023-10-10'
ORDER BY match_time;

EXPLAIN(ANALYZE,COSTS)
SELECT p.player_id, p.player_fname || ' ' || p.player_lname AS player_name,COUNT(*) AS goals_scored
FROM match_event mev
JOIN player p ON p.player_id=mev.player_id
JOIN tournament_match tm ON tm.match_id=mev.match_id
JOIN match_type mty ON mty.match_type_id=tm.match_type_id
WHERE mev.event='goal' AND mty.tournament_edition_id=20
GROUP BY p.player_id,player_name

ORDER BY goals_scored DESC;



EXPLAIN(ANALYZE,COSTS)
SELECT t.team_id,t.team_name,
te.tournament_edition_id,EXTRACT(YEAR FROM te.start_date) AS tournament_year,
tte.stage_reached 
FROM team_tournament_edition tte
JOIN tournament_edition te ON te.tournament_edition_id=tte.tournament_edition_id
JOIN team t ON t.team_id=tte.team_id
WHERE t.team_id=30

ORDER BY tournament_year;


EXPLAIN(ANALYZE,COSTS)
SELECT tte.tournament_edition_id,t.team_id AS tournament_winner_id,t.team_name AS tournament_winner_name,
t.country_id,c.country_name
FROM team_tournament_edition tte 
JOIN team t ON t.team_id=tte.team_id
JOIN country c ON c.country_id=t.country_id
WHERE tte.stage_reached='Winner';



EXPLAIN(ANALYZE,COSTS)
SELECT t.name,te.tournament_edition_id,
COUNT(tte.team_id) AS num_of_teams,
COUNT(tp.player_id) AS num_of_players
FROM team_tournament_edition tte
JOIN tournament_edition te ON te.tournament_edition_id=tte.tournament_edition_id
JOIN tournament t ON t.tournament_id=te.tournament_id
JOIN team_player tp ON tp.team_id=tte.team_id
GROUP BY t.name,te.tournament_edition_id;


EXPLAIN(ANALYZE,COSTS)
WITH player_goals AS (SELECT tp.team_id,tp.player_id,COUNT(*) AS goals_scored
FROM team_tournament_edition tte
JOIN team_player tp ON tp.team_id=tte.team_id
JOIN match_type mty ON mty.tournament_edition_id=tte.tournament_edition_id
JOIN tournament_match tm ON tm.match_type_id=mty.match_type_id
JOIN match_event mev ON mev.match_id=tm.match_id
WHERE mev.event='goal' AND mev.player_id=tp.player_id
GROUP BY tp.team_id,tp.player_id
)

SELECT DISTINCT ON(pg.team_id)
pg.team_id,p.player_id,p.player_fname || ' ' || p.player_lname AS player_name,pg.goals_scored
FROM player_goals pg
JOIN player p ON pg.player_id=p.player_id

ORDER BY pg.team_id,pg.goals_scored DESC;


EXPLAIN(ANALYZE,COSTS)
SELECT tm.match_id,r.referee_id,r.referee_fname|| ' '||r.referee_lname AS referee_name,r.birth_date,r.licence
FROM tournament_match tm
JOIN referee r ON r.referee_id=tm.referee_id
WHERE r.referee_id=30
ORDER BY r.referee_id;



