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
`i18next` assumes the existence of the locale directory containing translation files. The directory path can be configured (see section [Configuration](#configuration)).

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
It should be done <u>before first usage of `trans` function</u>:

```python
from i18next import config

config.fallback_lang = 'en'
config.locale_path = '/path/to/your/locale/directory'
config.strict = False
```
The table below describes the configuration parameters:

| Parameter     | Description                                                                                                                                                                                                      | Default value |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| fallback_lang | Fallback language to search for translation key if one cannot be found for requested language                                                                                                                    | en            |
| locale_path   | Directory path to locale files                                                                                                                                                                                   | ./locale      |
| strict        | Flag determining the behavior of `trans` function. If set to False - `key` itself will be returned in case one has not been found or translation interpolation has failed , otherwise - exception will be raised | False         |

## Usage
### Using `trans` function

`trans` function is executing two steps:
- it searches for translation string based on translation key and requested language
- it populates translation context within translation string to finally return ready translation.

The interface of this function is presented below:

```python
def trans(
    key: str,
    params: Optional[Dict[str, Any]] = None,
    lang: Optional[str] = None
):
    ...
```
Description of the parameters:
- `key` - translation key
- `params` - translation context [optional]
- `lang` - language to search for translation string [optional]

User has to provide at least `key` to get a translation.
`params` are used to populate translation string with translation context to produce ready translation.
`lang` is used to determine language to search for translation string, if not provided the `config.fallback_lang` will be used.

Typical usage of the function is presented below:

```python
from i18next import trans

# The content of the './locale/en.json' is as follows:
# {
#    "some-key": "Welcome, {firstname} {lastname}"
# }
# The content of the './locale/pl.json' is as follows:
# {
#    "some-key": "Witaj, {firstname} {lastname}"
# }
en_translation = trans('some-key', params={'firstname': 'John', 'lastname': 'Doe'})  # 'Welcome, John Doe'
pl_translation = trans('some-key', params={'firstname': 'John', 'lastname': 'Doe'}, lang='pl')  # 'Witaj, John Doe'
```

`trans` function is searching for translation files in `config.locale_path`. It means that if the user requested translation
for `lang='en'` it will search for `$config.locale_path/en.json` file .

### Extracting translations from source code


### Error handling
