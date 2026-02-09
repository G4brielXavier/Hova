from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str
    start_ln: int
    start_col: int
    end_ln: int
    end_col: int