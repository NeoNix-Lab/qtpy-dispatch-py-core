from pathlib import Path
from datamodel_code_generator import InputFileType, generate

def generate_models(schema_dir: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    imports = []
    for schema_file in sorted(schema_dir.glob('*.json')):
        output_file = out_dir / f"{schema_file.stem}.py"
        generate(
            schema_file.read_text(),
            input_file_type=InputFileType.JsonSchema,
            input_filename=schema_file.name,
            output=output_file,
        )
        imports.append(f"from .{schema_file.stem} import *")
    if imports:
        with open(out_dir / '__init__.py', 'w') as f:
            f.write('\n'.join(imports) + '\n')
