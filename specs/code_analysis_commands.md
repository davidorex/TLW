# Code Analysis Command Set Documentation

## Overview
This command set provides comprehensive static analysis capabilities for codebase inspection, pattern detection, and architectural analysis.

## Commands

### SCAN
Traverses directory structure to specified depth
```
!scan {directory} {depth}
Example: !scan src/auth 2
```

### MAP DEPENDENCIES 
Generates dependency graph
```
!map deps
```

### DETECT PATTERNS
Identifies code patterns and common structures
```
!detect patterns
```

### INFER
Performs analysis for specific aspects:
- Architecture (`arch`)
- Design patterns (`patterns`) 
- Risk areas (`risks`)
- Coverage gaps (`gaps`)
- Technical debt (`tech-debt`)
```
!infer {type}
```

### SUMMARIZE
Generates reports with configurable scope and detail
```
!sum {scope} {detail_level}
```

## Usage Context
These commands form an integrated toolkit for:
- Architectural analysis
- Dependency mapping
- Pattern recognition
- Risk assessment
- Technical debt identification
- Documentation generation
