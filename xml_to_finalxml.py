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


def convert_all(target):
    xslt_file = CONFIG[target]["xslt"]
    target_dir = CONFIG[target]["target_dir"]

    os.makedirs(target_dir, exist_ok=True)

    xslt_doc = etree.parse(xslt_file)
    transform = etree.XSLT(xslt_doc)

    converted = 0
    skipped = 0
    errors = 0

    for filename in os.listdir(SOURCE_DIR):
        if not filename.lower().endswith(".xml"):
            continue

        source_path = os.path.join(SOURCE_DIR, filename)
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
            print(f"Converted: {source_path} -> {target_path}")

        except Exception as e:
            errors += 1
            print(f"Error in {source_path}: {e}")

    print("")
    print(f"Target: {target}")
    print(f"Converted: {converted}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        choices=["datacite", "openaire"],
        required=True,
        help="Target format: datacite or openaire"
    )

    args = parser.parse_args()
    convert_all(args.target)


if __name__ == "__main__":
    main()
