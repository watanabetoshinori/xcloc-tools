import os
import pathlib
import dataclasses
from .tool import Tool
from .localized_contents import LocalizedContents

@dataclasses.dataclass
class Contents:
    file: str = ""
    source: str = ""
    target: str = "" 
    version: str = ""
    tool: Tool = None
    localized_contents: [LocalizedContents] = dataclasses.field(default_factory = list)
    screenshots: {str: str} = dataclasses.field(default_factory = dict)

    @property
    def basename(self):
        return os.path.basename(self.file)

    @property
    def stem(self):
        return pathlib.Path(self.file).stem

