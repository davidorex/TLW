"""Metadata schema validation utilities."""
from typing import Any, Dict, Optional
from pydantic import BaseModel, ValidationError

class MetadataValidator:
    """Validator for model metadata using Pydantic schemas."""

    def __init__(self, schema: Dict[str, Any]):
        """Initialize validator with schema definition."""
        class DynamicSchema(BaseModel):
            model_config = {
                "extra": "forbid"
            }

        self.schema = schema
        # Dynamically create Pydantic model from schema
        self.validator = type(
            'MetadataSchema',
            (DynamicSchema,),
            {
                "__annotations__": self._build_annotations(schema)
            }
        )

    def _build_annotations(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Build type annotations from JSON schema."""
        annotations = {}
        if "properties" in schema:
            for field_name, field_schema in schema["properties"].items():
                field_type = self._get_python_type(field_schema)
                if "required" in schema and field_name in schema["required"]:
                    annotations[field_name] = field_type
                else:
                    annotations[field_name] = Optional[field_type]
        return annotations

    def _get_python_type(self, field_schema: Dict[str, Any]) -> Any:
        """Convert JSON schema types to Python types."""
        type_mapping = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict
        }
        return type_mapping.get(field_schema.get("type", "string"), Any)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate metadata against schema."""
        try:
            validated_data = self.validator(**data)
            return validated_data.model_dump()
        except ValidationError as e:
            raise ValueError(f"Metadata validation failed: {str(e)}")

def validate_metadata_schema(value: Dict[str, Any]) -> None:
    """Django model field validator for metadata."""
    if not isinstance(value, dict):
        raise ValueError("Metadata must be a dictionary")
