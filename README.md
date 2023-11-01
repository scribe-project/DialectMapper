# Dialect mapper

Dialectal information given about speakers can vary between corpora. Some corpora may record the municipality of birth, or the county, or others may record the speakers' self-assessed dialect. We'd like a way of standardizing, or creating a meta-corpora mapping, between dialects and counties and municipalities. 

This package is bascially a wrapper around a file mapping between counties, municipalities, and dialects

## County/municipality to dialect mapping development

The alignment between kommune (municipalities), fylke (counties), and dialects was developed through manual effort. It began by looking over dialect maps (such as can be found in Skjekkeland's _Dei norske dialektane_ (page 276)) and attempting to align the currently existing kommune and fylke to them. Once I was satisified with the mapping I extended it to historical kommuner and fylker. To do this I referenced Wikipeida pages for the historial fylke and which kommune they contained and updated the list. The new 2024 updates were created via programtically parsing information in the table on the Regjering website [Nye kommune og fylkesnummer](https://www.regjeringen.no/no/tema/kommuner-og-regioner/kommunestruktur/nye-kommune-og-fylkesnummer-fra-1.-januar-2024/id2924701/). 

The named dialects used are from Skjekkeland's book (with the 4 Eastern regions collapsed into one). Additionally, the names were translated from Nynorsk to Bokmål. The numbered dialects are from a survey produced by SpeechData and used in the NST (? I only have the vaguest memory of this and I not can't find sources to back me up). 

The first column in the CSV file contains the historic kommuner and the second columns the moder kommuner. Where possible this creates a mapping between historic and current kommuner. That is, the kommune in column one became the kommune in column two. Occasionall column one is left empty. This is for instances where a new kommune, one that has not historical equivalent, was included. The same aligment through time can be found for the three fylke columns as well. 


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

## Fine-grainedness of dialects

While we have provided a relatively fine-grained mapping we may not always want/need such detail. Therefore there are two methods of collapsing regions into larger ones

1) The first method is to call the `enable_fine_grained_dialect_collapse`. This will collapse the different Mid dialects into just Trøndsk as well as transform Midlandsk into Østlandsk during the mapping process.

2) The second method is to use the `get_cardinal_dialect`. This is meant for use either post- or ad-hoc. That is, you should use the named mapping function(s) normally then pass the resulting names through this function. Additionally, this method can call the `get_named_dialect` method on its own so it is possible to pass a kommune or fylke name and get a cardinal dialect back.