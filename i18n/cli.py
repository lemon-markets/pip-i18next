import argparse
import json
import logging
import os
import sys
from typing import Iterable, Iterator

from i18n import config
from i18n.parser import parse

logger = logging.getLogger("i81n.cli")


def _get_python_paths(search_paths: Iterable[str]) -> Iterator[str]:
    for path in search_paths:
        path = os.path.abspath(path)
        if os.path.isdir(path):
            paths = []
            for root, _, files in os.walk(path):
                for f in files:
                    if f.endswith(".py"):
                        paths.append(os.path.join(root, f))
            yield from _get_python_paths(paths)
        elif os.path.isfile(path) and path.endswith(".py"):
            yield path


def update_translation_keys(paths: Iterable[str]) -> None:
    keys = parse(paths)

    target_path = os.path.abspath(
        os.path.join(config.locale_path, f"{config.fallback_lang}.json")
    )

    if not os.path.exists(os.path.dirname(target_path)):
        logger.error(
            f"Failed to generate translation file. "
            f"Missing locale directory {os.path.dirname(target_path)!r}"
        )
        sys.exit(-1)

    try:
        with open(target_path) as fh:
            en = json.load(fh)
    except:
        en = {}

    missing_keys = set(keys) - set(en)
    en.update({k: "" for k in missing_keys})
    en = {k: en[k] for k in sorted(en)}

    with open(target_path, "wt") as fh:
        json.dump(en, fh, indent=2, ensure_ascii=False)


def main(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("search_paths", nargs="*", default=["."])
    parser.add_argument("--locale", nargs="?", type=str)
    parser.add_argument("--lang", nargs="?")
    parser.add_argument("--debug", "-d", action="store_true")

    args = parser.parse_args(args=args)

    if args.locale:
        config.locale_path = args.locale

    if args.lang:
        config.fallback_lang = args.lang

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    paths = set(_get_python_paths(args.search_paths))

    logger.debug(f"Config: {config.dict()}")
    logger.debug("Paths to be parsed:")
    for path in paths:
        logger.debug(f" {path}")

    update_translation_keys(paths)


if __name__ == "__main__":
    try:
        main()
    except:
        sys.exit(-1)
