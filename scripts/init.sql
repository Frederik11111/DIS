CREATE TABLE IF NOT EXISTS players (
    -- Her skal I definere kolonnerne, der matcher jeres CSV, f.eks.:
    sofifa_id INT PRIMARY KEY,
    short_name VARCHAR(100),
    player_positions VARCHAR(100)
    -- osv...
);

-- Indlæs data fra CSV'en (som vi lige har mappet ind i /tmp)
COPY players FROM '/tmp/players_22.csv' DELIMITER ',' CSV HEADER;