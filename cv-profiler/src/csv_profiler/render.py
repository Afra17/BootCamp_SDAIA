from __future__ import annotations
import json 
from pathlib import Path

def write_json(report:dict, path:str|Path) -> None:
    path= Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False)+ "\n")
                    
def write_markdown(report:dict, path:str|Path) -> None:

    path=Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    columns = report.get("columns", {})
    col_names = list(columns.keys())
    lines : list[str]=[]
    lines.append(f"# CSV Profile Report\n")
    lines.append(f"- **Total Columns:** {report.get('total_columns',0)}")
    lines.append(f"- **Total Rows:** {report.get('total_rows',0)}\n")
    lines.append(f"## Column Statistics\n")
    lines.append(f"| Column Name | Count | Missing | Unique | Type | Mean | Min | Max | Top Key (Count) |")
    lines.append(f"|-------------|-------|---------|--------|------|------|-----|-----|-----------------|")   
    for c in col_names:
        col_data = columns.get(c, {})
        count = col_data.get("count", 0)
        missing = col_data.get("missing", 0)
        unique = col_data.get("unique", 0)
        col_type = col_data.get("type", "unknown")
        mean = col_data.get("mean")
        min_val = col_data.get("min")
        max_val = col_data.get("max")
        top_key = col_data.get("top_key", "N/A")
        lines.append(f"| {c} | {count} | {missing} | {unique} | {col_type} |{mean}|{min_val}|{max_val}|{top_key} |")
    lines.append("")
    path.write_text("\n".join(lines)+ "\n")