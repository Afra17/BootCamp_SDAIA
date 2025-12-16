class Cloumnprofile:
    def __init__(self,name:str, inferred_type:str, total:int, missing:int, unique:int):
        self.name = name
        self.inferred_type = inferred_type
        self.total = total
        self.missing = missing
        self.unique = unique

    @property
    def missing_pct(self) -> float:
       return 0.0 if self.total ==0 else (self.missing / self.total) * 100
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "inferred_type": self.inferred_type,
            "total": self.total,
            "missing": self.missing,
            "missing_pct": self.missing_pct,
            "unique": self.unique
        }
    
    def __repr__(self) -> str:
        return f"Cloumnprofile(name={self.name}, type={self.inferred_type}, total={self.total}, missing={self.missing}, unique={self.unique})"