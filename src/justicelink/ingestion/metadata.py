"""
JusticeLink AI: Ingests the Kerala court discovery tree and CNR sample keys.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd


def parse_kerala_courts_tree(json_path: str | Path) -> pd.DataFrame:
    with open(json_path, "r", encoding="utf-8") as f:
        tree = json.load(f)

    districts = tree.get("Kerala", {}).get("districts", {})
    records: List[Dict[str, Any]] = []

    for dist_name, dist_info in districts.items():
        dstvalue = dist_info.get("dstvalue", "")
        for comp_name, comp_info in dist_info.get("court_complexes", {}).items():
            records.append({
                "state": "Kerala",
                "state_code": 4,
                "district": dist_name,
                "district_code": dstvalue,
                "court_complex": comp_name,
                "court_value": comp_info.get("crtvalue", ""),
            })

    return pd.DataFrame(records)


def parse_sample_case_keys(keys_path: str | Path) -> pd.DataFrame:
    records: List[Dict[str, str]] = []
    with open(keys_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 4:
                records.append({
                    "district": parts[0],
                    "court_complex": parts[1],
                    "case_query_id": parts[2],
                    "cnr": parts[3],
                })
    return pd.DataFrame(records)
