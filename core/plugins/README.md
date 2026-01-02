# Plugin Contract

## Requirements
- Implement BasePlugin
- Define `name` and `version`
- Implement `run(payload: dict) -> dict`

## Lifecycle
1. Initialized by Core
2. Executed via `run`
3. Optional cleanup via `shutdown`

## Error Handling
- Raise PluginExecutionError on failure
