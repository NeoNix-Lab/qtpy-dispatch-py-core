"""Helpers for generating Pydantic models from JSON schemas."""

import os
from pathlib import Path

from datamodel_code_generator import InputFileType, generate


def generate_models(schema_dir: Path, out_dir: Path) -> None:
    """Generate Pydantic models for all JSON schemas in ``schema_dir``."""

    out_dir.mkdir(parents=True, exist_ok=True)
    _append_init(out_dir)
    imports = []
    for schema_file in sorted(schema_dir.glob("*.json")):
        output_file = out_dir / f"{schema_file.stem}.py"
        generate(
            schema_file.read_text(),
            input_file_type=InputFileType.JsonSchema,
            input_filename=schema_file.name,
            output=output_file,
        )
        imports.append(f"from .{schema_file.stem} import *")
    if imports:
        with open(out_dir / "__init__.py", "w") as f:
            f.write("\n".join(imports) + "\n")


def _append_init(dir_path: Path) -> None:
    """Create an empty ``__init__`` in ``dir_path`` if missing."""

    (dir_path / "__init__.py").write_text("")


def get_shared_dir() -> Path:
    """Return the shared schema directory from ``QT_SDK_PATH`` env var."""

    return Path(os.environ["QT_SDK_PATH"])
