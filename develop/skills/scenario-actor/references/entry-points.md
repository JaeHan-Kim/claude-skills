# Scenario Actor — three ways in, one contract (`agents/actor.md`)

| Called by | How | Inputs arrive as |
|-----------|-----|------------------|
| `scenario-director` | one subagent per spec, in parallel | the dispatch prompt |
| CI (`tests/scenarios/ci.sh`) | `claude -p "/develop:scenario-actor spec=… BASE_URL=… results=…"` | the skill argument line |
| a person | "이 시나리오 하나만 돌려줘" + a spec path | the conversation |
