import argparse
import json
import os
import sys
from typing import Iterable, Iterator

from i18n.config import CONFIG
from i18n.parser import parse


def _iterate_python_paths(search_paths: Iterable[str]) -> Iterator[str]:
    for path in search_paths:
        path = os.path.abspath(path)
        if os.path.isdir(path):
            paths = []
            for root, _, files in os.walk(path):
                for f in files:
                    if f.endswith(".py"):
                        paths.append(os.path.join(root, f))
            yield from _iterate_python_paths(paths)
        elif os.path.isfile(path) and path.endswith(".py"):
            yield path


def main():
    """
    Scan selected python files and update en.json with new translation keys
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("search_paths", nargs="*", default=["."])

    args = parser.parse_args()

    paths = set(_iterate_python_paths(args.search_paths))
    fallback_lang = CONFIG["fallback_lang"]

    keys = parse(paths)

    try:
        with open(os.path.join(CONFIG["locale"], f"{fallback_lang}.json")) as fh:
            en = json.load(fh)
    except:
        en = {}

    missing_keys = set(keys) - set(en)
    en.update({k: "" for k in missing_keys})
    en = {k: en[k] for k in sorted(en)}

    with open(os.path.join(CONFIG["locale"], f"{fallback_lang}.json"), "wt") as fh:
        json.dump(en, fh, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    try:
        main()
    except:
        sys.exit(-1)
