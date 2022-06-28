import ast
import json
import os
import warnings
from collections import Counter, OrderedDict
from functools import cache
from typing import Optional, Union, List


@cache
def get_translation(lang: str) -> dict:
    # TODO: get translations
    pass


def trans(key, params=None, lang="en"):
    """
    Translation method
    """
    try:
        msg = get_translation(lang)[key]
    except:
        # fallback
        try:
            msg = get_translation("en")[key]
        except:
            return key
    try:
        return msg.format(**(params if params else {}))
    except:
        warnings.warn(
            f"No translation found for {key!r}. Returning key. \nTrace: {get_traceback()}"
        )
        return key


class Tree:
    def __init__(self):
        self.nodes = {}

    @classmethod
    def from_ast(self, root_node: ast.AST) -> "Tree":
        """
        Create Tree from ast.AST
        """
        tree = Tree()

        def _iter_ast(
                node: ast.AST,
                parent_node: Optional[ast.AST] = None,
        ):
            """
            Iterate through the AST and yield each node and its parent.
            """
            yield node, parent_node

            if hasattr(node, "_fields"):
                for k in node._fields:
                    if isinstance(sub_node := getattr(node, k), list):
                        for v in sub_node:
                            yield from _iter_ast(v, node)
                    else:
                        yield from _iter_ast(sub_node, node)

        for node, parent in _iter_ast(root_node):
            # filter out all non ast.AST objects
            if issubclass(type(node), ast.AST):
                tree.nodes.setdefault(parent, []).append(node)

        return tree

    def get_calls_with_related_imports(self):
        """
        Discover all function calls and associate them with corresponding imports
        """

        def iter_nodes(root_node, stack=None):
            stack = stack if stack else []

            yield root_node, stack

            for child in self.nodes.get(root_node, []):
                if isinstance(child, (ast.Import, ast.ImportFrom)):
                    stack.append(child)
                yield from iter_nodes(child, stack.copy())

        def func_name(func: Union[ast.Attribute, ast.Name]) -> str:
            """
            Get function path, like "path.to.module.function_name"
            This function is allowing for very simple function calls like:
            - func('x')
            - module.func('x')
            - _.func('x')

            """
            if isinstance(func, ast.Attribute):
                try:
                    return f"{func_name(func.value)}.{func.attr}"
                except:
                    raise
            elif isinstance(func, ast.Name):
                return func.id
            else:
                raise AttributeError(ast.dump(func))

        for child, stack in iter_nodes(self.root):
            # we are analyzing function calls only
            if not isinstance(child, ast.Call):
                continue

            try:
                function_name = func_name(child.func)
            except:
                continue

            for _imp in reversed(stack):

                aliases = OrderedDict(
                    [(i.asname if i.asname else i.name, i.name) for i in _imp.names]
                )

                if isinstance(child.func, ast.Name) and isinstance(
                        _imp, ast.ImportFrom
                ):
                    if hasattr(child.func, "id") and child.func.id in aliases:
                        yield child, f"{_imp.module}.{aliases[child.func.id]}"
                        break

                if isinstance(child.func, ast.Attribute) and isinstance(
                        _imp, ast.Import
                ):
                    matches = list(
                        filter(lambda x: function_name.startswith(x), aliases)
                    )
                    if matches:
                        yield child, f"{aliases[matches[-1]]}.{child.func.attr}"
                        break

    def extract_calls(self, function_module_path):
        """
        Extract all calls matching module path
        """
        for call, imp in self.get_calls_with_related_imports():
            if imp == function_module_path:
                yield call

    @property
    def root(self):
        """
        Get root node
        """
        return self.nodes[None][0]

    def __repr__(self):
        return self.nodes


def is_call_valid(call: ast.Call):
    """
    Validate if the call has at least one positional argument which is a string
    """
    return (
            len(call.args) >= 1
            and isinstance(call.args[0], ast.Constant)
            and isinstance(call.args[0].value, str)
    )


def extract_keys() -> List[str]:
    def get_python_paths(root_path):
        """
        Get all python files under the root path
        """
        for root, directories, files in os.walk(root_path):
            for filename in files:
                if filename.endswith(".py"):
                    yield os.path.join(root, filename)

    DIRS_TO_CHECK = [PATH_PLAYBOOK, PATH_APPS]
    THIS_FILE = os.path.abspath(__file__)
    keys = []

    for dir in DIRS_TO_CHECK:
        for path in get_python_paths(dir):
            if path == THIS_FILE:
                continue

            with open(path, "r") as f:
                tree = Tree.from_ast(ast.parse(f.read()))

            for call in tree.extract_calls("playbook.i18n.trans"):
                if is_call_valid(call):
                    keys.append(call.args[0].value)
    return keys


def i18n(ctx):
    """
    Scan selected python files and update en.json with new translation keys
    """
    keys = extract_keys()
    if len(keys) != len(set(keys)):
        for k, v in Counter(keys).items():
            if v > 1:
                warnings.warn(f"Found duplicated key {k} (amount={v})")
        return

    try:
        with open(os.path.join(PATH_TO_LOCALE, "en.json"), "rt") as fh:
            en = json.load(fh)
    except:
        en = {}

    missing_keys = set(keys) - set(en)
    en.update({k: "" for k in missing_keys})
    en = {k: en[k] for k in sorted(en)}

    with open(os.path.join(PATH_TO_LOCALE, "en.json"), "wt") as fh:
        json.dump(en, fh, indent=2, ensure_ascii=False)
