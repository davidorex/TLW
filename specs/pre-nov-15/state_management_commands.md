# State Management Command Set Documentation

## Overview
This command set provides capabilities for managing assistant state, memory, and context during development and analysis tasks.

## Commands

### SAVE STATE
Persists typed data under a specified key
```
!save {key} {type} {data}
Example: !save auth_model arch { interfaces: [], patterns: [] }
```
Purpose: Store complex data structures with type information for later use

### LOAD STATE
Retrieves previously saved state
```
!load {key}
Example: !load auth_model
```
Purpose: Recall stored data structures and configurations

### REFERENCE
Uses saved state in current operations
```
!ref {key}
Example: Using !ref auth_model, add OAuth
```
Purpose: Reference and build upon previously saved work

### COMPRESS
Optimizes content for storage
```
!zip {content}
Example: !zip project_structure
```
Purpose: Efficiently store large data structures or project states

### CONTEXT
Manages analysis scope and focus
```
!ctx {scope}
Example: !ctx auth.login
```
Purpose: Switch between different areas of analysis while maintaining state

### CLEAR
Resets all state information
```
!clear
```
Purpose: Clear memory and start fresh when needed

## Usage Context
These commands enable:
- Persistent storage of analysis results
- Context-aware operations
- Memory management
- State referencing
- Scope control
- Clean state resets
