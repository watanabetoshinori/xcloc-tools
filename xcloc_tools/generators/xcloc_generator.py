import os
import pathlib
import json
import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring

class XclocGenerator:

    def __init__(self, contents):
        self.contents = contents

    def generate(self):
        self.__generate_directories()
        self.__generate_content_json()
        self.__generate_xliff()
        return self.contents.file

    def __generate_directories(self):
        root_path = pathlib.Path(self.contents.file)
        os.makedirs(root_path / "Localized Contents", exist_ok = True)
        os.makedirs(root_path / "Notes", exist_ok = True)
        os.makedirs(root_path / "Source Contents", exist_ok = True)

    def __generate_content_json(self):
        root_path = pathlib.Path(self.contents.file)

        contents = {
            "developmentRegion" : self.contents.source,
            "targetLocale" : self.contents.target,
            "toolInfo" : {
                "toolBuildNumber" : self.contents.tool.build,
                "toolID" : self.contents.tool.id,
                "toolName" : self.contents.tool.name,
                "toolVersion" : self.contents.tool.version
            },
            "version" : self.contents.version
        }

        with open(root_path / "contents.json", "w") as json_file:
            json.dump(contents, json_file, indent = 2)

    def __generate_xliff(self):
        root_path = pathlib.Path(self.contents.file)

        root = Element("xliff", { 
            "xmlns":"urn:oasis:names:tc:xliff:document:1.2", 
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance", 
            "version": "1.2", 
            "xsi:schemaLocation": "urn:oasis:names:tc:xliff:document:1.2 http://docs.oasis-open.org/xliff/v1.2/os/xliff-core-1.2-strict.xsd" 
        })

        for localized_content in self.contents.localized_contents:
            file = SubElement(root, "file", { "original": localized_content.file, "source-language": localized_content.source, "target-language": localized_content.target, "datatype": "plaintext" })
            header = SubElement(file, "header")
            tool = SubElement(header, "tool", { "tool-id": localized_content.tool.id, "tool-name": localized_content.tool.name, "tool-version": localized_content.tool.version,  "build-num": localized_content.tool.build })
            body = SubElement(file, "body")

            for translation in localized_content.translations:
                trans_unit = SubElement(body, "trans-unit", { "id": translation.id, "xml:space": "preserve" })
                if translation.source:
                    source = SubElement(trans_unit, "source")
                    source.text = translation.source
                if translation.target:
                    target = SubElement(trans_unit, "target")
                    target.text = translation.target
                note = SubElement(trans_unit, "note")
                if translation.note:
                    note.text = ElementTree.fromstring("<root>" + translation.note + "</root>").text

        self.__indent(root)
        tree = ElementTree.ElementTree(root)
        tree.write(root_path / "Localized Contents" / (self.contents.target + ".xliff"), encoding = "utf-8", xml_declaration = True)

    def __indent(self, tree, space = "  ", level = 0):
        # bpo-14465: Add an indent() function to xml.etree.ElementTree to pretty-print XML trees (GH-15200)
        # https://github.com/python/cpython/commit/b5d3ceea48c181b3e2c6c67424317afed606bd39

        # Reduce the memory consumption by reusing indentation strings.
        indentations = ["\n" + level * space]

        def _indent_children(elem, level):
            # Start a new indentation level for the first child.
            child_level = level + 1
            try:
                child_indentation = indentations[child_level]
            except IndexError:
                child_indentation = indentations[level] + space
                indentations.append(child_indentation)

            if not elem.text or not elem.text.strip():
                elem.text = child_indentation

            for child in elem:
                if len(child):
                    _indent_children(child, child_level)
                if not child.tail or not child.tail.strip():
                    child.tail = child_indentation

            # Dedent after the last child by overwriting the previous indentation.
            if not child.tail.strip():
                child.tail = indentations[level]

        _indent_children(tree, 0)