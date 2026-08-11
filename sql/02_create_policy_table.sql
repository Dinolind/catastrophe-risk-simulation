CREATE TABLE policies (
    policy_id INTEGER PRIMARY KEY,
    state VARCHAR(50),
    property_value NUMERIC,
    coverage_amount NUMERIC,
    deductible NUMERIC,
    annual_premium NUMERIC
);