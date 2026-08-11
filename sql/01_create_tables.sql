CREATE TABLE catastrophe_events (
    id SERIAL PRIMARY KEY,
    event_id INTEGER,
    event_type VARCHAR(50),
    event_date DATE,
    state VARCHAR(50),
    county VARCHAR(100),
    property_damage NUMERIC,
    year INTEGER
);