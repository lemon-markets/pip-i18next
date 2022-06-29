import json
import os
from typing import Any, Dict, Optional

from i18n.config import config
from i18n.errors import (
    TranslationFileInvalidFormatError,
    TranslationFileNotFoundError,
    TranslationFormatError,
    TranslationNotFoundError,
    I18nError,
)

__cache__ = {}


def _load_translations(lang: str) -> Dict[str, str]:
    try:
        return __cache__[lang]
    except KeyError:
        path = os.path.abspath(os.path.join(config.locale_path, f"{lang}.json"))
        try:
            with open(path) as fg:
                __cache__[lang] = json.load(fg)
        except FileNotFoundError:
            raise TranslationFileNotFoundError(
                f"Missing {lang!r} translation file {path!r}", path=path, lang=lang
            )
        except json.decoder.JSONDecodeError:
            raise TranslationFileInvalidFormatError(
                f"Invalid {lang!r} translation file {path!r}", path=path, lang=lang
            )
    return __cache__[lang]


def trans(
    key: str, params: Optional[Dict[str, Any]] = None, lang: Optional[str] = None
):
    lang = lang or config.fallback_lang

    try:
        translations = _load_translations(lang)
    except I18nError:
        try:
            translations = _load_translations(config.fallback_lang)
        except I18nError:
            if config.fallback_translation:
                return key
            raise

    try:
        trans_string = translations[key]
    except KeyError as e:
        if config.fallback_translation:
            return key
        raise TranslationNotFoundError(f"Missing key={key}", lang=lang, key=key) from e

    try:
        return trans_string.format(**(params if params else {}))
    except Exception as e:
        if config.fallback_translation:
            return key
        raise TranslationFormatError(
            f"Invalid format for key={key}", lang=lang, key=key
        ) from e


def clear_cache():
    global __cache__
    __cache__ = {}
