from __future__ import annotations
from pathlib import Path
from csv import DictReader



def read_csv_rows(path:str|Path ) -> list[dict[str,str]]:
    path = Path(path)
    with path.open(newline='', encoding='utf-8') as f:
        reader = DictReader(f)
        return [dict(row) for row in reader]

