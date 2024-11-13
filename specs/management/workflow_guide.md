# GPT Management Workflow Guide

## Starting New Development

1. Initialize Context
```
!ctx schoolcalendar
!load specs/knowledge/context/current_state.json
```

2. Access Patterns
```
!ref specs/knowledge/core/architecture.json
```

## Managing Development State

1. Save Progress
```
!save current specs/development/vectors/period_template/current_state.json
```

2. Update Context
```
!ctx period_template
!ref specs/development/vectors/period_template/current_state.json
```

## Token Optimization Practices

1. Use Compressed References
- Store in specs/knowledge/core/
- Reference specific sections
- Use !zip for large states

2. Context Management
- Keep specs/knowledge/context/current_state.json minimal
- Update only relevant sections
- Clear unused contexts

## Maintaining Project Vision

1. Update Vision Files
- specs/vision/current/overview_human.md
- specs/vision/current/overview_gpt.json

2. Track Development
- specs/development/vectors/{component}/current_state.json
- Archive completed states to timeline/

## Common Patterns

1. Feature Development
- Set component context
- Load architectural patterns
- Save incremental progress

2. Optimization Work
- Focus context on target
- Reference existing patterns
- Track improvements

3. Integration Tasks
- Load related components
- Reference shared patterns
- Update integration state
