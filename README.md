# GESIS Metadata Transformation Pipeline

This repository contains the production pipeline for converting metadata exported from the **GESIS Knowledge Graph** into intermediate XML and transforming it into **OpenAIRE-formatted** or **DataCite-formatted** XML.

The pipeline separates structural conversion from semantic mapping:

```text
json_input/<collection>/*.json
    |
    | json_to_xml_1to1.py
    v
xml_output/<collection>/*.xml
    |
    | xml_to_finalxml.py + selected XSLT
    +--> final_xml_openaire/<collection>/*.xml
    +--> final_xml_datacite/<collection>/*.xml
```

For the project's methodological background and OpenAIRE integration context, see [README_OpenAIRE_Pipeline.md](README_OpenAIRE_Pipeline.md).

## Supported collections

The pipeline supports six collections:

| Collection directory | Key under `skg` in source JSON |
| --- | --- |
| `bib` | `bib` |
| `bibsonomy` | `bibsonomy` |
| `gris` | `gris` |
| `other_study` | `other_study` |
| `ssoar` | `ssoar` |
| `study` | `dbk_study` |

Place the source JSON files in `json_input/<collection>/`. Input data and generated XML are not intended to be committed to this repository.

## Requirements

- Python 3
- [`lxml`](https://lxml.de/) for XSLT processing

Install the dependency:

```bash
python -m pip install lxml
```

Run all commands from the **repository root**, because the scripts currently use relative paths.

## Step 1 — JSON to intermediate XML

Convert all available collection directories:

```bash
python json_to_xml_1to1.py --collection all
```

Or convert one collection:

```bash
python json_to_xml_1to1.py --collection study
```

The script reads `json_input/<collection>/`, creates one intermediate XML file per record, and writes files to `xml_output/<collection>/`.

The conversion preserves the source structure as closely as possible: JSON objects become XML elements, arrays become `item` elements, and keys such as `@id` and `@type` become `id` and `type`. Invalid XML text characters are removed.

**Important:** For each selected collection, the script **deletes and recreates** the corresponding `xml_output/<collection>/` directory. Do not store manually edited files there.

## Step 2 — Intermediate XML to final XML

### OpenAIRE

Convert all available collections:

```bash
python xml_to_finalxml.py --target openaire --collection all
```

Or one collection:

```bash
python xml_to_finalxml.py --target openaire --collection study
```

This applies `transform_to_openaire.xsl` and writes to `final_xml_openaire/<collection>/`.

### DataCite

```bash
python xml_to_finalxml.py --target datacite --collection all
```

This applies `transform_to_datacite.xsl` and writes to `final_xml_datacite/<collection>/`.

The transformation script reports converted, skipped, and erroneous records for each collection and in total. **It does not automatically clear existing final-output directories**; stale XML files can remain if an input record is removed. Refresh those directories deliberately when a clean rebuild is required.

## Current OpenAIRE mapping

The OpenAIRE XSLT generates a `resource` element using the OpenAIRE 4.0 namespace and schema reference. Selected mappings include:

| Source metadata | OpenAIRE output |
| --- | --- |
| `identifier` | `datacite:identifier` as a GESIS URL |
| `hasIdentifier` DOI entries | `datacite:alternateIdentifiers` |
| `authors/*/name` or `authors/item` | `datacite:creators` |
| `title` | `datacite:titles` |
| `publisher/*/name` | `dc:publisher`, with `GESIS` fallback |
| `date_pub` | `datacite:date` with `dateType="Issued"` |
| `topics/*/name` | `datacite:subjects` |
| `contributors/*/name` | `datacite:contributors` |
| `language/item` | `dc:language` |
| `doctype/en` | `resourceType` (partial COAR mapping) |
| `metadataLicense` | `licenseCondition` |
| `src_journal/*/name` | `dc:source` |
| Supported `hasLink` relations | `datacite:relatedIdentifiers` |

For primary identifiers, values starting with `ZA` are mapped to `https://search.gesis.org/research_data/<identifier>`; other identifiers are mapped to `https://search.gesis.org/publication/<identifier>`. Supported `hasLink` targets include DOI references, `ZA` identifiers, and `gesis-bib-` identifiers.

## Current limitations and validation

**OpenAIRE-formatted does not yet mean OpenAIRE-compliant.** The current transformation still requires validation against the OpenAIRE schema and application-profile requirements before production exposure.

In particular:

- The COAR `resourceType` mapping is incomplete. The current XSLT recognizes `book` and `journal_article`, but defaults other values to `other` with `resourceTypeGeneral="literature"`; this is not appropriate for all research-data records.
- Multilingual titles and source-specific metadata variations require further review.
- The scripts report transformation errors but do not perform a complete OpenAIRE schema-validation step.

The output is intended for subsequent OAI-PMH exposure and validation. The production repository deliberately excludes temporary test scripts, test datasets, and generated XML collections.

## Repository files

| File | Purpose |
| --- | --- |
| `json_to_xml_1to1.py` | Converts source JSON into intermediate XML |
| `xml_to_finalxml.py` | Applies the selected XSLT by collection |
| `transform_to_openaire.xsl` | OpenAIRE metadata mapping |
| `transform_to_datacite.xsl` | DataCite metadata mapping |
| `README.md` | Current production usage and limitations |
| `README_OpenAIRE_Pipeline.md` | Background and methodology for the deliverable |

## Typical full run

```bash
python json_to_xml_1to1.py --collection all
python xml_to_finalxml.py --target openaire --collection all
```

To generate DataCite output as well:

```bash
python xml_to_finalxml.py --target datacite --collection all
```
