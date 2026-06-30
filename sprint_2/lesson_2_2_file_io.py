import os
from pathlib import Path


def write_secure_file(file_path: str, content: str, output_dir: str = "output") -> str:
    """Write content safely inside the output directory."""
    if not file_path:
        raise ValueError("file_path must not be empty.")

    output_dir_path = Path(output_dir).resolve()
    target_path = Path(file_path).resolve()

    if not str(target_path).startswith(str(output_dir_path) + os.sep) and target_path != output_dir_path:
        raise ValueError(
            "Security violation: writing outside the output directory is not allowed."
        )

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    return str(target_path)
