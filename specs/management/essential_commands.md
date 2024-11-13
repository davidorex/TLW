# Essential GPT Management Commands

## Core Commands

### Context Management
```
!ctx {scope}     - Set working context
!clear           - Reset context
```

### State Operations
```
!save {key} {type} {data}  - Save state
!load {key}                - Load state
!ref {key}                 - Reference state
!zip {content}             - Compress content
```

## Basic Workflow

1. Set Context
- Use !ctx to focus GPT on specific component
- Clear previous context if needed

2. Manage State
- Save important states with !save
- Load needed context with !load
- Reference specific states with !ref

3. Optimize Tokens
- Compress verbose content with !zip
- Load only necessary context
- Clear unused states

## Directory Usage

- /specs/vision/      - Project direction
- /specs/development/ - Active development
- /specs/knowledge/   - Core patterns
- /specs/current/     - Active state

## Tips

1. Keep contexts focused
2. Save incremental progress
3. Use compressed references
4. Clear unused states
5. Maintain clean state hierarchy
