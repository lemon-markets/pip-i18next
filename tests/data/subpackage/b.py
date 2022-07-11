from i18next import trans


class B:
    def __init__(self):
        self.a = 1

    def foo(self):
        return trans("b-1", params={"a": self.a})

    def bar(self):
        def buzz():
            return trans("b-2")

        return buzz()


def foo():
    return trans("b-3")


trans("b-4")
