# GESIS Metadata Transformation Pipeline for OpenAIRE

This repository contains a metadata transformation pipeline for
converting metadata exported from the **GESIS Knowledge Graph** into XML
records mapped to the **OpenAIRE metadata structure**.

> **Status:** The generated records are intended for OpenAIRE exposure
> and validation. Until validation of the current mapping is completed
> successfully, the output should be described as *OpenAIRE-formatted*
> rather than fully *OpenAIRE-compliant*.

## Workflow

``` text
GESIS Knowledge Graph JSON
        |
        | json_to_xml_1to1.py
        v
Intermediate XML (one XML file per record)
        |
        | transform_to_openaire.xsl
        | applied by xml_to_finalxml.py
        v
OpenAIRE-formatted XML
        |
        v
OAI-PMH exposure / OpenAIRE validation
```

The transformation is divided into two stages: the first preserves the
source metadata structure in XML; the second performs the OpenAIRE
mapping.

## 1. Input data

The input file is `bib_GWS_enriched.json`. It contains GESIS Knowledge
Graph records with metadata such as identifiers, titles, authors,
contributors, publishers, publication dates, document types, languages,
topics, related resources (`hasLink`), and metadata licence information.

The conversion script currently expects the records at:

``` python
data["skg"]["bib"]
```

## 2. JSON to intermediate XML

`json_to_xml_1to1.py` reads `bib_GWS_enriched.json` and creates one XML
file for every record in `xml_output/`.

This is primarily a **structural conversion**, not yet the OpenAIRE
semantic mapping. JSON objects become XML elements, arrays are
represented by repeated `<item>` elements, null values produce empty
elements, and keys such as `@id` and `@type` become `id` and `type`.
Invalid XML tag characters are cleaned. The record `@id` is used for the
root element and output filename.

Run:

``` bash
python json_to_xml_1to1.py
```

## 3. Mapping to OpenAIRE

`transform_to_openaire.xsl` transforms each intermediate record into an
OpenAIRE-formatted `<resource>` document. The output uses OpenAIRE,
DataCite, Dublin Core, DCMI Terms, RDF and XML Schema Instance
namespaces.

The current XSLT references:

``` text
https://www.openaire.eu/schema/repo-lit/4.0/openaire.xsd
```

### Main mappings

  GESIS source            OpenAIRE output
  ----------------------- ----------------------------------------------------
  `identifier`            `datacite:identifier`
  `authors/*/name`        `datacite:creators/datacite:creator`
  `title`                 `datacite:titles/datacite:title`
  `publisher/*/name`      `dc:publisher`
  `date_pub`              `datacite:dates/datacite:date[@dateType='Issued']`
  `topics/*/name`         `datacite:subjects/datacite:subject`
  `contributors/*/name`   `datacite:contributors`
  `language/item`         `dc:language`
  `doctype/en`            `resourceType`
  `metadataLicense`       `licenseCondition`
  metadata access         `datacite:rights`
  `src_journal/*/name`    `dc:source`
  `hasLink`               `datacite:relatedIdentifiers`

### Main identifier

Research-data identifiers beginning with `ZA` are converted to:

``` text
https://search.gesis.org/research_data/{identifier}
```

Other identifiers are represented as publication URLs:

``` text
https://search.gesis.org/publication/{identifier}
```

## 4. Related resources

Relations under `hasLink` are mapped to `datacite:relatedIdentifier`.
The current XSLT handles DOI identifiers, GESIS research-data targets
beginning with `ZA`, and GESIS publication targets beginning with
`gesis-bib-`.

For example:

``` text
ZA5231
→ https://search.gesis.org/research_data/ZA5231

gesis-bib-151981
→ https://search.gesis.org/publication/gesis-bib-151981
```

The relation type is derived from the link information, with fallback
handling in the XSLT.

## 5. Batch transformation

`xml_to_finalxml.py` applies the selected XSLT to all XML files in
`xml_output/`.

For OpenAIRE:

``` bash
python xml_to_finalxml.py --target openaire
```

The transformed records are written to `final_xml_openaire/`.

The same framework also supports a DataCite target:

``` bash
python xml_to_finalxml.py --target datacite
```

provided that `transform_to_datacite.xsl` is available.

The script reports converted, skipped and erroneous records.

## 6. Complete execution

``` bash
python json_to_xml_1to1.py
python xml_to_finalxml.py --target openaire
```

Expected structure:

``` text
.
├── bib_GWS_enriched.json
├── json_to_xml_1to1.py
├── transform_to_openaire.xsl
├── xml_to_finalxml.py
├── xml_output/
└── final_xml_openaire/
```

## 7. Why use intermediate XML?

The intermediate layer separates:

1.  **Serialization:** convert the JSON metadata to XML while preserving
    the source structure as closely as possible.
2.  **Semantic mapping:** use XSLT to map selected GESIS metadata fields
    to the OpenAIRE structure.

This separation makes the mapping easier to inspect, test and modify
without changing the JSON-to-XML conversion.

## 8. OAI-PMH and validation

The generated records are intended for exposure through the GESIS
OAI-PMH infrastructure and validation against OpenAIRE requirements.

During development, different versions of the OpenAIRE mapping were
tested. The XSLT was adapted using an OpenAIRE sample XML as a concrete
reference for elements, namespaces and XML structure.

The overall workflow is therefore:

``` text
Source metadata
→ JSON-to-XML conversion
→ OpenAIRE mapping
→ OAI-PMH exposure
→ OpenAIRE validation
```

## Files

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `bib_GWS_enriched.json`             Source metadata from the GESIS
                                      Knowledge Graph

  `json_to_xml_1to1.py`               Converts JSON records to
                                      intermediate XML

  `transform_to_openaire.xsl`         Maps intermediate GESIS XML to the
                                      OpenAIRE XML structure

  `xml_to_finalxml.py`                Applies the selected XSLT to all
                                      intermediate XML records
  -----------------------------------------------------------------------
