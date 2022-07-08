import json
import os.path
from i18next import config, trans
from tempfile import TemporaryDirectory

import pytest

from i18next.base import clear_cache
from i18next.errors import (
    TranslationFileNotFoundError,
    TranslationNotFoundError,
    TranslationFormatError,
    TranslationFileInvalidFormatError,
)


@pytest.fixture
def locale():
    en_content = {"key": "translation and arg {arg}"}
    directory = TemporaryDirectory()
    path = os.path.join(directory.name, "en.json")

    with open(path, "w") as f:
        json.dump(en_content, f)

    yield directory

    directory.cleanup()


class TestNoFallbackOnMissingTranslationTests:
    @pytest.fixture(autouse=True)
    def setup(self, locale):
        config.locale_path = locale.name
        config.fallback_lang = "en"
        config.strict = True

    def test_fail_on_missing_translation_file(self):
        config.fallback_lang = "de"
        with pytest.raises(TranslationFileNotFoundError) as err:
            trans("key", lang="it")

        assert err.value.message.startswith("Missing")
        assert err.value.kwargs["lang"] == "de"

        assert isinstance(err.value.dict(), dict)

    def test_fail_on_missing_translation(self):
        with pytest.raises(TranslationNotFoundError):
            trans("key-a")

    def test_fail_on_bad_formatting(self):
        with pytest.raises(TranslationFormatError):
            trans("key", params={"other-arg": 1})

    def test_fail_on_invalid_translation_format(self, locale):
        clear_cache()

        with open(os.path.join(locale.name, "en.json"), "wt") as fh:
            fh.write("bum")

        with pytest.raises(TranslationFileInvalidFormatError):
            trans("key")

    def test_get_translation(self):
        result = trans("key", params={"arg": "translated arg"})
        assert result == "translation and arg translated arg"


class TestFallbackOnMissingTranslationTests:
    @pytest.fixture(autouse=True)
    def setup(self, locale):
        config.locale_path = locale.name
        config.fallback_lang = "en"
        config.strict = False

    def test_fail_on_missing_translation_file(self):
        config.fallback_lang = "de"
        assert trans("key", lang="it") == "key"

    def test_fail_on_missing_translation(self):
        assert trans("key-a") == "key-a"

    def test_fail_on_bad_formatting(self):
        assert trans("key", params={"other-arg": 1}) == "key"

    def test_get_translation(self):
        result = trans("key", params={"arg": "translated arg"})
        assert result == "translation and arg translated arg"
