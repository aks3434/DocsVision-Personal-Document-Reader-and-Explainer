from __future__ import annotations

from collections import defaultdict
from typing import Dict, List


def build_page_structure(blocks: List[Dict]) -> List[Dict]:
    """
    Group document blocks into structured pages and sections.

    Output format:
    [
      {
        "page": 1,
        "sections": [
          {
            "heading": "Introduction",
            "blocks": [ ... ]
          }
        ]
      }
    ]
    """

    pages = defaultdict(list)

    # 1️⃣ Group blocks by page
    for block in blocks:
        pages[block["page"]].append(block)

    structured_pages: List[Dict] = []

    # 2️⃣ Process each page
    for page_num in sorted(pages.keys()):
        page_blocks = pages[page_num]

        # Sort top → bottom using bbox y-coordinate
        page_blocks.sort(key=lambda b: b["bbox"][1])

        sections = []
        current_section = {
            "heading": None,
            "blocks": []
        }

        for block in page_blocks:
            block_type = block.get("block_type")

            if block_type == "heading":
                # Start new section
                if current_section["blocks"]:
                    sections.append(current_section)

                current_section = {
                    "heading": block["text"],
                    "blocks": []
                }

            elif block_type in {"paragraph", "footer"}:
                current_section["blocks"].append(block)

            # ignore noise silently

        # Append last section
        if current_section["blocks"]:
            sections.append(current_section)

        structured_pages.append({
            "page": page_num,
            "sections": sections
        })

    return structured_pages
