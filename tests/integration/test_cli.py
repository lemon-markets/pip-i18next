import json
import os.path
from tempfile import TemporaryDirectory

import pytest

from cli import main
from tests.utils import TEST_DIR


@pytest.fixture
def data():
    def create_path(filename):
        return str(os.path.join(TEST_DIR, "data", filename))

    return create_path


@pytest.fixture
def locale():
    return TemporaryDirectory()


def cli_call(search_paths, locale, lang=None):
    lang = lang or "en"
    return main([search_paths, "--locale", locale, "--lang", lang, "-d"])


def test_update_translation_file_from_file(data, locale):
    cli_call(data("a.py"), locale.name)

    with open(os.path.join(locale.name, "en.json")) as fh:
        en = json.load(fh)

    assert {
        "a-1": "",
        "a-2": "",
        "a-3": "",
        "a-4": "",
    } == en


def test_update_translation_file_from_file_with_lang(data, locale):
    cli_call(data("a.py"), locale.name, "de")

    with open(os.path.join(locale.name, "de.json")) as fh:
        en = json.load(fh)

    assert {
        "a-1": "",
        "a-2": "",
        "a-3": "",
        "a-4": "",
    } == en


def test_update_translation_file_from_dir(data, locale):
    cli_call(os.path.join(TEST_DIR, "data"), locale.name)

    with open(os.path.join(locale.name, "en.json")) as fh:
        en = json.load(fh)

    assert {
        "a-1": "",
        "a-2": "",
        "a-3": "",
        "a-4": "",
        "b-1": "",
        "b-2": "",
        "b-3": "",
        "b-4": "",
    } == en

    # do not overwrite existing keys
    with open(os.path.join(locale.name, "en.json"), "wt") as fh:
        en["a-1"] = "some-translation"
        json.dump(en, fh)

    cli_call(os.path.join(TEST_DIR, "data"), locale.name)

    with open(os.path.join(locale.name, "en.json")) as fh:
        en = json.load(fh)

    assert {
        "a-1": "some-translation",
        "a-2": "",
        "a-3": "",
        "a-4": "",
        "b-1": "",
        "b-2": "",
        "b-3": "",
        "b-4": "",
    } == en


def test_fail_if_locale_are_invalid():
    with pytest.raises(SystemExit):
        cli_call(os.path.join(TEST_DIR, "data"), "./invalid/locale")
