import json
import os
from typing import Any, Dict, Optional

from i18n.config import CONFIG
from i18n.errors import (
    TranslationFileInvalidFormatError,
    TranslationFileNotFoundError,
    TranslationFormatError,
    TranslationNotFoundError,
)

__cache__ = {}


def _translations(lang: str) -> Dict[str, str]:
    try:
        return __cache__[lang]
    except KeyError:
        path = os.path.join(CONFIG["locale"], f"{lang}.json")
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
    lang = lang or CONFIG["fallback_lang"]

    try:
        translations = _translations(lang)
    except TranslationFileNotFoundError:
        translations = _translations(CONFIG["fallback_lang"])

    try:
        translation_string = translations[key]
    except KeyError:
        raise TranslationNotFoundError(f"Missing key={key}", lang=lang, key=key)

    try:
        return translation_string.format(**(params if params else {}))
    except:
        raise TranslationFormatError(
            f"Invalid format for key={key}", lang=lang, key=key
        )
