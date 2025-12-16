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
    
    # Separate numeric and text columns
    numeric_cols = [c for c in col_names if columns[c].get("type") == "numeric"]
    text_cols = [c for c in col_names if columns[c].get("type") == "text"]
    
    lines : list[str]=[]
    lines.append(f"# CSV Profile Report\n")
    lines.append(f"- **Total Columns:** {report.get('total_columns',0)}")
    lines.append(f"- **Total Rows:** {report.get('total_rows',0)}\n")
    
    # Numeric columns table
    if numeric_cols:
        lines.append(f"## Numeric Columns\n")
        lines.append(f"| Column Name | Count | Missing | Unique | Mean | Min | Max  |")
        lines.append(f"|-------------|-------|---------|--------|------|-----|-----|-----------------|")
        for c in numeric_cols:
            col_data = columns.get(c, {})
            count = col_data.get("count", 0)
            missing = col_data.get("missing", 0)
            unique = col_data.get("unique", 0)
            mean = col_data.get("mean")
            min_val = col_data.get("min")
            max_val = col_data.get("max")    
            lines.append(f"| {c} | {count} | {missing} | {unique} | {mean} | {min_val} | {max_val}|")
        lines.append("")
    
    # Text columns table
    if text_cols:
        lines.append(f"## Text Columns\n")
        lines.append(f"| Column Name | Count | Missing | Unique | Top Key (Count) |")
        lines.append(f"|-------------|-------|---------|--------|-----------------|")
        for c in text_cols:
            col_data = columns.get(c, {})
            count = col_data.get("count", 0)
            missing = col_data.get("missing", 0)
            unique = col_data.get("unique", 0)
            top_key = col_data.get("top_key")
            if top_key and isinstance(top_key, dict):
                top_str = f"{top_key['value']} ({top_key['count']})"
            else:
                top_str = "N/A"
            lines.append(f"| {c} | {count} | {missing} | {unique} | {top_str} |")
        lines.append("")
    
    path.write_text("\n".join(lines)+ "\n")