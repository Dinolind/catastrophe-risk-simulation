CREATE TABLE catastrophe_events (
    event_id INTEGER PRIMARY KEY,
    event_type VARCHAR(50),
    event_date DATE,
    state VARCHAR(50),
    county VARCHAR(100),
    property_damage NUMERIC,
    year INTEGER
);