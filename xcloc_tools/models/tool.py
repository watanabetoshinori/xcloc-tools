import dataclasses

@dataclasses.dataclass
class Tool:
    id: str = ""
    name: str = ""
    version: str = ""
    build: str = ""