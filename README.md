# lemon-i18n
[![License](https://img.shields.io/github/license/lemon-markets/pip-i18n-turbo
)](./LICENSE)
[![Tests](https://img.shields.io/github/workflow/status/lemon-markets/pip-i18n-turbo/tests/main?label=tests)](https://github.com/lemon-markets/sdk-python/actions)
[![Python versions](https://img.shields.io/pypi/pyversions/pip-i18n-turbo.svg)](https://pypi.python.org/pypi/lemon-i18n/)
[![PyPI](https://img.shields.io/pypi/v/lemon-i18n)](https://pypi.python.org/pypi/lemon-i18n/)

**lemon-i18n** is a library for internationalization and localization (i18n) of your Python applications

# Why to use this library?

TBD

## Installation

You can install library using [pip](http://pypi.python.org/pypi/pip):

```bash
pip install lemon-i18n
```

## Requirements
- Python 3.8, 3.9, 3.10

# Usage

The table below describes the terms used widely in this documentation.

## Glossary
| Term                | Description                                                        |
|---------------------|--------------------------------------------------------------------|
| translation key     | unique key identifying translation string                          |
| translation string  | string to be translated                                            |
| translation context | data should be used to fill in the translation string              |
| translation         | translation string filled with translation data                    |
| translation file    | file containing mapping of translation keys and translation string |

## General
As part of `lemon-i18n`, we offer two main functionalities:

- API to access translation for a given key and language
- a cli tool used to scan the Python source code for translation keys and storing them in a translation file

## Configuring the `lemon-i18n` module

`lemon-i18n` has to be configured to achieve expected functionality.
Configuration is done by modifying global `config` object before first usage of `trans` function.

```python
from i18n import config

config.fallback_lang = 'en'
config.locale_path = '/path/to/your/locale/directory'
config.fallback_translation = False
```
The table below describes the configuration parameters:

| Parameter            | Description                                                                                                                                                                                                                                            | Default value |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| fallback_lang        | fallback language to search for translation key if one cannot be found within requested language                                                                                                                                                       | en            |
| locale_path          | directory path to locale files                                                                                                                                                                                                                         | ./locale      |
| fallback_translation | flag determining the behavior of `trans` function in case given translation key is not found within requested language and fallback language. If set to True - translation key will be returned, otherwise - `TranslationNotFoundError` will be raised | True          |

## Using `trans` function

`trans` function is executing two steps:
- firstly, it searches for translation string based on translation key and requested language
- secondly, it populates translation context within translation string to finally return ready translation.

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
from i18n import trans
# The content of the './locale/en.json' is as follows:
# {
#    "some-key": "Welcome {firstname} {lastname}"
# }
translated_string = trans('some-key', params={'firstname': 'John', 'lastname': 'Doe'})
```

## Extracting translations from source code


## Error handling
