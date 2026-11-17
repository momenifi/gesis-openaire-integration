
import os
import argparse
from lxml import etree


SOURCE_DIR = "xml_output"

CONFIG = {
    "datacite": {
        "xslt": "transform_to_datacite.xsl",
        "target_dir": "final_xml_datacite"
    },
    "openaire": {
        "xslt": "transform_to_openaire.xsl",
        "target_dir": "final_xml_openaire"
    }
}


def convert_collection(target, collection, transform):
    source_dir = os.path.join(SOURCE_DIR, collection)
    target_dir = os.path.join(
        CONFIG[target]["target_dir"], collection
    )

    os.makedirs(target_dir, exist_ok=True)

    converted = 0
    skipped = 0
    errors = 0

    for filename in sorted(os.listdir(source_dir)):
        if not filename.lower().endswith(".xml"):
            continue

        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)

        try:
            xml_doc = etree.parse(source_path)
            result = transform(xml_doc)

            output_bytes = etree.tostring(
                result,
                pretty_print=True,
                xml_declaration=True,
                encoding="UTF-8"
            )

            if output_bytes is None:
                skipped += 1
                print(f"Skipped: {source_path}")
                continue

            with open(target_path, "wb") as f:
                f.write(output_bytes)

            converted += 1

        except Exception as e:
            errors += 1
            print(f"Error in {source_path}: {e}")

    print(f"\nCollection: {collection}")
    print(f"Target: {target}")
    print(f"Converted: {converted}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")

    return converted, skipped, errors


def convert_all(target, collection):
    xslt_file = CONFIG[target]["xslt"]

    xslt_doc = etree.parse(xslt_file)
    transform = etree.XSLT(xslt_doc)

    if collection == "all":
        collections = sorted(
            name for name in os.listdir(SOURCE_DIR)
            if os.path.isdir(os.path.join(SOURCE_DIR, name))
        )
    else:
        collections = [collection]

    total_converted = 0
    total_skipped = 0
    total_errors = 0

    for current_collection in collections:
        source_dir = os.path.join(
            SOURCE_DIR, current_collection
        )

        if not os.path.isdir(source_dir):
            print(f"Collection not found: {current_collection}")
            continue

        converted, skipped, errors = convert_collection(
            target, current_collection, transform
        )

        total_converted += converted
        total_skipped += skipped
        total_errors += errors

    print("\n=== TOTAL SUMMARY ===")
    print(f"Target: {target}")
    print(f"Converted: {total_converted}")
    print(f"Skipped: {total_skipped}")
    print(f"Errors: {total_errors}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--target",
        choices=["datacite", "openaire"],
        required=True,
        help="Target format: datacite or openaire"
    )

    parser.add_argument(
        "--collection",
        default="all",
        help="Collection name (bib, study, etc.) or all"
    )

    args = parser.parse_args()
    convert_all(args.target, args.collection)


if __name__ == "__main__":
    main()