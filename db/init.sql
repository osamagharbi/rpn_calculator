-- db/init.sql

CREATE TABLE IF NOT EXISTS calculations (
    id SERIAL PRIMARY KEY,
    expression VARCHAR(255) NOT NULL,
    result FLOAT NOT NULL
);
