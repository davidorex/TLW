# Specs Directory Structure

## Overview
This directory maintains project knowledge, state, and development vectors optimized for GPT code generation and project management.

## Directory Structure

```
specs/
├── vision/                           # Project vision and direction
│   ├── current/
│   │   ├── overview_human.md         # Human-readable project state
│   │   ├── overview_gpt.json         # GPT-optimized context
│   │   ├── architecture.json         # Current architectural principles
│   │   └── priorities.json           # Current development priorities
│   └── timeline/                     # Vision evolution tracking
│       └── 2024-Q1/
│           └── initial_vision.json
│
├── development/                      # Development management
│   ├── vectors/
│   │   ├── period_template/          # Period template system
│   │   │   ├── current_state.json
│   │   │   └── optimization.json
│   │   ├── calendar/                 # Calendar functionality
│   │   │   ├── current_state.json
│   │   │   └── integration.json
│   │   └── frontend/                 # Frontend development
│   │       ├── current_state.json
│   │       └── components.json
│   └── state/
│       ├── current_focus.json        # Active development areas
│       └── progress.json             # Development metrics
│
├── knowledge/                        # Optimized knowledge storage
│   ├── core/
│   │   ├── architecture.json         # Core architectural understanding
│   │   ├── patterns.json            # Implementation patterns
│   │   └── constraints.json         # System constraints
│   └── context/
│       ├── current_state.json       # Active context
│       └── references.json          # Compressed knowledge references
│
└── current/                         # Active working files
    ├── vectors/                     # Current state vectors
    │   ├── period_template.json
    │   └── frontend.json
    └── reports/                     # Current status reports
        └── optimization.json
```

## Usage

### For GPT Code Generation
- Load current context: `!load specs/knowledge/context/current_state.json`
- Reference patterns: `!ref specs/knowledge/core/patterns.json`
- Set development focus: `!ctx specs/development/state/current_focus.json`

### For Project Management
- Track development progress
- Maintain architectural knowledge
- Guide implementation decisions
- Optimize token usage

### File Naming Conventions
- Current state files: `current_state.json`
- Vector files: `{component}_vector.json`
- Timeline files: Include date/version
