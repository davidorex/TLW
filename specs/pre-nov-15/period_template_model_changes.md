# PeriodTemplate Model Changes

## Before Changes
The PeriodTemplate model was missing the required METADATA_SCHEMA definition which is needed for inheriting from MetadataModel.

## After Changes
Added METADATA_SCHEMA to the PeriodTemplate model:

```python
class PeriodTemplate(MetadataModel):
    METADATA_SCHEMA = {
        "type": "object",
        "properties": {
            "assessment_weeks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "week_number": {"type": "integer"},
                        "type": {"type": "string", "enum": ["formative", "summative"]}
                    }
                }
            },
            "special_events": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "format": "date"},
                        "description": {"type": "string"}
                    }
                }
            }
        }
    }
```

## Key Changes
1. Added METADATA_SCHEMA class attribute
2. Defined schema structure for:
   - Assessment weeks tracking
   - Special events tracking
3. Specified data types and validation rules
4. Ensured compliance with MetadataModel requirements

## Rationale
- Required by MetadataModel base class
- Enables structured storage of:
  - Assessment week information
  - Special event details
- Provides validation for metadata content
- Supports consistent data structure across instances
