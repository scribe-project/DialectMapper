# Dialect mapper

Dialectal information given about speakers can vary between corpora. Some corpora may record the municipality of birth, or the county, or others may record the speakers' self-assessed dialect. We'd like a way of standardizing, or creating a meta-corpora mapping, between dialects and counties and municipalities. 

This package is bascially a wrapper around a file mapping between counties, municipalities, and dialects

## Pip installation

This package can be pip installed and thus imported into code regarless of it's relationship to this directory. 

To pip install 

1. Nativate to this `dialect_mapper` directory
2. Run `pip install .` 

## Code usage

The mapper can be inported into other Python code and used like so

```python
import dialect_mapper

# you need to instaniate the class so it reads the CSV file
mm = dialect_mapper.mapper_methods()

mm.get_named_dialect('Arendal')
```

The `get_named_dialect()` and `get_numeric_dialect()` methods try to match the input against old municipalities, new municipalities, old counties, and new counties. If you know specifcially what input you're using, you can use a more explicit method such as `get_named_dialect_by_old_municipality()`

## Special mappings

As is inevitable when humans are inputting data, there are some typos or other inconsistencies in the location data for certain speakers in various corpora. I've done my best to manually correct these and make them available in this package. The two corpora that I've currently accounts for are NB Tale and NPSC. To enable the corrections simply call the enable method on the `mapper_methods` object before querrying for the named or numeric dialect. 

**NB Tale**
```python
import dialect_mapper

mm = dialect_mapper.mapper_methods()
mm.enable_nbtale_corrections()
named_dialect = mm.get_named_dialect('Hyllestand')
```

**NPSC**

```python
import dialect_mapper

mm = dialect_mapper.mapper_methods()
mm.enable_npsc_corrections()
named_dialect = mm.get_named_dialect('Vestfossen')
```