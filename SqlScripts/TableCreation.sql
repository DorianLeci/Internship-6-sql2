CREATE TABLE country(
	country_id SERIAL PRIMARY KEY,
	country_name VARCHAR(40) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE tournament_location(
	location_id SERIAL PRIMARY KEY,
	city_postal_code VARCHAR(9) NOT NULL,
	city_name VARCHAR(40) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

	country_id INT NOT NULL REFERENCES country(country_id)
);

CREATE TABLE player(
	player_id SERIAL PRIMARY KEY,
	player_fname VARCHAR(20) NOT NULL,
	player_lname VARCHAR(20) NOT NULL,
	birth_date DATE NOT NULL,
	height INT,
	weight INT,
	is_injured BOOL,
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

	country_id INT NOT NULL REFERENCES country(country_id)
);

CREATE TABLE referee(
	referee_id SERIAL PRIMARY KEY,
	referee_fname VARCHAR(20) NOT NULL,
	referee_lname VARCHAR(20) NOT NULL,
	birth_date DATE NOT NULL,
	licence CHAR(8) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

	country_id INT NOT NULL REFERENCES country(country_id)
);

CREATE TABLE team(
	team_id SERIAL PRIMARY KEY,
	team_name VARCHAR(50) NOT NULL,
	team_email VARCHAR(50),
	contact_number CHAR(17),
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
	country_id INT NOT NULL REFERENCES country(country_id)
	
);

CREATE TABLE team_player(
	team_player_id SERIAL PRIMARY KEY,
	date_of_joining DATE NOT NULL,
	date_of_departure DATE,
	shirt_number INT,
	is_captain BOOL,
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

	team_id INT NOT NULL REFERENCES team(team_id),
	player_id INT NOT NULL REFERENCES player(player_id)
	
);

ALTER TABLE team_player
ADD CONSTRAINT team_player_unique UNIQUE(team_id,player_id);

CREATE TABLE tournament(
	tournament_id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL,
	description TEXT
);

CREATE TABLE tournament_edition(
	tournament_edition_id SERIAL PRIMARY KEY,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL,
	num_of_teams INT NOT NULL,
	tournament_id INT NOT NULL REFERENCES tournament(tournament_id),
	location_id INT NOT NULL REFERENCES tournament_location(location_id)
);

CREATE TYPE tournament_phase AS ENUM('group_stage','round_of_64','round_of_32','round_of_16','quarterfinal','semifinal','final','third_place');
CREATE TABLE match_type(
	match_type_id SERIAL PRIMARY KEY,
	phase tournament_phase NOT NULL,
	number_of_teams INT NOT NULL,

	tournament_edition_id INT NOT NULL REFERENCES tournament_edition(tournament_edition_id) ON DELETE CASCADE
	
);

CREATE TABLE team_tournament_edition(
	team_id INT NOT NULL REFERENCES team(team_id),
	tournament_edition_id INT NOT NULL REFERENCES tournament_edition(tournament_edition_id) ON DELETE CASCADE,

	UNIQUE(team_id,tournament_edition_id),

	number_of_wins INT DEFAULT 0,
	ranking INT DEFAULT NULL,
	stage_reached tournament_phase DEFAULT NULL
);

CREATE TABLE tournament_match(
	match_id SERIAL PRIMARY KEY,
	date_time TIMESTAMP NOT NULL,
	
    match_type_id INT NOT NULL REFERENCES match_type(match_type_id),
	referee_id INT NOT NULL REFERENCES referee(referee_id),
	winner_id INT REFERENCES team(team_id)
);

CREATE TABLE match_team(
	match_team_id SERIAL PRIMARY KEY,
	match_id INT NOT NULL REFERENCES tournament_match(match_id),
	team_id INT NOT NULL REFERENCES team(team_id),
	
	UNIQUE(match_id,team_id),
	
	score INT NOT NULL
);







