import ast
import inspect

from i18n.parser import _Tree


def func1():
    pass


def func2():
    from i18n import trans

    trans("1")


def func3():
    from i18n import trans as _

    _("2")


def func4():
    import i18n

    i18n.trans("3")


def func5():
    import i18n as _

    _.trans("4")


def func6():
    class A:
        def __init__(self):
            pass

        def a(self):
            from i18n import trans

            trans("1")

        def b(self):
            from i18n import trans as _

            _("2")

        def c(self):
            import i18n

            i18n.trans("3")

        def d(self):
            import i18n as _

            _.trans("4")


def func7():
    from i18n import trans

    trans("a " + "b " + "c")


def dump(node: ast.AST):
    if hasattr(node, "_fields"):
        d = {}
        for k in node._fields:
            v = getattr(node, k)
            if isinstance(v, list):
                d[k] = [dump(sv) for sv in v]
            else:
                d[k] = dump(v)
        return d
    else:
        return node


def test_root():
    node = ast.parse(inspect.getsource(func1))
    tree = _Tree.from_ast(node)
    assert tree.root == node


def test_get_calls_with_imports_for__from__x__import__y():
    tree = _Tree.from_ast(ast.parse(inspect.getsource(func2)))

    result = list(tree.get_calls_with_related_imports())
    assert len(result) == 1
    call, _import = result[0]

    assert isinstance(call.func.ctx, ast.Load)

    assert dump(call) == {
        "args": [{"kind": None, "value": "1"}],
        "func": {"ctx": {}, "id": "trans"},
        "keywords": [],
    }
    assert dump(_import) == "i18n.trans"


def test_get_calls_with_imports_for__from__x_import__y_as():
    tree = _Tree.from_ast(ast.parse(inspect.getsource(func3)))

    result = list(tree.get_calls_with_related_imports())
    assert len(result) == 1
    call, _import = result[0]

    assert isinstance(call.func.ctx, ast.Load)

    assert dump(call) == {
        "args": [{"kind": None, "value": "2"}],
        "func": {"ctx": {}, "id": "_"},
        "keywords": [],
    }
    assert dump(_import) == "i18n.trans"


def test_get_calls_with_imports_for__import__x():
    tree = _Tree.from_ast(ast.parse(inspect.getsource(func4)))
    result = list(tree.get_calls_with_related_imports())

    assert len(result) == 1
    call, _import = result[0]

    assert isinstance(call.func.ctx, ast.Load)

    assert dump(call) == {
        "args": [{"kind": None, "value": "3"}],
        "func": {"attr": "trans", "ctx": {}, "value": {"ctx": {}, "id": "i18n"}},
        "keywords": [],
    }
    assert dump(_import) == "i18n.trans"


def test_get_calls_with_imports_for__import__x__as():
    tree = _Tree.from_ast(ast.parse(inspect.getsource(func5)))
    result = list(tree.get_calls_with_related_imports())

    assert len(result) == 1
    call, _import = result[0]

    assert isinstance(call.func.ctx, ast.Load)

    assert dump(call) == {
        "args": [{"kind": None, "value": "4"}],
        "func": {"attr": "trans", "ctx": {}, "value": {"ctx": {}, "id": "_"}},
        "keywords": [],
    }
    assert dump(_import) == "i18n.trans"


def test_get_calls_with_imports_from__class():
    tree = _Tree.from_ast(ast.parse(inspect.getsource(func6)))
    result = list(tree.extract_calls("i18n.trans"))

    assert len(result) == 4

    for r, exp in zip(result, ["1", "2", "3", "4"]):
        assert r.args[0].value == exp
