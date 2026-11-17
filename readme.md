# JSON to XML Transformation Pipeline

This pipeline converts GESIS JSON metadata into XML files and then transforms them into final XML formats for DataCite or OpenAIRE.

## Files

```text
json_to_xml_1to1.py
transform_to_datacite.xsl
transform_to_openaire.xsl
xml_to_finalxml.py
```

---

## Step 1: Convert JSON to 1:1 XML

Run:

```bash
python3 json_to_xml_1to1.py \
    --input /path/to/bib_GWS_enriched.json \
    --output /path/to/xml_output
```

Parameters:

| Parameter | Description |
|------------|-------------|
| `--input` | Input JSON file |
| `--output` | Directory for generated XML files |

Example:

```bash
python3 json_to_xml_1to1.py \
    --input ./bib_GWS_enriched.json \
    --output ./xml_output
```

Output:

```text
xml_output/
```

One XML file is created per record.

---

## Step 2: Transform XML to DataCite

Run:

```bash
python3 xml_to_finalxml.py \
    --target datacite \
    --input /path/to/xml_output
```

Parameters:

| Parameter | Description |
|------------|-------------|
| `--target` | datacite or openaire |
| `--input` | Source directory containing XML files |

Output:

```text
final_xml_datacite/
```

Rules:

- Only records with DOI as main identifier are generated
- Main identifier → DOI
- hasLink identifiers → relatedIdentifiers

---

## Step 3: Transform XML to OpenAIRE

Run:

```bash
python3 xml_to_finalxml.py \
    --target openaire \
    --input /path/to/xml_output
```

Output:

```text
final_xml_openaire/
```

Rules:

- Records can be generated without DOI
- Main identifier becomes GESIS URL
- hasLink identifiers become relatedIdentifiers

---

## Full workflow

```bash
python3 json_to_xml_1to1.py \
    --input ./bib_GWS_enriched.json \
    --output ./xml_output

python3 xml_to_finalxml.py \
    --target datacite \
    --input ./xml_output

python3 xml_to_finalxml.py \
    --target openaire \
    --input ./xml_output
```

---

## Dependencies

Install required package:

```bash
pip install lxml
```

or:

```bash
pip3 install lxml
```