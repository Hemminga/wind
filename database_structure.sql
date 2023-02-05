CREATE TABLE wind (
    id SERIAL,
    station TEXT,
    weather TEXT,
    temperature DECIMAL,
    chill DECIMAL,
    humidity INTEGER,
    wind TEXT,
    windspeed INTEGER,
    windgusts INTEGER,
    visibility INTEGER,
    pressure DECIMAL,
    observation TIMESTAMPTZ,
    UNIQUE(station, observation));