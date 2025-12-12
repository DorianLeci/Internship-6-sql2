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
	name VARCHAR(30) NOT NULL,
	foundation_year INT NOT NULL,
	description TEXT
);

CREATE TABLE tournament_edition(
	tournament_edition_id SERIAL PRIMARY KEY,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL,

	tournament_id INT NOT NULL REFERENCES tournament(tournament_id),
	location_id INT NOT NULL REFERENCES tournament_location(location_id)
);






