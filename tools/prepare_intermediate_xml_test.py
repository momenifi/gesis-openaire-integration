
from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR =  PROJECT_ROOT /"xml_output"
TARGET_DIR =  PROJECT_ROOT /"xml_output_test" 

COLLECTIONS = [
    "bib",
    "bibsonomy",
    "gris",
    "other_study",
    "ssoar",
    "study",
]

COUNT = 2

total = 0

for collection in COLLECTIONS:
    source = SOURCE_DIR / collection
    target = TARGET_DIR / collection

    if not source.is_dir():
        print(f"Missing directory: {source}")
        continue

    files = sorted(source.glob("*.xml"))[:COUNT]

    target.mkdir(parents=True, exist_ok=True)

    # Remove previous test XML files
    for old_file in target.glob("*.xml"):
        old_file.unlink()

    for file in files:
        shutil.copy2(file, target / file.name)

    print(f"{collection}: {len(files)} XML files copied")
    total += len(files)

print(f"\nTotal: {total} XML files")
print(f"Output directory: {TARGET_DIR}")

