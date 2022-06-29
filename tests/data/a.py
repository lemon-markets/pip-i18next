from i18n import trans


class A:
    def __init__(self):
        self.a = 1

    def foo(self):
        return trans("a-1", params={"a": self.a})

    def bar(self):
        def buzz():
            return trans("a-2")

        return buzz()


def foo():
    return trans("a-3")


trans("a-4")
