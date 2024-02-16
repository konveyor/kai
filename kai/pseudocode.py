# Konveyor GenAI service, somehow exists?

# Three user entry points:
# 1. Initial seeding
# 2. Send over the incident to generate a solution for
#    - Returns a solution
# 3. Accept or reject the solution

# Do an analysis of our application
# - Send the results or do the analysis of the application
# - Store those results
# - (There is something here about invalidating/checking old runs of the
#   analysis engine for the same application)

# The user selects an incident/violation/whatever to fix, which has a code
# location

# We need to build the prompt, which needs:
# 1. Current code snippet
# 2. Hint of what to fix from analysis metadata (?)
# 3. Similar solved example snippet(s)

# To get 3, query the incident store, which is a database of all the incidences
# that have yet to be solved and incidences that have been solved

# Call to an LLM with the prompt (configurable)

# Send back to user

# If accepted, update the incident store, otherwise undo everything ever


# Nail down data
# - The repo is nebuluously already there
# - The analysis is run server-side
