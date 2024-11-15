# Context Transition Management Guide

## Core Transition Commands

1. Task Start
```bash
# Load current state
!load specs/knowledge/context/current_state.json

# Set focus
!ctx schoolcalendar.period_template
```

2. State Preservation
```bash
# Save progress
!save current_progress dev {
    "component": "period_template",
    "state": "optimization_phase"
}
```

## Best Practices

1. State Management
- Keep current_state.json updated
- Reference previous work
- Build context incrementally
- Maintain continuity

2. Transition Points
- Save before switching
- Load minimal context
- Add as needed
- Verify state

3. Knowledge Chain
- Link related tasks
- Reference past work
- Track progress
- Maintain history
