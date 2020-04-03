import os
import dataclasses
from .tool import Tool
from .translation import Translation

@dataclasses.dataclass
class LocalizedContents:
    file: str = ""
    source: str = ""
    target: str = "" 
    tool: Tool = None
    translations: [Translation] = dataclasses.field(default_factory = list)

    @property
    def basename(self):
        return os.path.basename(self.file)
