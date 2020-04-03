import dataclasses

@dataclasses.dataclass
class Translation:
    id: str = ""
    source: str = ""
    target: str = ""
    note: str = ""