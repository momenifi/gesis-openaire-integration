import json
import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from urllib.parse import quote


def prettify(elem):
    rough_string = ET.tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="UTF-8")


def clean_tag(tag):
    tag = str(tag)

    # @id -> id, @type -> type, @none -> none
    if tag.startswith("@"):
        tag = tag[1:]

    # Ungültige XML-Zeichen durch "_" ersetzen
    tag = re.sub(r"[^a-zA-Z0-9_.-]", "_", tag)

    # XML-Tags dürfen nicht mit Ziffer, Punkt oder Minus anfangen
    if not tag or re.match(r"^[0-9.-]", tag):
        tag = "_" + tag

    return tag


def escape_identifier(value):
    if value is None:
        return ""
    return quote(str(value), safe="")


def build_xml(parent, data):
    if isinstance(data, dict):
        for key, value in data.items():
            tag = clean_tag(key)
            child = ET.SubElement(parent, tag)
            build_xml(child, value)

    elif isinstance(data, list):
        for item in data:
            child = ET.SubElement(parent, "item")
            build_xml(child, item)

    else:
        if data is None:
            parent.text = None
        else:
            parent.text = str(data)


with open("bib_GWS_enriched.json", "r", encoding="utf-8") as f:
    data = json.load(f)

records = data["skg"]["bib"]
TRAGET_DIR = "xml_output"
os.makedirs(TRAGET_DIR, exist_ok=True)

#for i, (key, record) in enumerate(records.items()):
#    if i >= 100:
#        break
for key, record in records.items():
    record_id_raw = record.get("@id", key)

    # Für Dateiname: reservierte Zeichen escapen
    record_id_file = escape_identifier(record_id_raw)

    # Für Root-Element: ID als Tagname verwenden, aber XML-konform bereinigen
    root_tag = clean_tag(record_id_raw)

    root = ET.Element(root_tag)
    build_xml(root, record)

    xml_bytes = prettify(root)

    output_file = os.path.join(TRAGET_DIR, f"{record_id_file}.xml")
    with open(output_file, "wb") as f:
        f.write(xml_bytes)

    print(f"Created: {output_file}")
