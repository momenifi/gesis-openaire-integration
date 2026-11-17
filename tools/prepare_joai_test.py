
from pathlib import Path
import shutil
import argparse
import random

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG = {
    "openaire": PROJECT_ROOT / "final_xml_openaire",
    "datacite": PROJECT_ROOT / "final_xml_datacite",
}

COLLECTIONS = [
    "bib",
    "bibsonomy",
    "gris",
    "other_study",
    "ssoar",
    "study",
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        choices=["openaire", "datacite", "all"],
        default="all"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=20
    )
    args = parser.parse_args()

    if args.count < 1:
        parser.error("--count must be at least 1")

    targets = (
        list(CONFIG) if args.target == "all"
        else [args.target]
    )

    for target in targets:
        source_root = CONFIG[target]
        output_root = PROJECT_ROOT / "joai_test" / target

        for collection in COLLECTIONS:
            source_dir = source_root / collection
            output_dir = output_root / collection

            if not source_dir.is_dir():
                print(f"Missing folder: {source_dir}")
                continue

            files = sorted(source_dir.glob("*.xml"))

            # Reproducible random selection
            rng = random.Random(42)
            selected = rng.sample(
                files, min(args.count, len(files))
            )

            # Refresh only the selected test directory
            if output_dir.exists():
                shutil.rmtree(output_dir)

            output_dir.mkdir(parents=True)

            for file in selected:
                shutil.copy2(
                    file, output_dir / file.name
                )

            print(
                f"{target}/{collection}: "
                f"{len(selected)} files copied"
            )

if __name__ == "__main__":
    main()
