ALTER TABLE accepted_solutions ADD COLUMN IF NOT EXISTS small_diff_embedding vector(%s); 
ALTER TABLE accepted_solutions ADD COLUMN IF NOT EXISTS original_code_embedding vector(%s); 
ALTER TABLE incidents ADD COLUMN IF NOT EXISTS incident_snip_embedding vector(%s); 