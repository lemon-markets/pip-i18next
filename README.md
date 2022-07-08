# i18next

[![License](https://img.shields.io/github/license/lemon-markets/pip-i18n-turbo
)](./LICENSE)
[![Tests](https://img.shields.io/github/workflow/status/lemon-markets/pip-i18n-turbo/tests/main?label=tests)](https://github.com/lemon-markets/sdk-python/actions)
[![Python versions](https://img.shields.io/pypi/pyversions/pip-i18n-turbo.svg)](https://pypi.python.org/pypi/i18next/)
[![PyPI](https://img.shields.io/pypi/v/i18next)](https://pypi.python.org/pypi/i18-next/)

**i18next** is a library facilitating internationalization and localization (i18n) of your Python applications

## Installation

You can install library using [pip](http://pypi.python.org/pypi/pip):

```bash
pip install i18next
```

## Glossary

The table below describes the terms used in this documentation.

| Term                | Description                                                         |
|---------------------|---------------------------------------------------------------------|
| translation key     | unique key identifying translation string                           |
| translation string  | string to be translated                                             |
| translation context | data used to interpolate translation string                         |
| translation file    | file containing mapping of translation keys and translation strings |
| translation         | interpolated translation string                                     |

## Locale files

`i18next` assumes the existence of the locale directory containing translation files. The locale directory path can be
configured (see section [Configuration](#configuration)).

Translation files are JSON files containing mapping between translation keys and translation strings.
The translation file should be named as `<language>.json` where` <language> `is a language code.

An example of translation file content is presented below:

```json
{
  "translation-key-1": "This is a text without interpolation",
  "translation-key-2": "This is a text with interpolation: { interpolated-value }"
}
```

An example directory structure of your locale directory should be similar to:

```
locale/
  en.json
  fr.json
  es.json
  pt.json
  ...
```

## Configuration

`i18next` configuration is being done by modifying global `config` object from `i18next` package.
It should be done before first usage of `trans` function:

```python
from i18next import config

config.fallback_lang = 'en'
config.locale_path = '/path/to/your/locale/directory'
config.strict = False
```

The table below describes the configuration parameters:

| Parameter     | Description                                                                                                                                                                                          | Default value |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| fallback_lang | Fallback language to search for translation key if one cannot be found for requested language                                                                                                        | en            |
| locale_path   | Locale directory path                                                                                                                                                                                | ./locale      |
| strict        | Flag determining the behavior of `trans` function. If set to False - `key` itself will be returned in case one has not been found or interpolation has failed , otherwise - exception will be raised | False         |

## Usage

`trans` function is used to get translation based on translation key and requested language.

### Non-strict mode

```python
from i18next import trans, config

# './locale/en.json':
# {
#    "key-1": "Welcome {firstname} {lastname}!",
#    "key-2": "Good morning!",
#    "key-3": "Bye!"
# }
# './locale/pl.json':
# {
#    "key-1": "Witaj {firstname} {lastname}!",
#    "key-2": "Dzień dobry!"
# }

config.fallback_lang = 'en'
config.strict = False

en_trans1 = trans('key-1', params={'firstname': 'John', 'lastname': 'Doe'}) # 'Welcome John Doe!'
en_trans2 = trans('key-2') # 'Good morning!'
en_trans3 = trans('key-3') # 'Bye!'

pl_trans1 = trans('key-1', params={'firstname': 'John', 'lastname': 'Doe'}, lang='pl') # 'Witaj John Doe!'
pl_trans2 = trans('key-2', lang='pl') # 'Dzień dobry!'
pl_trans3 = trans('key-3', lang='pl') # 'Bye!' - fallback case because of missing 'key-3' in pl translation

# config.strict=False so key itself is returned when translation key or file is missing
missing_en_trans = trans('missing-key1') # 'missing-key1'
missing_pl_trans = trans('missing-key2', lang='pl') # 'missing-key2'
missing_fr_trans = trans('missing-key3', lang='fr') # 'missing-key3' because translation file is missing
```

### Strict mode

`trans` function is raising exceptions in strict mode (`config.strict=True`) when:

- translation file is missing
- translation key does not exist
- interpolation fails

```python
from i18next import trans, config, errors

# './locale/en.json':
# {
#    "key-1": "Welcome {firstname} {lastname}!",
#    "key-2": "Good morning!"
# }

config.strict = True

en_trans1 = trans('key-1', params={'firstname': 'John', 'lastname': 'Doe'}) # 'Welcome John Doe!'
en_trans2 = trans('key-2')                                                  # 'Good morning!'


# interpolation error
try:
    trans('key-1', params={'firstname': 'John'}) # missing lastname
except errors.TranslationFormatError:
    ...

# missing translation key
try:
    trans('missing-key')
except errors.TranslationNotFoundError:
    ...

# missing translation file
try:
    trans('key-2', lang='pl')
except errors.TranslationFileNotFoundError:
    ...
```

### Error handling

Exception hierarchy available in strict mode is presented below:

- `I18nError` - base class for all exceptions thrown within `i18next` library
  - `TranslationFileNotFoundError` - missing translation file error
  - `TranslationNotFoundError` - missing translation key error
  - `TranslationFormatError` - interpolation error

## Extracting translation keys from source code
