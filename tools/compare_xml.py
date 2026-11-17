
from pathlib import Path
import hashlib

OLD_DIR = Path("#final_xml_openaire/study")
NEW_DIR = Path("final_xml_openaire/study")


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


old_files = {p.name: p for p in OLD_DIR.glob("*.xml")}
new_files = {p.name: p for p in NEW_DIR.glob("*.xml")}

missing = sorted(old_files.keys() - new_files.keys())
extra = sorted(new_files.keys() - old_files.keys())

different = [
    name for name in sorted(old_files.keys() & new_files.keys())
    if checksum(old_files[name]) != checksum(new_files[name])
]

print(f"Old XML files: {len(old_files)}")
print(f"New XML files: {len(new_files)}")
print(f"Missing files: {len(missing)}")
print(f"Extra files: {len(extra)}")
print(f"Different files: {len(different)}")

for name in missing[:10]:
    print("Missing:", name)

for name in extra[:10]:
    print("Extra:", name)

for name in different[:10]:
    print("Different:", name)

if not missing and not extra and not different:
    print("\nSUCCESS: All XML files are identical!")
else:
    print("\nWARNING: Differences found.")
