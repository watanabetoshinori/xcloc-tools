import os
import json
import re
import pathlib
import xml.etree.ElementTree as ElementTree
from models import Contents, Tool, LocalizedContents, Translation

class XclocParser:

    def __init__(self, path):
        if path.exists() == False:
            raise IOError("No such file or directory: {}".format(path))

        if path.is_dir() == False:
            raise TypeError("File is not xcloc format: {}".format(path))

        self.xcloc_path = path

        self.contents_json_path = path / "Contents.json"
        if self.contents_json_path.exists() == False:
            raise TypeError("File is not xcloc format. Contents.json not found.: {}".format(self.contents_json_path))

        self.source_contents_path = path / "Source Contents"
        if self.source_contents_path.exists() == False:
            raise TypeError("File is not xcloc format. Source Contents directory not found.: {}".format(self.source_contents_path))

        self.notes_path = path / "Notes"
        if self.notes_path.exists() == False:
            raise TypeError("File is not xcloc format. Notes directory not found.: {}".format(self.notes_path))

        self.localized_contents_path = path / "Localized Contents"
        if self.localized_contents_path.exists() == False:
            raise TypeError("File is not xcloc format. Localized Contents directory not found.: {}".format(self.localized_contents_path))

        self.xliff_path = self.localized_contents_path / (path.stem + ".xliff")
        if self.xliff_path.exists() == False:
            raise TypeError("File is not xcloc format. xliff file not found.: {}".format(self.xliff_path))

    def parse(self):
        contents = Contents(file = str(self.xcloc_path))

        self.__parse_contents_json(contents)
        self.__parse_xliff(contents)
        self.__parse_screenshots(contents)

        return contents

    def __parse_contents_json(self, contents):
        with open(self.contents_json_path, "r") as contents_json:
            root = json.load(contents_json)
            contents.source = root["developmentRegion"]
            contents.target = root["targetLocale"]
            contents.version = root["version"]

            tool_info = root["toolInfo"]
            tool = Tool()
            tool.id = tool_info["toolID"]
            tool.name = tool_info["toolName"]
            tool.version = tool_info["toolVersion"]
            tool.build = tool_info["toolBuildNumber"]
            contents.tool = tool
    
    def __parse_xliff(self, contents):
        ns = {"xliff": "urn:oasis:names:tc:xliff:document:1.2"}

        tree = ElementTree.parse(self.xliff_path)
        root = tree.getroot()

        for file in root:
            localized_contents = LocalizedContents()
            localized_contents.file = file.get("original")
            localized_contents.source = file.get("source-language")
            localized_contents.target = file.get("target-language")

            header = file.find("xliff:header", ns)
            header_tool = header.find("xliff:tool", ns)
            tool = Tool()
            tool.id = header_tool.get("tool-id")
            tool.name = header_tool.get("tool-name")
            tool.version = header_tool.get("tool-version")
            tool.build = header_tool.get("build-num")
            localized_contents.tool = tool

            for trans_unit in (body := file.find("xliff:body", ns)):
                translation = Translation()
                translation.id = trans_unit.get("id")

                if (source_tag := trans_unit.find("xliff:source", ns)) is not None:
                    translation.source = source_tag.text

                if (target_tag := trans_unit.find("xliff:target", ns)) is not None:
                    translation.target = target_tag.text

                if (note_tag := trans_unit.find("xliff:note", ns)) is not None:
                    translation.note = note_tag.text

                localized_contents.translations.append(translation)
            
            contents.localized_contents.append(localized_contents)
    
    def __parse_screenshots(self, contents):
        screenshots = [file for file in os.listdir(self.notes_path) if re.search(r'(.png)$', file)]
        contents.screenshots = dict(map(lambda f: (pathlib.Path(f).stem, str(self.notes_path / f)), screenshots))
