import pandas as pd
import typer 


non_list=["","na","n/a","null","none","nan"]

def is_missing_value(value:str|None) -> bool:
    if value is None:
        return True
    return value.strip().lower() in non_list



def try_float(v:str) -> float|None:
    try:
        return float(v)
    except ValueError:
        return None
    
def infer_type(values: list[str]) -> str:
    usable=[v for v in values if not is_missing_value(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "numeric" 



def numeric_stats(values: list[str]) -> dict:
    usable = [v for v in values if not is_missing_value(v)]
    missing = len(values) - len(usable)
    nums: list[float] = []
    for v in usable:
        x = try_float(v)
        if x is None:
            raise ValueError(f"Non-numeric value found: {v!r}")
        nums.append(x)

    count = len(nums)
    unique = len(set(nums))
    mean = sum(nums) / count if count > 0 else None
    max_val = max(nums) if nums else None
    min_val = min(nums) if nums else None

    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "mean": mean,
        "min": min_val,
        "max": max_val,
    }

def by_count(pair):
    return pair[1]

def text_stats(values: list[str],top_k: int=5) -> dict:
    usable = [v for v in values if not is_missing_value(v)]
    missing = len(values) - len(usable)

    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1
    top_items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True) [:top_k]# sort by count from small to laege
    top=[{  "value": v, "count": c} for v, c in top_items]

    return{

        "count": len(usable),
        "missing": missing,
        "top": top,

    }
    
def basic_profile(rows : list[dict[str,str]]) -> dict:
    if not rows:
        return {"rows":0, "columns":{},"notes":["empty dataset"]}
    
    columns=list(rows[0].keys())
    missing={col:0 for col in columns}
    non_empty={col:0 for col in columns}
    values = {col: [] for col in columns}
    for row in rows:
        for col in columns:
            v=(row.get(col) or "").strip()
            if v=="":
                missing[col]+=1 
            else:
                non_empty[col]+=1
                values[col].append(v)

    profile = {
        "total_rows": len(rows),
        "total_columns": len(columns),
        "columns": {}
    }
    for col in columns:
        col_values = values[col]
        col_type = infer_type(col_values)
        
        if col_type == "numeric":
            stats = numeric_stats(col_values)
            profile["columns"][col] = {
                "count": stats["count"],
                "missing": stats["missing"],
                "unique": stats["unique"],
                "type": col_type,
                "mean": stats["mean"],
                "min": stats["min"],
                "max": stats["max"],
      }
        else:
            stats = text_stats(col_values)
            unique = len(set(col_values))
            top_key = stats["top"][0] if stats["top"] else None
            profile["columns"][col] = {
                "count": stats["count"],
                "missing": stats["missing"],
                "unique": unique,
                "type": col_type,
                "top_key": top_key
            }
        
    
    return profile


def cloumn_value(rows:list[dict[str,str]], column_name:str) -> list[str]:
    return [row.get(column_name,"") for row in rows]
