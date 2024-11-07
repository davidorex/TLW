# Core Abstract Models (core/models/abstracts.py)

### Required Configuration
```python
Required Settings:
USE_HISTORY = True    # Enable history tracking
USE_FSM = True       # Enable state machine
METADATA_VALIDATION = True  # Enable schema validation

Required Libraries:
- django-simple-history>=3.3.0
- django-model-utils>=4.3.1
- django-safedelete>=1.3.1
- django-fsm>=2.8.1
- pydantic>=2.0.0  # For metadata validation
```

### BaseModel
```python
Purpose: Foundation for all system models

Fields:
- id: UUIDField
    primary_key=True
    default=uuid4
    editable=False
    db_index=True
    help_text="Unique identifier for this object"

- is_active: BooleanField
    default=True
    db_index=True
    help_text="Soft deletion status"

- created_at: AutoDateTimeField
    auto_now_add=True
    db_index=True
    help_text="Timestamp when object was created"

- modified_at: AutoDateTimeField
    auto_now=True
    help_text="Timestamp when object was last modified"

Meta:
- abstract = True
- ordering = ['-created_at']
- indexes = [
    models.Index(fields=['created_at', 'is_active'])
  ]

Managers:
- objects = BaseManager()
- active = ActiveManager()

Methods:
- soft_delete()
- restore()
- hard_delete()

Properties:
- is_deleted
- active_status
```

### AuditableModel
```python
Purpose: User action tracking
Inherits: BaseModel

Fields:
- created_by: ForeignKey
    settings.AUTH_USER_MODEL
    null=True
    on_delete=models.SET_NULL
    related_name="%(class)s_created"
    help_text="User who created this object"

- modified_by: ForeignKey
    settings.AUTH_USER_MODEL
    null=True
    on_delete=models.SET_NULL
    related_name="%(class)s_modified"
    help_text="User who last modified this object"

Methods:
- save(user=None)
    Updates user fields from passed user or context

- get_creator_name()
    Returns string representation of creator

- get_modifier_name()
    Returns string representation of last modifier

Signals:
- pre_save: Ensure user tracking
- post_save: Log audit event
```

### HistoricalModel
```python
Purpose: Change tracking and versioning
Inherits: AuditableModel

Configuration:
- history = HistoricalRecords(
    inherit=True,
    cascade_delete_history=True,
    user_model=settings.AUTH_USER_MODEL,
    table_name='core_historical_%(class)s',
    custom_model_name=lambda x: f'Historical{x}',
    excluded_fields=['modified_at'],
    bases=[SafeDeleteHistoricalModel]
  )

Fields:
- change_reason: CharField
    max_length=255
    null=True
    help_text="Reason for this change"

Methods:
- get_history_type_display()
- revert_to(history_id)
- get_version_at(timestamp)
- diff_with(other_version)

Properties:
- previous_version
- next_version
- has_changes
```

### MetadataModel
```python
Purpose: Flexible metadata storage with validation
Inherits: HistoricalModel

Fields:
- metadata: JSONField
    default=dict
    validators=[validate_metadata_schema]
    help_text="JSON metadata storage"

Schema Validation:
- Must define METADATA_SCHEMA in model
- Uses Pydantic for validation
- Supports nested schemas
- Version tracking for schema changes

Methods:
- get_metadata(key, default=None)
    Returns value for key with optional default

- set_metadata(key, value)
    Sets and validates single metadata value

- update_metadata(data_dict)
    Bulk updates with validation

- validate_metadata()
    Full schema validation

Properties:
- metadata_schema
- has_metadata
- valid_metadata

Signals:
- pre_save: Validate metadata
- post_init: Setup schema validation
```

### Implementation Notes
```python
1. Core Utilities Required:
   - core/utils/context.py: User context management
   - core/utils/metadata.py: Schema validation
   - core/utils/history.py: History helpers

2. Manager Classes Needed:
   - BaseManager: Basic functionality
   - ActiveManager: Active instance filtering
   - HistoricalManager: Version management

3. Test Coverage Required:
   - Soft deletion behavior
   - User tracking accuracy
   - History recording
   - Metadata validation
   - Manager functionality
   - Signal handling
   - Schema validation
   - Reversion capabilities

4. Documentation:
   - Full docstring coverage
   - Type hints
   - Usage examples
   - Schema definitions
```

### Example Usage
```python
from core.models.abstracts import MetadataModel

class MyModel(MetadataModel):
    METADATA_SCHEMA = {
        "type": "object",
        "properties": {
            "key": {"type": "string"},
            "value": {"type": "integer"}
        }
    }
    
    # Model gets all base functionality:
    # - UUID pk
    # - Soft delete
    # - User tracking
    # - History
    # - Metadata with validation
```

Should I continue with the SchoolYear spec that builds on these abstractions?