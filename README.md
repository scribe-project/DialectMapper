# Dialect mapper

Dialect mapper standardizes Norwegian location and dialect metadata across speech corpora. It maps historical and newer municipalities (*kommuner*) and counties (*fylker*) to named, numeric, and cardinal dialect regions, supports reverse lookups and corpus-specific corrections, and draws shaded maps of Norway.

The mapping CSV has been officially published through the National Library of Norway’s Language Bank: [resource catalogue entry](https://www.nb.no/sprakbanken/en/resource-catalogue/oai-nb-no-sbr-92/).

If you find this code or the dialect mappings useful, please cite:

Phoebe Parsons, Per Erik Solberg, Knut Kvale, Torbjørn Svendsen, and Giampiero Salvi. 2025. [Adding Metadata to Existing Parliamentary Speech Corpus](https://aclanthology.org/2025.nodalida-1.49/). _In Proceedings of the Joint 25th Nordic Conference on Computational Linguistics and 11th Baltic Conference on Human Language Technologies (NoDaLiDa/Baltic-HLT 2025)_, pages 448–457, Tallinn, Estonia. University of Tartu Library.

## General information and mapping development

Corpora may record a speaker’s municipality of birth, county, or self-assessed dialect. This package wraps a mapping table to help align those different forms of metadata across corpora.

The alignment between municipalities, counties, and dialects was developed manually by Phoebe Parsons, with feedback from Per Erik Solberg. It began by consulting dialect maps, including Skjekkeland’s _Dei norske dialektane_ (page 276), and aligning the municipalities and counties in use at the time with dialect regions. The mapping was then extended to historical municipalities and counties using Wikipedia pages describing historical counties and their constituent municipalities. The 2024 county updates were created by programmatically parsing the table on the government’s [Nye kommune og fylkesnummer](https://www.regjeringen.no/no/tema/kommuner-og-regioner/kommunestruktur/nye-kommune-og-fylkesnummer-fra-1.-januar-2024/id2924701/) page.

The named dialects follow Skjekkeland’s book, with its four Eastern regions collapsed into one and names translated from Nynorsk to Bokmål. The original author recalled that the numbered dialects came from a Speech-Dat survey used in NST, but could not verify that provenance; it remains unconfirmed.

The first CSV column contains historical municipalities and the second contains newer municipalities. Where possible, each row links an old municipality to the municipality it became. An empty historical municipality denotes a newer municipality without a historical equivalent in the table. The county columns likewise align names over time.

The mapper currently loads `dialect_mapper/mapping_data/muni_county_namedDialect_numericDialect_mapping_manual_additions_renamed_2024_cardinals.csv`, whose columns are:

| Column | Meaning |
| --- | --- |
| `old_muni` | Historical municipality |
| `new_muni` | Newer municipality |
| `old_county` | Historical county |
| `new_county` | County in the intermediate, pre-2024 mapping |
| `new_county_2024` | County in the 2024 mapping |
| `named_dialect` | Fine-grained dialect name |
| `numeric_dialect` | Numeric dialect code, read as a string |
| `cardinal_five` | Five-region cardinal classification |
| `cardinal_four` | Four-region cardinal classification |

These are the table’s historical snapshots; “new” does not mean a live administrative register. A municipality or county can span multiple dialect regions.

## Installation

From the repository root (the directory containing `pyproject.toml`), install the package so it can be imported from other projects:

```bash
python -m pip install .
```

For an editable development installation, use `python -m pip install -e .`.

`pyproject.toml` now declares Python `^3.8` (`>=3.8,<4.0`) and the following dependencies. Pip resolves their additional Python and platform requirements during installation.

| Dependency | Version specification |
| --- | --- |
| Matplotlib | `3.6.1` |
| Shapely | `^2.1.2` (`>=2.1.2,<3.0`) |
| NumPy | `^1.20.0` (`>=1.20.0,<2.0`) |
| CairoSVG | `2.6.0` |

The Shapely dependency is now a valid TOML entry and supports the plotter’s top-level `Polygon` and `MultiPolygon` imports.

The package imports its plotting module at import time, so Matplotlib, Shapely, NumPy, and CairoSVG are needed even when using only the mapper. PNG/PDF conversion also needs CairoSVG’s system dependencies, including Cairo.

## Basic usage

```python
import dialect_mapper

# Instantiate once to load the bundled mapping CSV.
mm = dialect_mapper.mapper_methods()

mm.get_named_dialect('Arendal')       # 'Sørlandsk'
mm.get_numeric_dialect('Arendal')     # '20'
mm.get_cardinal_five('Arendal')       # 'south'
mm.get_cardinal_four('Arendal')       # 'east'
```

The four general lookup methods accept municipality or county names, ignoring case and surrounding whitespace. They try historical municipalities, newer municipalities, historical counties, intermediate counties, and finally 2024 counties, stopping at the first successful category.

They return a string for one matching dialect, a list for multiple matching dialects, and `None` with a printed error when no match is found. Numeric codes are strings, not integers. For example, `mm.get_named_dialect('Agder')` returns `['Sørlandsk', 'Sørvestlandsk']`.

### Explicit lookups and ambiguous municipalities

Each of `get_named_dialect`, `get_numeric_dialect`, `get_cardinal_four`, and `get_cardinal_five` also has these explicit variants:

| Suffix | Example |
| --- | --- |
| `_by_old_municipality` | `mm.get_named_dialect_by_old_municipality('Kristiansand')` |
| `_by_new_municipality` | `mm.get_named_dialect_by_new_municipality('Kristiansand')` |
| `_by_old_county` | `mm.get_named_dialect_by_old_county('Aust-Agder')` |
| `_by_new_county` | `mm.get_named_dialect_by_new_county('Agder')` |
| `_by_new_county_2024` | `mm.get_named_dialect_by_new_county_2024('Telemark')` |

Explicit lookups return sorted, unique lists, including `[]` for no match. They do not apply the optional fine-grained dialect collapse.

When a municipality name occurs in both historical and newer columns with different named-dialect results, general lookups default to the newer municipality. Choose the historical interpretation with `resolve_ambiguous='old'`:

```python
mm.get_named_dialect('Os', resolve_ambiguous='old')
mm.get_named_dialect('Os', resolve_ambiguous='new')
mm.is_ambiguious_municipality('Os')
```

The same keyword works with numeric and cardinal lookups. For a known administrative snapshot, use an explicit lookup to avoid category fallback.

### Reverse lookups and numeric conversion

Find the municipalities or counties associated with a named dialect:

```python
mm.get_old_municipalities_from_named_dialect('Sørlandsk')
mm.get_new_municipalities_from_named_dialect('Sørlandsk')
mm.get_old_counties_from_named_dialect('Sørlandsk')
mm.get_new_counties_from_named_dialect('Sørlandsk')
mm.get_new_counties_2024_from_named_dialect('Sørlandsk')
```

Numeric reverse lookups accept an integer or numeric string:

```python
mm.get_old_municipalities_from_numeric_dialect(17)
mm.get_new_municipalities_from_numeric_dialect('17')
mm.get_old_counties_from_numeric_dialect(17)
mm.get_new_counties_from_numeric_dialect('17')
```

These methods return sorted, unique lists. Historical municipality results may include `''` where a row has no historical equivalent. There is no numeric reverse lookup for 2024 counties.

`mm.get_cardinal_four_from_numeric('17')` converts a numeric dialect code to a list of four-region labels. Pass the code as a string: this method compares directly with the CSV strings. There is no corresponding five-region conversion method.

### Less fine-grained dialects and cardinal regions

The fine-grained named regions are `Helgelandsk`, `Midlandsk`, `Namdalsk`, `Nordlandsk`, `Nordvestlandsk`, `Sørlandsk`, `Sørvestlandsk`, `Troms-Finnmarks-mål`, `Uttrøndersk`, `Østlandsk`, and `Østtrøndsk`.

To collapse `Namdalsk`, `Østtrøndsk`, and `Uttrøndersk` into `Trøndsk`, and `Midlandsk` into `Østlandsk`, enable collapse before calling the general lookup methods:

```python
mm.enable_fine_grained_dialect_collapse()
mm.get_named_dialect('Trondheim')  # 'Trøndsk'
mm.disable_fine_grained_dialect_collapse()
```

Collapse is applied by the general response formatter, not by explicit or reverse lookups. It does not deduplicate labels after collapsing, so a list can contain repeated `Trøndsk` entries.

For broader geographic groupings, `get_cardinal_five()` returns `north`, `mid`, `west`, `east`, or `south`. `get_cardinal_four()` returns `north`, `mid`, `west`, or `east`, using the separate four-region classification in the CSV. For example, Arendal maps to `south` in the five-region scheme and `east` in the four-region scheme.

The legacy `get_cardinal_dialect()` still converts a single named dialect, such as `mm.get_cardinal_dialect('Sørlandsk')`, to a five-region label (`'south'`). **Location input to this method is deprecated and now raises an exception.** Use `get_cardinal_four()` or `get_cardinal_five()` for municipality/county input. Older documentation described an automatic location lookup in the legacy method; that behavior is no longer supported.

## Corpus-specific mappings

Corpus metadata can contain typos, town names in place of municipalities, and foreign locations. Optional correction tables normalize these inputs before municipality lookups for named, numeric, and cardinal dialects. Enable the appropriate table before querying. Corrections are disabled by default and do not alter the underlying mapping CSV or apply to explicit county lookups.

| Corpus | Enable method | Example input |
| --- | --- | --- |
| NB Tale | `mm.enable_nbtale_corrections()` | `Hyllestand` |
| NPSC | `mm.enable_npsc_corrections()` | `Vestfossen` |
| Stortinget (SSC) | `mm.enable_stortinget_corrections()` | `opdal` |
| Nordic Dialect Corpus (NDC) | `mm.enable_ndc_corrections()` | `Kirkenær` |

```python
import dialect_mapper

mm = dialect_mapper.mapper_methods()
mm.enable_nbtale_corrections()
named_dialect = mm.get_named_dialect('Hyllestand')  # 'Nordvestlandsk'
```

Use the other enable methods with their corresponding example inputs in the same way. Multiple correction tables can be enabled on one instance; they are applied in the order NB Tale, NPSC, Stortinget, then NDC, regardless of the order of the enable calls.

NB Tale corrections ignore `Herøy` by default because two municipalities share that name and the speaker’s location cannot be reliably disambiguated. Use `mm.enable_nbtale_corrections(ignore_herøy=False)` to retain the table’s normal lookup behavior for that name. Some foreign locations are corrected to an empty value and produce no match.

### NB Tale speaker IDs

Two speaker-ID lookup methods provide manually curated named dialects and five-region cardinal labels for NB Tale speakers across modules 1–3:

```python
mm = dialect_mapper.mapper_methods()
mm.get_nbtale_named_dialect_from_id('p1_g02_f2_4')    # 'Troms-Finnmarks-mål'
mm.get_nbtale_named_dialect_from_id('p2_g14_m0_5_t')  # 'Utenlandsk'
mm.get_nbtale_named_dialect_from_id('p2_g24_n0_5_t')  # 'Nordvestlandsk'

mm.get_nbtale_cardinal_five_from_id('p1_g02_f2_4')    # 'north'
mm.get_nbtale_cardinal_five_from_id('p2_g14_m0_5_t')  # 'non-native'
mm.get_nbtale_cardinal_five_from_id('p2_g24_n0_5_t')  # 'west'
```

Most assignments were made using the municipality mapper. Phoebe also manually added dialects where the municipality was missing but other metadata allowed an estimate. Both methods lazily load the bundled updated informant CSVs and share a cache of named dialects. Neither requires enabling NB Tale corrections. IDs are matched exactly, and both methods return `''` for an unknown speaker ID.

`get_nbtale_named_dialect_from_id()` returns the stored named dialect, which can include `Utenlandsk` in addition to geographic dialect names. `get_nbtale_cardinal_five_from_id()` converts that stored name to `north`, `mid`, `west`, `east`, or `south` using `get_cardinal_dialect()`, and returns `non-native` for `Utenlandsk`. These speaker-ID lookups do not use the municipality lookup’s ambiguity resolution or optional fine-grained collapse.

## Plotting maps

`plotter_methods` draws maps using bundled GeoJSON boundaries and a Mercator projection. The original municipal GeoJSON data came from [robhop/fylker-og-kommuner-2020](https://github.com/robhop/fylker-og-kommuner-2020); these boundaries are separate resources from the mapper’s 2024 county table.

```python
import dialect_mapper

plotter = dialect_mapper.plotter_methods()
plotter.plot_card5_dialect_regions(
    'dialect_counts.svg',
    dia_region_to_value={'north': 10, 'mid': 20, 'west': 15, 'east': 30, 'south': 5},
    color_map_name='Blues',
    max_region_value=30,
    final_width=600,
    final_height=600,
)
```

Available map methods and their value-dictionary arguments are:

| Method | Dictionary argument | Keys |
| --- | --- | --- |
| `plot_kommune_regions` | `kommune_region_to_value` | Municipality names in the bundled geometry |
| `plot_dialect_regions` | `dialect_region_to_value` | Fine-grained dialect names in the bundled geometry |
| `plot_card4_dialect_regions` | `dia_region_to_value` | `north`, `mid`, `west`, `east` |
| `plot_card5_dialect_regions` | `dia_region_to_value` | `north`, `mid`, `west`, `east`, `south` |
| `plot_rundkast_regions` | `rundkast_region_to_value` | `north`, `mid`, `west`, `east`, `south` |

All methods take the output path as their first argument (named `output_svg_filepath` even for PNG/PDF output). Use a string ending in `.svg`, `.png`, or `.pdf`; PNG and PDF outputs are converted through CairoSVG using an intermediate SVG, which is then removed. Use a distinct output basename if an SVG with that name already exists.

All methods accept `color_map_name='Blues'`, `color_map_levels=50`, `max_region_value=30`, `default_color='#66cc99'`, `final_width='500'`, and `final_height='500'`. Numeric values are shaded on a linear scale from zero to `max_region_value`, with values outside that range clamped to the endpoints. Omitted regions use `default_color`; cardinal-four and cardinal-five maps also accept `None` for a region value to render it white.

Plot dictionary keys are case-sensitive. To inspect the exact names in a map, read its GeoJSON `properties['navn']` values, for example:

```python
[f['properties']['navn'] for f in plotter.dialekter_json['features']]
```

The corresponding geometry attributes are `kommuner_json`, `dialekter_json`, `card4_dialekter_json`, `card5_dialekter_json`, and `region_json`. Municipality plotting distinguishes the two Herøy regions with the keys `Herøy_Helgelandsk` and `Herøy_Nordvestlandsk`.

`plot_rundkast_regions()` additionally accepts `split_norway=False`, `rotate_norway=False`, and `stroke_width=0.025`. These options reposition northern regions, rotate the map, and adjust boundary line width, respectively.

## Existing tests

With the dependencies installed, run the bundled tests from the repository root:

```bash
python -m unittest discover -s dialect_mapper/tests
```

The tests rely on specific bundled CSV contents. Two legacy tests still expect `get_cardinal_dialect()` to accept location names; those expectations no longer match the implementation described above.
