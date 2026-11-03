DROP TABLE IF EXISTS manhattan_populations;

CREATE TABLE manhattan_populations (
    id SERIAL PRIMARY KEY,
    borough VARCHAR(50),
    year INT,
    fips_county_code INT,
    nta_code VARCHAR(20),
    nta_name VARCHAR(150),
    population INT
);
