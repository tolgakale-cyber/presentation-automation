import json
from jsonschema import validate

def validate_presentation(data, schema_path):
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(instance=data, schema=schema)
    return True
