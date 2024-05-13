# We need to solve the n -> n+1 problem

INSERT, UPDATE, and DELETE

can use JSONB as postgres type

instead of the solved_branch business, only keep track of current branch, commit, etc... Then when we get the analysis report, supply that stuff

```sql
CREATE TABLE IF NOT EXISTS applications (
  application_id SERIAL PRIMARY KEY,
  application_name TEXT NOT NULL,
  repo_uri       TEXT NOT NULL,
  current_branch TEXT NOT NULL,
  current_commit TEXT NOT NULL,
  time_generated TEXT NOT NULL
  -- report ?
);

```
