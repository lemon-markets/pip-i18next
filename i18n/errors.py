class I18nError(Exception):
    def __init__(self, message: str, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __repr__(self):
        return f"I18NError(message={self.message}, **{self.kwargs})"

    def dict(self):
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "kwargs": self.kwargs,
        }


class TranslationFileNotFoundError(I18nError):
    pass


class TranslationFileInvalidFormatError(I18nError):
    pass


class TranslationNotFoundError(I18nError):
    pass


class TranslationFormatError(I18nError):
    pass
