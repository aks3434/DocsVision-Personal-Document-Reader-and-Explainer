from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


def export_structured_document(
    structured_pages: List[Dict],
    output_path: str | Path
) -> None:
    """
    Export structured document pages to a JSON file.

    Parameters
    ----------
    structured_pages : List[Dict]
        Output from build_page_structure().
    output_path : str | Path
        Destination path for JSON file.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            structured_pages,
            f,
            indent=2,
            ensure_ascii=False
        )
