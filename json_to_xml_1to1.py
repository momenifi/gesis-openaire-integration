import json
import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from urllib.parse import quote
import argparse
import shutil


def prettify(elem):
    rough_string = ET.tostring(elem, encoding="utf-8")

    try:
        reparsed = minidom.parseString(rough_string)
    except Exception as e:
        if hasattr(e, "offset"):
            pos = e.offset
            print("\nProblematic XML content:")
            print(repr(rough_string[max(0, pos - 100):pos + 100]))
        raise

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

def clean_xml_text(value):
    return "".join(
        char for char in str(value)
        if (
            char in "\t\n\r"
            or "\u0020" <= char <= "\uD7FF"
            or "\uE000" <= char <= "\uFFFD"
            or "\U00010000" <= char <= "\U0010FFFF"
        )
    )

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
            parent.text = clean_xml_text(data)



INPUT_DIR = "json_input"
OUTPUT_DIR = "xml_output"

COLLECTION_KEYS = {
    "bib": "bib",
    "bibsonomy": "bibsonomy",
    "gris": "gris",
    "other_study": "other_study",
    "ssoar": "ssoar",
    "study": "dbk_study",
}


def convert_collection(collection):
    source_dir = os.path.join(INPUT_DIR, collection)
    target_dir = os.path.join(OUTPUT_DIR, collection)
    

    json_files = [
        filename for filename in os.listdir(source_dir)
        if filename.lower().endswith(".json")
    ]

    if not json_files:
        print(f"No JSON files found in {source_dir}")
        return

    # Recreate the output folder for this collection
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    os.makedirs(target_dir, exist_ok=True)

    total = 0

    for filename in sorted(json_files):
        input_file = os.path.join(source_dir, filename)

        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        json_key = COLLECTION_KEYS.get(collection, collection)
        records = data["skg"][json_key]

        for key, record in records.items():
            record_id_raw = record.get("@id", key)
            record_id_file = escape_identifier(record_id_raw)
            root_tag = clean_tag(record_id_raw)

            root = ET.Element(root_tag)
            build_xml(root, record)

            try:
                xml_bytes = prettify(root)
            except Exception as e:
                print(f"\nERROR in collection: {collection}")
                print(f"JSON file: {filename}")
                print(f"Record ID: {record_id_raw}")
                print(f"Error: {e}")
                raise

            output_file = os.path.join(
                target_dir, f"{record_id_file}.xml"
            )

            with open(output_file, "wb") as f:
                f.write(xml_bytes)

            total += 1

    print(f"{collection}: {total} XML files created in {target_dir}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--collection",
        default="all",
        help="Collection name (bib, study, etc.) or all"
    )

    args = parser.parse_args()

    if args.collection == "all":
        collections = sorted(
            name for name in os.listdir(INPUT_DIR)
            if os.path.isdir(os.path.join(INPUT_DIR, name))
        )
    else:
        collections = [args.collection]

    for collection in collections:
        source_dir = os.path.join(INPUT_DIR, collection)

        if not os.path.isdir(source_dir):
            print(f"Collection not found: {collection}")
            continue

        convert_collection(collection)


if __name__ == "__main__":
    main()
