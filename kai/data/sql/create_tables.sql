CREATE TABLE IF NOT EXISTS applications (
  application_id   SERIAL PRIMARY KEY,
  application_name TEXT NOT NULL,
  repo_uri         TEXT NOT NULL,
  current_branch   TEXT NOT NULL,
  current_commit   TEXT NOT NULL,
  generated_at     TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS rulesets (
  ruleset_id     SERIAL PRIMARY KEY,
  ruleset_name   TEXT NOT NULL,
  application_id INT REFERENCES applications,
  tags           JSONB NOT NULL
);

DO $$ BEGIN
  CREATE TYPE violation_category_t AS ENUM (
    'potential', 'optional', 'mandatory'
  );          
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS violations (
  violation_id   SERIAL PRIMARY KEY,
  violation_name TEXT NOT NULL,
  ruleset_id     INT REFERENCES rulesets,
  category       violation_category_t NOT NULL,
  labels         JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS accepted_solutions (
  solution_id         SERIAL PRIMARY KEY,
  generated_at        TIMESTAMP DEFAULT current_timestamp,
  solution_big_diff   TEXT NOT NULL,
  solution_small_diff TEXT NOT NULL,
  embedding           vector(%s)
);

CREATE TABLE IF NOT EXISTS incidents (
  incident_id         SERIAL PRIMARY KEY,
  violation_id        INT REFERENCES violations,
  incident_uri        TEXT NOT NULL,
  incident_snip       TEXT NOT NULL,
  incident_line       INT NOT NULL,
  solution_id         INT REFERENCES accepted_solutions
);

CREATE TABLE IF NOT EXISTS potential_solutions (
  solution_id         SERIAL PRIMARY KEY,
  generated_at        TIMESTAMP DEFAULT current_timestamp,
  solution_big_diff   TEXT NOT NULL,
  solution_small_diff TEXT NOT NULL,
  incident_id         INT REFERENCES Incidents
);

-- CREATE TABLE IF NOT EXISTS embeddings (
--   embedding_id   SERIAL PRIMARY KEY,
--   embedding_name TEXT NOT NULL,
--   incident_id    INT,
--   embedding      vector(%s),
--   FOREIGN KEY (incident_id)
--     REFERENCES solved_incidents(incident_id)
-- );