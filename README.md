# Dialect mapper

Dialectal information given about speakers can vary between corpora. Some corpora may record the municipality of birth, or the county, or others may record the speakers self-assed dialect. We'd like a way of standardiing, or creating a meta-corpora mapping, between dialects and counties and municipalities. 

This package is bascially a wrapper around a file mapping between counties, municipalities, and dialects

## Usage

### Pip installation

This package can be pip installed and thus imported into code regarless of it's relationship to this directory. 

To pip install 

1. Nativate to this `dialect_mapper` directory
2. Run `pip install .` 

### Code usage

The mapper can be inported into other Python code and used like so

```python
import dialect_mapper

# you need to instaniate the class so it reads in the CSV file
mm = dialect_mapper.mapper_methods()

mm.get_named_dialect('Arendal')
```

The `get_named_dialect()` and `get_numeric_dialect()` methods try to match the input against old municipalities, new municipalities, old counties, and new counties. If you know specifcially what input you're using, you can use a more explicit method such as `get_named_dialect_by_old_municipality()`

