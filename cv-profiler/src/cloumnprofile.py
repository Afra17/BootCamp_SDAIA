class Colunmprofile:
    def __init__(self,name:str, inferred_type:str, total:int, missing:int, unique:int):
        self.name = name
        self.inferred_type = inferred_type
        self.total = total
        self.massing = missing
        self.unique = unique

    @property
    def missing_pct(self) -> float:
       return 0.0 if self.total == 0 else (self.missing / self.total) * 100
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "inferred_type": self.inferred_type,
            "total": self.total,
            "massing": self.massing,
            "missing_pct": self.missing_pct,
            "unique": self.unique
        }
    
    def __repr__(self) -> str:
        return f"Cloumnprofile(name={self.name}, type={self.inferred_type},total={self.total}, missing={self.missing}, unique={self.unique})"
    
    def is_missing_value(self ,value:str|None) -> bool:
        non_list=["","na","n/a","null","none","nan"]
        if value is None:
            return True
        return value.strip().lower() in non_list
    

    def try_float(self,v:str) -> float|None:
        try:
            return float(v)
        except ValueError:
            return None
        
    def infer_type(self,values: list[str]) -> str:
        usable=[v for v in values if not self.is_missing_value(v)]
        if not usable:
            return "text"
        for v in usable:
            if self.try_float(v) is None:
                return "text"
        return "numeric" 
            
    def numeric_stats(self,values: list[str]) -> dict:
        usable = [v for v in values if not self.is_missing_value(v)]
        missing = len(values) - len(usable)
        nums: list[float] = []
        for v in usable:
            x = Colunmprofile.try_float(v)
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

